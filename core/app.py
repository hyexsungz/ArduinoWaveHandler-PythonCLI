import time
import threading

from detection.serial_scanner import SerialScanner
from detection.arduino_scanner import ArduinoScanner
from detection.usb_scanner import USBScanner
from detection.device_watcher import DeviceWatcher
from detection.device_verifier import DeviceVerifier
from detection.port_identifier import PortIdentifier
from detection.vidpid import VIDPIDScanner
from detection.auto_connect import AutoConnect

class CoreApp:
    def __init__(self):
        self.running = False
        self.thread = None

        self.serial_scanner = SerialScanner()
        self.arduino_scanner = ArduinoScanner()
        self.usb_scanner = USBScanner()
        self.device_watcher = DeviceWatcher()
        self.device_verifier = DeviceVerifier()
        self.port_identifier = PortIdentifier()
        self.vidpid_scanner = VIDPIDScanner()
        self.auto_connect = AutoConnect()

        self.cycle_delay = 2

        self.stats = {
            "cycles": 0,
            "devices_seen": 0,
            "errors": 0
        }

    def cycle(self):
        while self.running:
            try:
                self.stats["cycles"] += 1

                serial_devices = self.serial_scanner.scan()
                arduino_devices = self.arduino_scanner.scan()
                usb_devices = self.usb_scanner.scan()
                vidpid_devices = self.vidpid_scanner.scan()

                verified = self.device_verifier.scan()
                identified = self.port_identifier.scan()

                if serial_devices:
                    self.stats["devices_seen"] += len(serial_devices)

                if arduino_devices:
                    self.stats["devices_seen"] += len(arduino_devices)

                if usb_devices:
                    self.stats["devices_seen"] += len(usb_devices)

                if vidpid_devices:
                    self.stats["devices_seen"] += len(vidpid_devices)

                if not self.auto_connect.connection:
                    self.auto_connect.auto_connect()

                time.sleep(self.cycle_delay)

            except Exception:
                self.stats["errors"] += 1

    def start(self):
        if self.running:
            return

        self.running = True

        self.device_watcher.start()

        self.thread = threading.Thread(
            target=self.cycle,
            daemon=True
        )

        self.thread.start()

    def stop(self):
        self.running = False
        self.device_watcher.stop()
        self.auto_connect.stop()

    def status(self):
        return {
            "running": self.running,
            "stats": self.stats,
            "auto_connect": self.auto_connect.status(),
            "watcher": self.device_watcher.status()
        }

    def pretty_print(self):
        print("============================================================")
        print("               ARDUINOWAVEHANDLER CORE APP")
        print("============================================================")
        print("RUNNING     :", self.running)
        print("CYCLES      :", self.stats["cycles"])
        print("DEVICES     :", self.stats["devices_seen"])
        print("ERRORS      :", self.stats["errors"])
        print("AUTO PORT   :", self.auto_connect.connected_port)
        print("WATCHER     :", self.device_watcher.status()["active_devices"])
        print("============================================================")

    def run_forever(self):
        self.start()

        try:
            while True:
                time.sleep(5)
                self.pretty_print()

        except KeyboardInterrupt:
            self.stop()
            print("\n[INFO] Core stopped")


if __name__ == "__main__":
    app = CoreApp()
    app.run_forever()