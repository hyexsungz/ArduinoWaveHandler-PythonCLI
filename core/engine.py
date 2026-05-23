import time
import threading

from core.constants import Constants
from core.app import CoreApp


class Engine:
    def __init__(self):
        self.constants = Constants()
        self.app = CoreApp()

        self.running = False
        self.thread = None

        self.loop_count = 0
        self.last_tick = 0

        self.performance = {
            "cycles_per_second": 0,
            "total_runtime": 0,
            "errors": 0
        }

    def _tick(self):
        self.last_tick = time.time()

    def loop(self):
        start_time = time.time()
        last_time = start_time

        while self.running:
            try:
                now = time.time()
                delta = now - last_time
                last_time = now

                self.loop_count += 1
                self._tick()

                if self.loop_count % 10 == 0:
                    self.performance["cycles_per_second"] = 10 / delta if delta > 0 else 0

                if not self.app.running:
                    self.app.start()

                time.sleep(0.1)

            except Exception:
                self.performance["errors"] += 1

        self.performance["total_runtime"] = time.time() - start_time

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.loop,
            daemon=True
        )

        self.thread.start()

    def stop(self):
        self.running = False
        self.app.stop()

    def restart(self):
        self.stop()
        time.sleep(1)
        self.start()

    def status(self):
        return {
            "running": self.running,
            "loops": self.loop_count,
            "performance": self.performance,
            "app": self.app.status()
        }

    def pretty_print(self):
        print("============================================================")
        print("               ARDUINOWAVEHANDLER ENGINE")
        print("============================================================")
        print("RUNNING     :", self.running)
        print("LOOPS       :", self.loop_count)
        print("CPS         :", self.performance["cycles_per_second"])
        print("RUNTIME     :", round(self.performance["total_runtime"], 2))
        print("ERRORS      :", self.performance["errors"])
        print("============================================================")
        print("APP STATUS")
        print(self.app.status())
        print("============================================================")

    def run_forever(self):
        self.start()

        try:
            while True:
                time.sleep(5)
                self.pretty_print()

        except KeyboardInterrupt:
            self.stop()
            print("\n[INFO] Engine stopped cleanly")


if __name__ == "__main__":
    engine = Engine()
    engine.run_forever()