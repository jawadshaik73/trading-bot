"""
CLI interface for the Trading Bot using Click.
Provides an elegant, user-friendly command-line interface.
Supports multiple exchange modes: mock, ccxt, and binance.
"""
import sys
import click
from tabulate import tabulate
from colorama import Fore, Style, init
from trading_bot.bot import BinanceClient, OrderManager, BinanceAPIError, ValidationError
from trading_bot.bot.ccxt_client import CCXTClient, CCXTAPIError
from trading_bot.bot.mock_exchange import MockExchange
from trading_bot.bot.logging_config import setup_logger
import config

# Initialize colorama for cross-platform colored output
init(autoreset=True)

logger = setup_logger(__name__)


class BotContext:
    """Context object for storing CLI state with dynamic exchange selection."""
    def __init__(self):
        self.mode = config.EXCHANGE_MODE
        
        if self.mode == "mock":
            # Use MockExchange - completely offline, no API calls
            self.exchange = MockExchange()
            self.client = None  # MockExchange doesn't use traditional client
            self.order_manager = None  # MockExchange handles orders directly
            self.is_mock = True
        elif self.mode == "ccxt":
            # Use CCXT library with Binance
            self.client = CCXTClient()
            self.exchange = self.client  # CCXT client is the exchange
            self.order_manager = None  # CCXT handles orders directly
            self.is_mock = False
        elif self.mode == "binance":
            # Use legacy Binance REST API
            self.client = BinanceClient()
            self.exchange = None
            self.order_manager = OrderManager(self.client)
            self.is_mock = False
        else:
            raise ValueError(f"Invalid EXCHANGE_MODE: {self.mode}. Must be 'mock', 'ccxt', or 'binance'")


def print_header():
    """Print application header with current exchange mode."""
    mode_display = config.EXCHANGE_MODE.upper()
    mode_color = Fore.GREEN if config.EXCHANGE_MODE == "mock" else Fore.YELLOW
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}  🤖 Trading Bot - {mode_color}[{mode_display} MODE]{Fore.CYAN}")
    print(f"{Fore.CYAN}  v1.0.0 - Professional Trading Interface")
    print(f"{Fore.CYAN}{'='*60}\n")


def print_success(message: str):
    """Print success message."""
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")


def print_error(message: str):
    """Print error message."""
    print(f"{Fore.RED}✗ {message}{Style.RESET_ALL}")


def print_info(message: str):
    """Print info message."""
    print(f"{Fore.YELLOW}ℹ {message}{Style.RESET_ALL}")


@click.group()
@click.pass_context
def cli(ctx):
    """
    Trading Bot CLI - Place orders on Binance Futures Testnet.
    
    This tool provides a clean interface to interact with Binance Futures Testnet.
    Make sure to set API credentials in .env file before using.
    """
    ctx.ensure_object(dict)
    ctx.obj['bot'] = BotContext()


