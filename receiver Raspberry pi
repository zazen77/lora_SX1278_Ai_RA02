import sys 
from time import sleep
from SX127x.LoRa import *
from SX127x.board_config import BOARD
# import the python libraries
BOARD.setup()
# is used to set the board and LoRa parameters

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        # sleep to save power
        self.set_dio_mapping([0,0,0,0,0,0])
        # go to this https://cdn-shop.adafruit.com/product-files/3179/sx1276_77_78_79.pdf
    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(.5)
        rssi_value = self.get_rssi_value()
        status = self.get_modem_status()
        #configure the RSSI (Receiving signal strength Indicator), status, operating frequency etc.
        sys.stdout.flush()
     
    def on_rx_done(self):
        self.clear_irq_flags(RxDone=1)
        payload = self.read_payload(nocheck=True)
        data = ''.join([chr(c) for c in payload])
        print(data)
        # get executed data after the incoming packet is read
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        
lora = LoRaRcvCont(verbose=False)

lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)


assert(lora.get_agc_auto_on() == 1)

try: 
    lora.start()
    sys.stdout.flush()
    sys.stderr.write("KeyboardInterrupt\n")
#print the received values on the console and terminate the program using a keyboard interrupt
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()

