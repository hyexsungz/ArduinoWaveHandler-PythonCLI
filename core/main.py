import time

from core.engine import Engine
from core.app import CoreApp
from detection.device_watcher import DeviceWatcher


class Main:
    def __init__(self):
        self.engine = Engine()
        self.app = CoreApp()
        self.watcher = DeviceWatcher()

        self.running = False

        self.boot_time = time.time()
        self.mode = "NORMAL"

    def boot(self):
        print("============================================================")
        print("                 ARDUINOWAVEHANDLER BOOT")
        print("============================================================")
        print("INITIALIZING ENGINE...")
        self.engine.start()

        print("INITIALIZING APP...")
        self.app.start()

        print("INITIALIZING DEVICE WATCHER...")
        self.watcher.start()

        self.running = True

        print("STATUS        : ONLINE")
        print("MODE          :", self.mode)
        print("BOOT TIME     :", self.boot_time)
        print("============================================================")

    def shutdown(self):
        print("\n[INFO] Shutting down system...")

        self.running = False

        self.engine.stop()
        self.app.stop()
        self.watcher.stop()

        print("[INFO] All systems stopped")

    def status(self):
        return {
            "running": self.running,
            "mode": self.mode,
            "uptime": time.time() - self.boot_time,
            "engine": self.engine.status(),
            "app": self.app.status(),
            "watcher": self.watcher.status()
        }

    def loop(self):
        while self.running:
            try:
                time.sleep(5)

                status = self.status()

                print("============================================================")
                print("                    SYSTEM STATUS")
                print("============================================================")
                print("UPTIME        :", round(status["uptime"], 2))
                print("ENGINE LOOPS  :", status["engine"]["loops"])
                print("DEVICES       :", status["app"]["stats"]["devices_seen"])
                print("ACTIVE PORTS  :", status["watcher"]["active_devices"])
                print("RUNNING       :", status["running"])
                print("============================================================")

            except Exception:
                pass

    def run(self):
        self.boot()

        try:
            self.loop()

        except KeyboardInterrupt:
            self.shutdown()
            print("[INFO] System exited safely")


if __name__ == "__main__":
    main = Main()
    main.run()