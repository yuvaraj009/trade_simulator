import numpy as np
from scipy.stats import norm
from sklearn.linear_model import LogisticRegression

class TradeSimulatorModels:

    @staticmethod
    def calculate_slippage(order_book, quantity, side='buy'):
        """
        Estimate slippage as the % difference from top of book to VWAP of fulfilled levels
        """
        book_side = order_book['asks'] if side == 'buy' else order_book['bids']
        prices = np.array([float(p) for p, _ in book_side])
        vols = np.array([float(v) for _, v in book_side])
        cum_vol = np.cumsum(vols)

        if quantity > cum_vol[-1]:
            return float('inf')  # Not enough liquidity

        idx = np.searchsorted(cum_vol, quantity)
        fulfilled_price = prices[0]
        if idx > 0:
            remaining_qty = quantity - cum_vol[idx - 1]
            total_qty = cum_vol[idx - 1] + remaining_qty
            price_sum = np.sum(prices[:idx] * vols[:idx]) + prices[idx] * remaining_qty
        else:
            price_sum = prices[0] * quantity
            total_qty = quantity

        vwap = price_sum / quantity
        slippage = ((vwap - prices[0]) / prices[0]) if side == 'buy' else ((prices[0] - vwap) / prices[0])
        return slippage * 100

    @staticmethod
    def calculate_fees(quantity, price, fee_tier=0.0005):
        """
        Estimate trading fee (notional * fee rate)
        """
        return quantity * price * fee_tier

    @staticmethod
    def almgren_chriss_impact(quantity, volatility, liquidity, permanent_impact=0.1, temporary_impact=0.1):
        """
        Almgren-Chriss market impact approximation (simplified version)
        """
        daily_vol = volatility / np.sqrt(252)
        cost = permanent_impact * quantity + (temporary_impact * quantity ** 2) / liquidity
        return cost * daily_vol

    @staticmethod
    def estimate_maker_taker_ratio(order_book, window_size=100):
        """
        Estimate prob(maker) using logistic regression on spread width
        (placeholder: uses random data for training)
        """
        best_bid = float(order_book['bids'][0][0])
        best_ask = float(order_book['asks'][0][0])
        spread = best_ask - best_bid
        mid = (best_ask + best_bid) / 2
        rel_spread = spread / mid

        # Simulate a training set of [relative_spread, is_maker]
        X = np.random.rand(window_size, 1) * 0.1  # rel spread ~ [0, 10%]
        y = (np.random.rand(window_size) > 0.3).astype(int)  # 70% chance maker

        model = LogisticRegression()
        model.fit(X, y)

        # Predict maker prob at current spread
        prob = model.predict_proba([[rel_spread]])[0][1]
        return prob if prob else 0.5
