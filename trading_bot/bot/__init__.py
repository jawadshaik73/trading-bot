"""
Trading Bot Package - Binance Futures Testnet
Supports multiple exchange modes: Binance Testnet (live) and Mock (offline).
"""
from .client import BinanceClient, BinanceAPIError
from .mock_client import MockClient
from .orders import OrderManager
from .validators import ValidationError

__all__ = [
    'BinanceClient',
    'BinanceAPIError',
    'MockClient',
    'OrderManager',
    'ValidationError'
]
