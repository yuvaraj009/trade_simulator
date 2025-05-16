import websocket
import json
import threading
import time
import logging
from queue import Queue

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

class OrderBookWebSocket:
    def __init__(self, symbol, message_queue, reconnect_timeout=5, ping_interval=20, ping_timeout=10):
        self.symbol = symbol
        self.message_queue = message_queue
        self.ws_url = f"wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/{symbol}"
        self.ws = None
        self.thread = None
        self.running = False
        self.reconnect_timeout = reconnect_timeout
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            self.message_queue.put(data)
        except json.JSONDecodeError as e:
            logging.warning(f"JSON decode error: {e}")

    def on_error(self, ws, error):
        logging.error(f"WebSocket error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        logging.warning(f"WebSocket closed: {close_status_code} - {close_msg}")
        self.running = False

    def on_open(self, ws):
        logging.info("WebSocket connection established")
        self.running = True

    def run_forever(self):
        while True:
            try:
                self.ws = websocket.WebSocketApp(
                    self.ws_url,
                    on_open=self.on_open,
                    on_message=self.on_message,
                    on_error=self.on_error,
                    on_close=self.on_close
                )
                self.ws.run_forever(
                    ping_interval=self.ping_interval,
                    ping_timeout=self.ping_timeout
                )
            except Exception as e:
                logging.exception(f"Exception in WebSocket thread: {e}")
            finally:
                self.running = False
                logging.info(f"Reconnecting in {self.reconnect_timeout} seconds...")
                time.sleep(self.reconnect_timeout)

    def start(self):
        logging.info(f"Starting WebSocket for symbol: {self.symbol}")
        self.thread = threading.Thread(target=self.run_forever, daemon=True)
        self.thread.start()

    def stop(self):
        if self.ws:
            logging.info("Closing WebSocket connection...")
            self.ws.close()
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)
            logging.info("WebSocket thread terminated cleanly")
