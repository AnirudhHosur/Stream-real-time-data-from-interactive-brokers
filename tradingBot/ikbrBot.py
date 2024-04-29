from ibapi.client import EClient
from ibapi.wrapper import EWrapper
# Stream data imports
from ibapi.contract import Contract
from ibapi.order import *
import threading
import time

# Class for IBKR connection
class IBAPI(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    # Listen for real time bars
    def realtimeBar(self, reqId, time, open, high, low, close, vlume, wap, count):
        bot.on_bar_update(reqId, time, open, high, low, close, vlume, wap, count)

# Bot Logic
class Bot():
    ib = None
    def __init__(self):
        # Connect to IB on init
        self.ib = IBAPI()
        self.ib.connect("127.0.0.1", 7496, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)

        # Get Symbol info
        symbol = input("Enter the symbol you want to trade: ")
        # Create IB contract object
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"

        # Reqeuest real time data
        self.ib.reqRealTimeBars(0, contract, 5, "TRADES", 1, [])

    def run_loop(self):
        # Separate thread
        self.ib.run()

    def on_bar_update(self, reqId, time, open, high, low, close, vlume, wap, count):
        print(reqId)

# Start Bot
bot = Bot()
        
