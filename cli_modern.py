"""
Modern CLI interface for Trading Bot with interactive authentication.
Provides multiple authentication options without requiring .env files.
"""
import sys
import click
from tabulate import tabulate
from colorama import Fore, Style, init
from dotenv import load_dotenv
from trading_bot.bot import BinanceClient, OrderManager, BinanceAPIError, ValidationError
from trading_bot.bot.ccxt_client import CCXTClient, CCXTAPIError
from trading_bot.bot.mock_exchange import MockExchange
from trading_bot.bot.logging_config import setup_logger
from config_modern import EXCHANGE_MODE, API_CONFIG, CCXT_SANDBOX_MODE
from pathlib import Path

# Initialize colorama for cross-platform colored output
init(autoreset=True)

logger = setup_logger(__name__)


class ModernBotContext:
    """Modern context object with interactive authentication."""
    
    def __init__(self):
        self.mode = EXCHANGE_MODE
        self.is_mock = self.mode == "mock"
        
        if self.mode == "mock":
            # Use MockExchange - completely offline, no API calls
            self.exchange = MockExchange()
            self.client = None
            self.order_manager = None
            print_info("Using Mock Exchange (offline mode) - No API keys required")
            
        elif self.mode == "ccxt":
            # Use CCXT library with Binance
            api_key, api_secret = API_CONFIG.get_credentials()
            if not api_key or not api_secret:
                print_info("CCXT mode requires API credentials")
                API_CONFIG.prompt_for_credentials()
                api_key, api_secret = API_CONFIG.get_credentials()

                # Exit if credentials are still not available after prompt
                if not api_key or not api_secret:
                    print_error("API credentials not provided. Exiting.")
                    sys.exit(1)
            
            self.client = CCXTClient(api_key, api_secret, CCXT_SANDBOX_MODE)
            self.exchange = self.client
            self.order_manager = None
            print_info(f"Using CCXT with {'Sandbox' if CCXT_SANDBOX_MODE else 'Live'} mode")
            
        elif self.mode == "binance":
            # Use legacy Binance REST API
            api_key, api_secret = API_CONFIG.get_credentials()
            if not api_key or not api_secret:
                print_info("Binance REST API mode requires API credentials")
                API_CONFIG.prompt_for_credentials()
                api_key, api_secret = API_CONFIG.get_credentials()
            
            self.client = BinanceClient(api_key, api_secret)
            self.exchange = None
            self.order_manager = OrderManager(self.client)
            print_info("Using Binance REST API (Testnet)")
            
        else:
            raise ValueError(f"Invalid EXCHANGE_MODE: {self.mode}. Must be 'mock', 'ccxt', or 'binance'")


def print_header(mode: str):
    """Print application header with current exchange mode."""
    mode_display = mode.upper()
    mode_color = Fore.GREEN if mode == "mock" else Fore.YELLOW
    
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}  🤖 Modern Trading Bot - {mode_color}[{mode_display} MODE]{Fore.CYAN}")
    print(f"{Fore.CYAN}  v2.0.0 - Interactive Authentication")
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


def print_warning(message: str):
    """Print warning message."""
    print(f"{Fore.MAGENTA}⚠ {message}{Style.RESET_ALL}")


@click.group()
@click.pass_context
def cli(ctx):
    """
    Modern Trading Bot CLI - Multiple authentication options.
    
    Supports:
    - Mock mode (offline, no API keys)
    - CCXT mode (interactive API key input)
    - Binance REST API mode (interactive API key input)
    
    No .env file required! Just run and follow prompts.
    """
    ctx.ensure_object(dict)
    ctx.obj['bot'] = ModernBotContext()


