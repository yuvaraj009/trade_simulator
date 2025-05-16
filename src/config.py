# WebSocket Config
WEBSOCKET_URL = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx"
DEFAULT_SYMBOL = "BTC-USDT-SWAP"
RECONNECT_TIMEOUT = 5  # seconds before trying again
HEARTBEAT_INTERVAL = 30  # ping server every 30 sec

# Trade Defaults
DEFAULT_USD_QTY = 100.0
MAX_DEPTH_LEVELS = 10  # max levels to fetch from order book
MIN_ORDER_SIZE = 0.001  # BTC units

# OKX Spot Fees (base tier)
MAKER_FEE = 0.0002  # 0.02
TAKER_FEE = 0.0005  # 0.05

# TODO: Pull these from API dynamically
Vip_Fee_Tiers = {
    'VIP0': { 'maker': 0.0002, 'taker': 0.0005 },
    'VIP1': { 'maker': 0.00018, 'taker': 0.00045 },
    'VIP2': { 'maker': 0.00016, 'taker': 0.0004 },
    # 'VIP3': ...
}

# Market Impact
PERMANENT_IMPACT_COEFF = 0.1   # η: permanent impact
TEMP_IMPACT_COEFF = 0.1        # γ: temporary impact
LIQUIDITY_LEVELS = 5           # levels to aggregate for liquidity

# UI/Frontend
UI_UPDATE_INTERVAL_MS = 100     # refresh rate for labels
DECIMAL_PRECISION = 4           # global decimal control
PRICE_DECIMALS = 2
QTY_DECIMALS = 6

# Perf & Logs
MAX_LATENCY_MS = 50            # upper latency bound
LOG_RETENTION_DAYS = 7         # delete old logs after 7d

# Pairs Available (expand later)
SUPPORTED_SYMBOLS = [
    "BTC-USDT-SWAP",
    "ETH-USDT-SWAP",
    "SOL-USDT-SWAP",
    "XRP-USDT-SWAP"
    # "DOGE-USDT-SWAP" ?
]
