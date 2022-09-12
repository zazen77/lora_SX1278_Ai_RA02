[
    {
        "id": "ffe84c4d311299e9",
        "type": "tab",
        "label": "Flow 1",
        "disabled": false,
        "info": "",
        "env": []
    },
    {
        "id": "3e4b8a6e9bdd4591",
        "type": "debug",
        "z": "ffe84c4d311299e9",
        "name": "debug 1",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "true",
        "targetType": "full",
        "statusVal": "",
        "statusType": "auto",
        "x": 380,
        "y": 80,
        "wires": []
    },
    {
        "id": "733d3a6e0b3bde57",
        "type": "python3-function",
        "z": "ffe84c4d311299e9",
        "name": "",
        "func": "from SX127x.LoRaArgumentParser import LoRaArgumentParser\nimport sys\nfrom time import sleep\nimport RPi.GPIO as GPIO\nfrom SX127x.LoRa import LoRa, LoRa2\nfrom SX127x.constants import MODE, BW, CODING_RATE, GAIN, PA_SELECT, PA_RAMP, MASK\nfrom SX127x.board_config import BOARD, BOARD2\n\nBOARD.setup()\n\nparser = LoRaArgumentParser(\"A simple LoRa beacon\")\nparser.add_argument('--single', '-S', dest='single', default=False, action=\"store_true\", help=\"Single transmission\")\nparser.add_argument('--wait', '-w', dest='wait', default=1, action=\"store\", type=float, help=\"Waiting time between transmissions (default is 0s)\")\n\n\nclass LoRaBeacon(LoRa):\n    counter = msg['payload']\n    def __init__(self, verbose=False):\n        super(LoRaBeacon, self).__init__(verbose)\n        self.set_mode(MODE.SLEEP)\n        self.set_dio_mapping([1,0,0,0,0,0])\n\n    def on_tx_done(self):\n        global counter\n        self.set_mode(MODE.STDBY)\n        self.clear_irq_flags(TxDone=1)\n        self.counter =msg['payload']\n        sys.stdout.flush()\n        #if args.single:\n            #sys.exit(0)\n        #sleep(args.wait)\n        \n        #data=input(msg['payload'])\n        sleep(2)\n        data=self.counter\n        a=[int(hex(ord(m)), 0) for m in data]\n        #print(a)\n        self.write_payload(a)\n        #print(self.write_payload(a))\n        self.set_mode(MODE.TX)\n        return msg;\n\n    def start(self):\n        global counter\n        self.write_payload([])\n        self.counter=msg['payload']\n        self.set_mode(MODE.TX)\n        while True:\n            sleep(1)\n\nlora = LoRaBeacon(verbose=False)\nargs = parser.parse_args(lora)\n\nlora.set_pa_config(pa_select=1)\n#lora.set_rx_crc(True)\n#lora.set_agc_auto_on(True)\n#lora.set_lna_gain(GAIN.NOT_USED)\n#lora.set_coding_rate(CODING_RATE.CR4_6)\n#lora.set_implicit_header_mode(False)\n#lora.set_pa_config(max_power=0x04, output_power=0x0F)\n#lora.set_pa_config(max_power=0x04, output_power=0b01000000)\n#lora.set_low_data_rate_optim(True)\n#lora.set_pa_ramp(PA_RAMP.RAMP_50_us)\n\n\n#print(lora)\n#assert(lora.get_lna()['lna_gain'] == GAIN.NOT_USED)\nassert(lora.get_agc_auto_on() == 1)\n\n#print(\"Beacon config:\")\n#print(\"  Wait %f s\" % args.wait)\n#print(\"  Single tx = %s\" % args.single)\n#print(\"\")\n#try: input(\"Press enter to start...\")\ntry: sleep(0.001)\nexcept: pass\n\ntry:\n    lora.start()\n    return msg;\nexcept KeyboardInterrupt:\n    sys.stdout.flush()\n    #print(\"\")\n    sys.stderr.write(\"KeyboardInterrupt\\n\")\nfinally:\n    sys.stdout.flush()\n    #print(\"\")\n    lora.set_mode(MODE.SLEEP)\n    #print(lora)\n    return msg;\n    BOARD.teardown()\nreturn msg;\n",
        "outputs": 1,
        "x": 190,
        "y": 200,
        "wires": [
            [
                "3e4b8a6e9bdd4591"
            ]
        ]
    },
    {
        "id": "a7b4ad5bac9ee3d2",
        "type": "inject",
        "z": "ffe84c4d311299e9",
        "name": "",
        "props": [
            {
                "p": "payload"
            },
            {
                "p": "topic",
                "vt": "str"
            }
        ],
        "repeat": "",
        "crontab": "",
        "once": false,
        "onceDelay": 0.1,
        "topic": "",
        "payload": "11",
        "payloadType": "str",
        "x": 110,
        "y": 80,
        "wires": [
            [
                "733d3a6e0b3bde57"
            ]
        ]
    }
]