@cli.command()
@click.pass_context
def info(ctx):
    """Show current configuration and exchange information."""
    bot = ctx.obj['bot']
    print_header(bot.mode)
    
    config_data = [
        ['Exchange Mode', EXCHANGE_MODE.upper()],
        ['Authentication', 'Interactive (No .env required)'],
        ['Sandbox Mode', str(CCXT_SANDBOX_MODE) if EXCHANGE_MODE == "ccxt" else 'N/A'],
        ['API Key Configured', 'Yes' if API_CONFIG.api_key else 'No'],
        ['API Secret Configured', 'Yes' if API_CONFIG.api_secret else 'No'],
    ]
    
    print(f"{Fore.CYAN}Configuration:{Style.RESET_ALL}")
    print(tabulate(config_data, tablefmt='grid'))
    
    if EXCHANGE_MODE == "mock":
        print_info("Running in offline mock mode - Perfect for testing!")
        print_info("No real API calls will be made.")
    elif EXCHANGE_MODE in ["ccxt", "binance"]:
        if not API_CONFIG.api_key or not API_CONFIG.api_secret:
            print_warning("API credentials not configured yet")
            print_info("They will be prompted when needed")
        else:
            print_success("API credentials configured successfully")


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
    """Place a MARKET order with interactive authentication."""
    bot = ctx.obj
    print_header(bot.mode)
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
            ['Mode', bot.mode.upper()],
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
@click.option(
    '--price',
    prompt='Price',
    type=float,
    help='Limit price'
)
@click.pass_context
def limit(ctx, symbol, side, quantity, price):
    """Place a LIMIT order with interactive authentication."""
    bot = ctx.obj
    print_header(bot.mode)
    print_info(f"Preparing {side} limit order...")
    
    try:
        bot = ctx.obj['bot']
        
        # Normalize symbol format based on mode
        if bot.mode in ['mock', 'ccxt']:
            if '/' not in symbol:
                if symbol.endswith('USDT'):
                    base = symbol[:-4]
                    symbol = f"{base}/USDT"
        else:
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
            ['Mode', bot.mode.upper()],
        ]
        print(tabulate(summary_data, tablefmt='grid'))
        
        # Confirm execution
        if not click.confirm(f"\n{Fore.YELLOW}Execute this order?", default=True):
            print_info("Order cancelled by user")
            return
        
        print(f"\n{Fore.CYAN}Executing order...")
        
        # Execute order based on mode
        if bot.mode == 'mock' or bot.mode == 'ccxt':
            response = bot.exchange.create_order(
                symbol=symbol,
                order_type='limit',
                side=side.lower(),
                amount=quantity,
                price=price
            )
            
            # Normalize response
            normalized_response = {
                'orderId': response.get('id', response.get('orderId', 'N/A')),
                'symbol': response.get('symbol', symbol),
                'side': response.get('side', side).upper(),
                'status': response.get('status', 'UNKNOWN').upper(),
                'quantity': response.get('amount', quantity),
                'executedQty': response.get('filled', 0),
                'avgPrice': response.get('average', 0),
                'cumulativeQuoteQty': response.get('cost', 0),
            }
            response = normalized_response
        else:
            response = bot.order_manager.place_limit_order(symbol, side, quantity, price)
        
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
        
        print_success(f"Limit order {response['orderId']} placed on {symbol}")
        logger.info(f"Limit order placed: {response['orderId']}")
    
    except (ValidationError, BinanceAPIError, CCXTAPIError) as e:
        print_error(f"Error: {str(e)}")
        logger.error(f"Order error: {str(e)}")


@cli.command()
@click.pass_context
def balance(ctx):
    """Check account balance."""
    bot = ctx.obj['bot']
    print_header(bot.mode)
    print_info("Fetching account balance...")
    
    try:
        bot = ctx.obj['bot']
        
        if bot.mode == 'mock' or bot.mode == 'ccxt':
            # Mock and CCXT use fetch_balance
            balance = bot.exchange.fetch_balance()
            
            # Extract USDT balance and other major currencies
            usdt_balance = balance.get('USDT', {})
            btc_balance = balance.get('BTC', {})
            eth_balance = balance.get('ETH', {})
            
            balance_data = [
                ['Asset', 'Free', 'Used', 'Total'],
                ['USDT', f"{usdt_balance.get('free', 0):.2f}", f"{usdt_balance.get('used', 0):.2f}", f"{usdt_balance.get('total', 0):.2f}"],
                ['BTC', f"{btc_balance.get('free', 0):.6f}", f"{btc_balance.get('used', 0):.6f}", f"{btc_balance.get('total', 0):.6f}"],
                ['ETH', f"{eth_balance.get('free', 0):.4f}", f"{eth_balance.get('used', 0):.4f}", f"{eth_balance.get('total', 0):.4f}"],
            ]
            
        else:
            # Binance mode uses client directly
            balance = bot.client.get_account_balance()
            
            # Filter for assets with non-zero balance
            assets_with_balance = [
                asset for asset in balance 
                if float(asset['balance']) > 0 or float(asset['availableBalance']) > 0
            ]
            
            balance_data = [['Asset', 'Balance', 'Available']]
            for asset in assets_with_balance:
                balance_data.append([
                    asset['asset'],
                    f"{float(asset['balance']):.8f}",
                    f"{float(asset['availableBalance']):.8f}"
                ])
        
        print(f"\n{Fore.CYAN}Account Balance:{Style.RESET_ALL}")
        print(tabulate(balance_data, headers='firstrow', tablefmt='grid'))
        
        print_success("Balance fetched successfully")
        
    except (BinanceAPIError, CCXTAPIError) as e:
        print_error(f"Error fetching balance: {str(e)}")
        logger.error(f"Balance error: {str(e)}")


@cli.command()
@click.pass_context
def test(ctx):
    """Test API connection and authentication."""
    bot = ctx.obj['bot']
    print_header(bot.mode)
    print_info("Testing API connection...")
    
    try:
        
        if bot.mode == 'mock':
            # Mock exchange always works
            print_success("Mock exchange connection successful!")
            print_info("Running in offline mode - No real API calls")
            
        elif bot.mode == 'ccxt':
            # Test CCXT connection
            markets = bot.exchange.fetch_markets()
            print_success(f"CCXT connection successful!")
            print_info(f"Available markets: {len(markets)}")
            
        elif bot.mode == 'binance':
            # Test Binance REST API connection
            server_time = bot.client.get_server_time()
            print_success(f"Binance API connection successful!")
            print_info(f"Server time: {server_time}")
        
        print_success("API test completed successfully!")
        
    except (BinanceAPIError, CCXTAPIError) as e:
        print_error(f"API test failed: {str(e)}")
        logger.error(f"API test error: {str(e)}")


if __name__ == '__main__':
    cli()