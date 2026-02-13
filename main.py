#!/usr/bin/env python3
"""
Modern Trading Bot - Main Entry Point

A professional trading bot with multiple authentication options:
- Mock mode (offline, no API keys required)
- Interactive CLI authentication
- Environment variable support
- Configuration file support

No .env files required! Just run and trade.
"""
import sys
import os
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point for the Modern Trading Bot."""
    print("🤖 Modern Trading Bot - Starting...")
    print("=" * 50)

    try:
        from cli_modern import cli
        print("✓ Modern CLI loaded successfully")
        print("📋 Available commands: market, balance, test, info")
        print("💡 Tip: Run 'python main.py --help' for usage information")
        print("=" * 50)

        # Run the modern CLI
        cli()

    except ImportError:
        print("❌ Error: Modern CLI interface not found.")
        print("💡 Please ensure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())