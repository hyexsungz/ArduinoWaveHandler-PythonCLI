import time
import platform
import hashlib


class Version:
    def __init__(self):
        self.name = "ARDUINOWAVEHANDLER"
        self.major = 1
        self.minor = 0
        self.patch = 0

        self.build = int(time.time())

        self.platform = platform.system()

        self.commit_hash = self._generate_hash()

        self.changelog = [
            {
                "version": "1.0.0",
                "date": self.build,
                "notes": [
                    "Initial core system",
                    "Device scanning engine",
                    "Serial monitoring layer",
                    "Signal processing module",
                    "Auto-connect system"
                ]
            }
        ]

    def _generate_hash(self):
        base = f"{self.name}-{self.major}.{self.minor}.{self.patch}-{time.time()}"
        return hashlib.sha256(base.encode()).hexdigest()[:12]

    def version_string(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    def full(self):
        return {
            "name": self.name,
            "version": self.version_string(),
            "build": self.build,
            "platform": self.platform,
            "commit": self.commit_hash
        }

    def bump_major(self):
        self.major += 1
        self.minor = 0
        self.patch = 0
        self.build = int(time.time())
        self.commit_hash = self._generate_hash()

    def bump_minor(self):
        self.minor += 1
        self.patch = 0
        self.build = int(time.time())
        self.commit_hash = self._generate_hash()

    def bump_patch(self):
        self.patch += 1
        self.build = int(time.time())
        self.commit_hash = self._generate_hash()

    def add_changelog(self, notes):
        self.changelog.append({
            "version": self.version_string(),
            "date": int(time.time()),
            "notes": notes if isinstance(notes, list) else [notes]
        })

    def latest_changelog(self):
        return self.changelog[-1] if self.changelog else None

    def pretty_print(self):
        print("============================================================")
        print("                 ARDUINOWAVEHANDLER VERSION")
        print("============================================================")
        print("NAME       :", self.name)
        print("VERSION    :", self.version_string())
        print("BUILD      :", self.build)
        print("PLATFORM   :", self.platform)
        print("COMMIT     :", self.commit_hash)
        print("============================================================")

        if self.changelog:
            print("[CHANGELOG]")
            for entry in self.changelog[-3:]:
                print("")
                print("VERSION :", entry["version"])
                for note in entry["notes"]:
                    print("-", note)

        print("============================================================")


if __name__ == "__main__":
    v = Version()
    v.pretty_print()