@cli.command()
@click.option(
    '--symbol',
    prompt='Trading symbol (e.g., BTCUSDT or BTC/USDT)',
    type=str,
    help='Trading pair'
)
@click.option(
    '--side',
    type=click.Choice(['BUY', 'SELL'], case_sensitive=False),
    prompt='Order side',
    help='Buy or Sell'
)
@click.option(
    '--quantity',
    prompt='Quantity',
    type=float,
    help='Order quantity'
)
@click.pass_context
def market(ctx, symbol, side, quantity):
    """
    Place a MARKET order.
    
    Market orders execute immediately at the current market price.
    Works in mock, ccxt, or binance mode based on configuration.
    """
    print_header()
    print_info(f"Preparing {side} market order...")
    
    try:
        bot = ctx.obj['bot']
        
        # Normalize symbol format based on mode
        if bot.mode in ['mock', 'ccxt']:
            # CCXT and Mock use BTC/USDT format
            if '/' not in symbol:
                # Convert BTCUSDT to BTC/USDT
                if symbol.endswith('USDT'):
                    base = symbol[:-4]
                    symbol = f"{base}/USDT"
        else:
            # Binance API uses BTCUSDT format
            if '/' in symbol:
                symbol = symbol.replace('/', '')
        
        # Show order summary
        print(f"\n{Fore.CYAN}Order Summary:")
        summary_data = [
            ['Symbol', symbol],
            ['Side', side.upper()],
            ['Type', 'MARKET'],
            ['Quantity', quantity],
            ['Price', 'Market Price'],
        ]
        print(tabulate(summary_data, tablefmt='grid'))
        
        # Confirm execution
        if not click.confirm(f"\n{Fore.YELLOW}Execute this order?", default=True):
            print_info("Order cancelled by user")
            return
        
        print(f"\n{Fore.CYAN}Executing order...")
        
        # Execute order based on mode
        if bot.mode == 'mock' or bot.mode == 'ccxt':
            # Mock and CCXT use create_order
            response = bot.exchange.create_order(
                symbol=symbol,
                order_type='market',
                side=side.lower(),
                amount=quantity
            )
            
            # Normalize response to match Binance format
            normalized_response = {
                'orderId': response.get('id', response.get('orderId', 'N/A')),
                'symbol': response.get('symbol', symbol),
                'side': response.get('side', side).upper(),
                'status': response.get('status', 'UNKNOWN').upper(),
                'quantity': response.get('amount', quantity),
                'executedQty': response.get('filled', response.get('amount', quantity)),
                'avgPrice': response.get('average', response.get('price', 0)),
                'cumulativeQuoteQty': response.get('cost', 0),
            }
            response = normalized_response
        else:
            # Binance mode uses order_manager
            response = bot.order_manager.place_market_order(symbol, side, quantity)
        
        # Display order response
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}✓ ORDER PLACED SUCCESSFULLY{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        
        response_data = [
            ['Order ID', response['orderId']],
            ['Symbol', response['symbol']],
            ['Side', response['side']],
            ['Status', response['status']],
            ['Quantity', response['quantity']],
            ['Executed Qty', response['executedQty']],
            ['Avg Price', f"{response['avgPrice']:.8f}" if response['avgPrice'] else "N/A"],
            ['Quote Qty', f"{response['cumulativeQuoteQty']:.8f}"],
        ]
        print(tabulate(response_data, tablefmt='grid'))
        
        print_success(f"Market order {response['orderId']} placed on {symbol}")
        logger.info(f"Market order placed: {response['orderId']}")
    
    except (ValidationError, BinanceAPIError, CCXTAPIError) as e:
        print_error(f"Error: {str(e)}")
        logger.error(f"Order error: {str(e)}")
        sys.exit(1)
    
    except Exception as e:
        print_error(f"Unexpected Error: {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option(
    '--symbol',
    prompt='Trading symbol (e.g., BTCUSDT)',
    type=str,
    help='Futures trading pair'
)
@click.option(
    '--side',
    type=click.Choice(['BUY', 'SELL'], case_sensitive=False),
    prompt='Order side',
    help='Buy or Sell'
)
@click.option(
    '--quantity',
    prompt='Quantity',
    type=float,
    help='Order quantity'
)
@click.option(
    '--price',
    prompt='Limit price',
    type=float,
    help='Order price'
)
@click.option(
    '--tif',
    type=click.Choice(['GTC', 'IOC', 'FOK'], case_sensitive=False),
    default='GTC',
    help='Time in Force (GTC=Good Till Cancel, IOC=Immediate or Cancel, FOK=Fill or Kill)'
)
@click.pass_context
def limit(ctx, symbol, side, quantity, price, tif):
    """
    Place a LIMIT order on Binance Futures Testnet.
    
    Limit orders execute only at the specified price or better.
    Works in mock, ccxt, or binance mode based on configuration.
    """
    print_header()
    print_info(f"Preparing {side} limit order...")
    
    try:
        bot = ctx.obj['bot']
        
        # Normalize symbol format based on mode
        if bot.mode in ['mock', 'ccxt']:
            # CCXT and Mock use BTC/USDT format
            if '/' not in symbol:
                # Convert BTCUSDT to BTC/USDT
                if symbol.endswith('USDT'):
                    base = symbol[:-4]
                    symbol = f"{base}/USDT"
        else:
            # Binance API uses BTCUSDT format
            if '/' in symbol:
                symbol = symbol.replace('/', '')
        
        # Show order summary
        print(f"\n{Fore.CYAN}Order Summary:")
        summary_data = [
            ['Symbol', symbol],
            ['Side', side.upper()],
            ['Type', 'LIMIT'],
            ['Quantity', quantity],
            ['Price', f"{price:.8f}"],
            ['Time in Force', tif.upper()],
        ]
        print(tabulate(summary_data, tablefmt='grid'))
        
        # Confirm execution
        if not click.confirm(f"\n{Fore.YELLOW}Execute this order?", default=True):
            print_info("Order cancelled by user")
            return
        
        print(f"\n{Fore.CYAN}Executing order...")
        
        # Execute order based on mode
        if bot.mode == 'mock' or bot.mode == 'ccxt':
            # Mock and CCXT use create_order
            response = bot.exchange.create_order(
                symbol=symbol,
                order_type='limit',
                side=side.lower(),
                amount=quantity,
                price=price
            )
            
            # Normalize response to match Binance format
            normalized_response = {
                'orderId': response.get('id', response.get('orderId', 'N/A')),
                'symbol': response.get('symbol', symbol),
                'side': response.get('side', side).upper(),
                'status': response.get('status', 'UNKNOWN').upper(),
                'quantity': response.get('amount', quantity),
                'executedQty': response.get('filled', response.get('amount', quantity)),
                'avgPrice': response.get('average', response.get('price', 0)),
                'cumulativeQuoteQty': response.get('cost', 0),
                'price': response.get('price', price),
                'timeInForce': response.get('timeInForce', tif.upper()),
            }
            response = normalized_response
        else:
            # Binance mode uses order_manager
            response = bot.order_manager.place_limit_order(
                symbol, side, quantity, price, tif.upper()
            )
        
        # Display order response
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}✓ ORDER PLACED SUCCESSFULLY{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        
        response_data = [
            ['Order ID', response['orderId']],
            ['Symbol', response['symbol']],
            ['Side', response['side']],
            ['Status', response['status']],
            ['Quantity', response['quantity']],
            ['Price', f"{response['price']:.8f}"],
            ['Executed Qty', response['executedQty']],
            ['Avg Price', f"{response['avgPrice']:.8f}" if response['avgPrice'] else "N/A"],
            ['Time in Force', response['timeInForce']],
        ]
        print(tabulate(response_data, tablefmt='grid'))
        
        print_success(f"Limit order {response['orderId']} placed on {symbol}")
        logger.info(f"Limit order placed: {response['orderId']}")
    
    except (ValidationError, BinanceAPIError, CCXTAPIError) as e:
        print_error(f"Error: {str(e)}")
        logger.error(f"Order error: {str(e)}")
        sys.exit(1)
    
    except Exception as e:
        print_error(f"Unexpected Error: {str(e)}")
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option('--symbol', prompt='Trading symbol (e.g., BTCUSDT or BTC/USDT)', type=str, help='Futures trading pair')
@click.option('--order-id', prompt='Order ID', type=int, help='Order ID to check')
@click.pass_context
def status(ctx, symbol, order_id):
    """
    Check the status of an existing order.
    Works in mock, ccxt, or binance mode based on configuration.
    """
    print_header()
    print_info(f"Fetching order status for {symbol} (ID: {order_id})...")
    
    try:
        bot = ctx.obj['bot']
        
        # Normalize symbol format based on mode
        if bot.mode in ['mock', 'ccxt']:
            # CCXT and Mock use BTC/USDT format
            if '/' not in symbol:
                # Convert BTCUSDT to BTC/USDT
                if symbol.endswith('USDT'):
                    base = symbol[:-4]
                    symbol = f"{base}/USDT"
        else:
            # Binance API uses BTCUSDT format
            if '/' in symbol:
                symbol = symbol.replace('/', '')
        
        # Fetch order based on mode
        if bot.mode == 'mock' or bot.mode == 'ccxt':
            # Mock and CCXT use fetch_order
            response = bot.exchange.fetch_order(
                order_id=order_id,
                symbol=symbol
            )
            
            # Normalize response to match Binance format
            normalized_response = {
                'orderId': response.get('id', response.get('orderId', order_id)),
                'symbol': response.get('symbol', symbol),
                'side': response.get('side', 'UNKNOWN').upper(),
                'status': response.get('status', 'UNKNOWN').upper(),
                'type': response.get('type', 'UNKNOWN').upper(),
                'quantity': response.get('amount', 0),
                'executedQty': response.get('filled', 0),
                'price': response.get('price', 0),
                'avgPrice': response.get('average', response.get('price', 0)),
                'timeInForce': response.get('timeInForce', 'N/A'),
            }
            response = normalized_response
        else:
            # Binance mode uses order_manager
            response = bot.order_manager.get_order_status(symbol, order_id)
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Order Status{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        status_data = [
            ['Order ID', response['orderId']],
            ['Symbol', response['symbol']],
            ['Side', response['side']],
            ['Status', response['status']],
            ['Type', response['type']],
            ['Quantity', response['quantity']],
            ['Executed', response['executedQty']],
            ['Price', f"{response['price']:.8f}" if response['price'] else "N/A"],
            ['Avg Price', f"{response['avgPrice']:.8f}" if response['avgPrice'] else "N/A"],
        ]
        print(tabulate(status_data, tablefmt='grid'))
        
        print_success(f"Order {order_id} status retrieved")
    
    except (BinanceAPIError, CCXTAPIError) as e:
        print_error(f"API Error: {str(e)}")
        logger.error(f"API error: {str(e)}")
        sys.exit(1)
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option('--symbol', prompt='Trading symbol (e.g., BTCUSDT or BTC/USDT)', type=str, help='Futures trading pair')
@click.option('--order-id', prompt='Order ID', type=int, help='Order ID to cancel')
@click.pass_context
def cancel(ctx, symbol, order_id):
    """
    Cancel an open order.
    Works in mock, ccxt, or binance mode based on configuration.
    """
    print_header()
    print_info(f"Attempting to cancel order {order_id} on {symbol}...")
    
    # Confirm cancellation
    if not click.confirm(f"{Fore.YELLOW}Are you sure you want to cancel this order?", default=False):
        print_info("Cancellation aborted")
        return
    
    try:
        bot = ctx.obj['bot']
        
        # Normalize symbol format based on mode
        if bot.mode in ['mock', 'ccxt']:
            # CCXT and Mock use BTC/USDT format
            if '/' not in symbol:
                # Convert BTCUSDT to BTC/USDT
                if symbol.endswith('USDT'):
                    base = symbol[:-4]
                    symbol = f"{base}/USDT"
        else:
            # Binance API uses BTCUSDT format
            if '/' in symbol:
                symbol = symbol.replace('/', '')
        
        # Cancel order based on mode
        if bot.mode == 'mock' or bot.mode == 'ccxt':
            # Mock and CCXT use cancel_order
            response = bot.exchange.cancel_order(
                order_id=order_id,
                symbol=symbol
            )
            
            # Normalize response to match Binance format
            normalized_response = {
                'orderId': response.get('id', response.get('orderId', order_id)),
                'symbol': response.get('symbol', symbol),
                'side': response.get('side', 'UNKNOWN').upper(),
                'status': response.get('status', 'UNKNOWN').upper(),
            }
            response = normalized_response
        else:
            # Binance mode uses order_manager
            response = bot.order_manager.cancel_order(symbol, order_id)
        
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}✓ ORDER CANCELLED SUCCESSFULLY{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        
        cancel_data = [
            ['Order ID', response['orderId']],
            ['Symbol', response['symbol']],
            ['Status', response['status']],
            ['Side', response['side']],
        ]
        print(tabulate(cancel_data, tablefmt='grid'))
        
        print_success(f"Order {order_id} cancelled successfully")
    
    except (BinanceAPIError, CCXTAPIError) as e:
        print_error(f"API Error: {str(e)}")
        logger.error(f"API error: {str(e)}")
        sys.exit(1)
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


@cli.command()
@click.pass_context
def info(ctx):
    """
    Display account information and balance.
    """
    print_header()
    print_info("Fetching account information...")
    
    try:
        client = ctx.obj['bot'].client
        account = client.get_account_balance()
        
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}Account Information{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        
        # Display key account info
        info_data = [
            ['Account Type', account.get('accountType', 'N/A')],
            ['Max Orders', account.get('maxOrders', 'N/A')],
            ['Max Algo Orders', account.get('maxAlgoOrders', 'N/A')],
        ]
        print(tabulate(info_data, tablefmt='grid'))
        
        # Display balances
        print(f"\n{Fore.CYAN}Balances:")
        if 'assets' in account and account['assets']:
            balances = []
            for asset in account['assets']:
                if float(asset.get('walletBalance', 0)) > 0:
                    balances.append([
                        asset['asset'],
                        float(asset['walletBalance']),
                        float(asset.get('unrealizedProfit', 0)),
                    ])
            
            if balances:
                print(tabulate(
                    balances,
                    headers=['Asset', 'Wallet Balance', 'Unrealized P&L'],
                    tablefmt='grid'
                ))
            else:
                print_info("No active balances")
        
        print_success("Account information retrieved")
    
    except BinanceAPIError as e:
        print_error(f"API Error: {str(e)}")
        logger.error(f"API error: {str(e)}")
        sys.exit(1)
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


@cli.command()
def test():
    """
    Test exchange connection.
    Works with mock, ccxt, or binance mode based on configuration.
    """
    print_header()
    print_info(f"Testing {config.EXCHANGE_MODE.upper()} mode connection...")
    
    try:
        bot = BotContext()
        
        if bot.mode == 'mock':
            # Test mock exchange
            if bot.exchange.test_connection():
                balance = bot.exchange.fetch_balance()
                
                print(f"\n{Fore.GREEN}{'='*60}")
                print(f"{Fore.GREEN}✓ MOCK EXCHANGE READY{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
                
                test_data = [
                    ['Mode', 'MOCK (Offline)'],
                    ['Status', '✓ Working'],
                    ['API Calls', 'None (Completely Offline)'],
                    ['USDT Balance', f"${balance['total'].get('USDT', 0):.2f}"],
                ]
                print(tabulate(test_data, tablefmt='grid'))
                
                print_success("Mock exchange is ready for testing!")
                print_info("No API credentials needed in mock mode")
                logger.info("Mock exchange test successful")
        
        elif bot.mode == 'ccxt':
            # Test CCXT client
            if bot.client.test_connection():
                balance = bot.client.fetch_balance()
                
                print(f"\n{Fore.GREEN}{'='*60}")
                print(f"{Fore.GREEN}✓ CCXT CONNECTION SUCCESSFUL{Style.RESET_ALL}")
                print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
                
                test_data = [
                    ['Mode', 'CCXT'],
                    ['Status', '✓ Connected'],
                    ['Environment', 'LIVE (Real Money!)'],
                    ['USDT Balance', f"${balance['total'].get('USDT', 0):.2f}"],
                ]
                print(tabulate(test_data, tablefmt='grid'))
                
                print_success("CCXT connection is working!")
                logger.info("CCXT connection test successful")
        
        else:
            # Test Binance client
            account = bot.client.get_account_balance()
            
            print(f"\n{Fore.GREEN}{'='*60}")
            print(f"{Fore.GREEN}✓ CONNECTION SUCCESSFUL{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            
            test_data = [
                ['Mode', 'BINANCE'],
                ['Account Type', account.get('accountType', 'N/A')],
                ['API Key Status', '✓ Valid'],
            ]
            print(tabulate(test_data, tablefmt='grid'))
            
            print_success("API credentials are valid and connection is working")
            logger.info("API connection test successful")
    
    except (BinanceAPIError, CCXTAPIError) as e:
        print_error(f"API Error: {str(e)}")
        print_info("Please check your API credentials in .env file")
        logger.error(f"API connection test failed: {str(e)}")
        sys.exit(1)
    
    except Exception as e:
        print_error(f"Error: {str(e)}")
        logger.error(f"Connection test error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    cli()
