import platform

class Constants:
    APP_NAME = "ARDUINOWAVEHANDLER"
    VERSION = "1.0.0"

    PLATFORM = platform.system()

    SCAN_DELAY = 2
    WATCH_DELAY = 1
    AUTO_CONNECT_DELAY = 2
    HEARTBEAT_INTERVAL = 3

    MAX_BUFFER_SIZE = 4096

    TIMEOUT = 1

    BAUDRATES = [
        9600,
        19200,
        38400,
        57600,
        115200,
        230400,
        460800,
        921600
    ]

    DEVICE_KEYWORDS = [
        "arduino",
        "usb serial",
        "ch340",
        "cp210",
        "ftdi",
        "ttyusb",
        "ttyacm",
        "esp32",
        "esp8266",
        "stm32",
        "teensy",
        "nano",
        "uno",
        "mega",
        "leonardo",
        "micro"
    ]

    VIDPID_MAP = {
        "1a86": "CH340 (WCH)",
        "10c4": "Silicon Labs CP210x",
        "0403": "FTDI",
        "2341": "Arduino LLC",
        "2a03": "Arduino SA",
        "303a": "Espressif",
        "0483": "STMicroelectronics",
        "16c0": "Teensy (PJRC)"
    }

    FRAME_TYPES = {
        "DATA": 1,
        "BINARY": 2,
        "HANDSHAKE": 8,
        "HEARTBEAT": 9,
        "ERROR": 99
    }

    FLAGS = {
        "NONE": 0,
        "ENCRYPTED": 1,
        "COMPRESSED": 2,
        "ACK": 4
    }

    STATUS = {
        "DISCONNECTED": 0,
        "CONNECTED": 1,
        "AUTHENTICATED": 2,
        "ACTIVE": 3,
        "FAILED": 4
    }

    def dump(self):
        return {
            "APP_NAME": self.APP_NAME,
            "VERSION": self.VERSION,
            "PLATFORM": self.PLATFORM,
            "SCAN_DELAY": self.SCAN_DELAY,
            "WATCH_DELAY": self.WATCH_DELAY,
            "AUTO_CONNECT_DELAY": self.AUTO_CONNECT_DELAY,
            "HEARTBEAT_INTERVAL": self.HEARTBEAT_INTERVAL,
            "MAX_BUFFER_SIZE": self.MAX_BUFFER_SIZE
        }


if __name__ == "__main__":
    c = Constants()
    print(c.dump())