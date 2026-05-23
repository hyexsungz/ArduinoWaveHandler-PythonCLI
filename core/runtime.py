import time
import threading
import traceback


class Runtime:
    def __init__(self, engine=None, app=None, watcher=None):
        self.engine = engine
        self.app = app
        self.watcher = watcher

        self.running = False
        self.thread = None

        self.start_time = 0
        self.tick_count = 0

        self.errors = []
        self.max_errors = 50

        self.metrics = {
            "uptime": 0,
            "ticks_per_second": 0,
            "last_tick": 0,
            "error_count": 0
        }

    def _tick(self):
        self.tick_count += 1
        self.metrics["last_tick"] = time.time()

    def _record_error(self, err):
        self.errors.append({
            "time": time.time(),
            "error": str(err),
            "trace": traceback.format_exc()
        })

        self.metrics["error_count"] += 1

        if len(self.errors) > self.max_errors:
            self.errors.pop(0)

    def loop(self):
        self.start_time = time.time()
        last_time = self.start_time
        tick_window = 0
        tick_counter = 0

        while self.running:
            try:
                now = time.time()
                delta = now - last_time
                last_time = now

                self._tick()

                tick_window += delta
                tick_counter += 1

                if tick_window >= 1.0:
                    self.metrics["ticks_per_second"] = tick_counter / tick_window
                    tick_window = 0
                    tick_counter = 0

                if self.engine and hasattr(self.engine, "start"):
                    if not getattr(self.engine, "running", False):
                        self.engine.start()

                if self.app and hasattr(self.app, "start"):
                    if not getattr(self.app, "running", False):
                        self.app.start()

                if self.watcher and hasattr(self.watcher, "start"):
                    if not getattr(self.watcher, "running", False):
                        self.watcher.start()

                time.sleep(0.05)

            except Exception as e:
                self._record_error(e)

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

        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

        if self.app:
            try:
                self.app.stop()
            except:
                pass

        if self.watcher:
            try:
                self.watcher.stop()
            except:
                pass

    def uptime(self):
        return time.time() - self.start_time

    def status(self):
        self.metrics["uptime"] = self.uptime()

        return {
            "running": self.running,
            "ticks": self.tick_count,
            "metrics": self.metrics,
            "active_errors": len(self.errors)
        }

    def get_errors(self):
        return self.errors

    def clear_errors(self):
        self.errors = []
        self.metrics["error_count"] = 0

    def pretty_print(self):
        print("============================================================")
        print("                 ARDUINOWAVEHANDLER RUNTIME")
        print("============================================================")
        print("RUNNING        :", self.running)
        print("UPTIME         :", round(self.uptime(), 2))
        print("TICKS          :", self.tick_count)
        print("TPS            :", self.metrics["ticks_per_second"])
        print("ERRORS         :", self.metrics["error_count"])
        print("============================================================")

        if self.errors:
            print("[RECENT ERROR]")
            print(self.errors[-1]["error"])
            print("============================================================")


if __name__ == "__main__":
    runtime = Runtime()
    runtime.start()

    try:
        while True:
            time.sleep(5)
            runtime.pretty_print()

    except KeyboardInterrupt:
        runtime.stop()
        print("\n[INFO] Runtime stopped")