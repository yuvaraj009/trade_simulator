import sys
import time
from queue import Queue
from PyQt5.QtWidgets import QApplication
from websocket_client import OrderBookWebSocket
from models import TradeSimulatorModels
from ui import TradeSimulatorUI

class TradeSimulatorCore:
    def __init__(self):
        self.msg_q = Queue()
        self.ws = None
        self.models = TradeSimulatorModels()
        self.active = False
        self.res = {
            'slippage': 0,
            'fees': 0,
            'market_impact': 0,
            'net_cost': 0,
            'maker_prob': 0.5,
            'latency': 0,
            'book_depth': 0
        }
        self._last_time = time.time()
        
    def start(self, symbol, qty, vol, fee_level):
        if self.ws:
            self.ws.stop()
            
        self.qty = qty
        self.vol = vol
        self.fee = fee_level
        self.ws = OrderBookWebSocket(symbol, self.msg_q)
        self.ws.start()
        self.active = True
        
    def process_message(self, msg):
        start = time.time()

        buy_slip = self.models.calculate_slippage(msg, self.qty, 'buy')
        sell_slip = self.models.calculate_slippage(msg, self.qty, 'sell')
        slippage = (buy_slip + sell_slip) / 2
        
        top_ask = float(msg['asks'][0][0])
        top_bid = float(msg['bids'][0][0])
        mid = (top_ask + top_bid) / 2
        fees = self.models.calculate_fees(self.qty, mid, self.fee)
        
        liq = 0
        for level in msg['bids'][:5]:
            liq += float(level[1])
        impact = self.models.almgren_chriss_impact(self.qty, self.vol, liq)
        
        maker = self.models.estimate_maker_taker_ratio(msg)
        latency = time.time() - start
        
        self.res = {
            'slippage': slippage,
            'fees': fees,
            'market_impact': impact * 100,
            'net_cost': fees + (slippage/100 * self.qty * mid) + (impact * mid),
            'maker_prob': maker,
            'latency': latency,
            'book_depth': len(msg['asks']) + len(msg['bids'])
        }

    def getResults(self):
        while not self.msg_q.empty():
            item = self.msg_q.get()
            self.process_message(item)
        return self.res

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    sim = TradeSimulatorCore()
    ui = TradeSimulatorUI(sim)
    ui.show()
    
    sys.exit(app.exec_())
