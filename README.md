# ArduinoWaveHandler

ArduinoWaveHandler is a modular Python-based hardware monitoring and runtime utility framework focused on live USB/COM device tracking, logging, parsing, and real-time terminal monitoring.

The project is designed around a layered architecture where utility modules operate independently while sharing a unified runtime environment.

---

# Features

- Live USB and COM monitoring
- Real-time terminal device engine
- Disconnect and reconnect tracking
- File utility abstraction layer
- Multi-level logging system
- Parsing and encoding toolkit
- String processing utilities
- Time and stopwatch engine
- Modular build system
- Threaded monitoring runtime
- Configurable runtime settings
- JSON-based configuration layer

---

# Live Monitoring Engine

The monitoring engine continuously scans connected hardware devices and tracks:

- COM ports
- USB serial adapters
- CH340 devices
- CP210x devices
- FTDI adapters
- Runtime device changes

The terminal stays active while scanning and updates in real-time.

Example:

```text id="live01"
ArduinoWaveHandler LIVE DEVICE ENGINE
TIME 21:38:18
UPTIME 110s
SCAN 94
EVENT STABLE LINK

DEVICES
COMM
COM3
CH340 USB SERIAL

# ARDUINOWAVEHANDLER

A real-time Arduino / USB serial detection and signal processing framework.

---

## ⚙️ Requirements

Install dependencies first:

```bash
pip install pyserial
```

---

## 🚀 How to Run

### Start full system (recommended)

```bash
python main.py
```

---

### Run core engine only

```bash
python -m core.engine
```

---

### Run runtime controller

```bash
python -m core.runtime
```

---

### Run individual scanners

```bash
python -c "from detection.serial_scanner import SerialScanner; SerialScanner().pretty_print()"
python -c "from detection.usb_scanner import USBScanner; USBScanner().pretty_print()"
python -c "from detection.vidpid import VIDPIDScanner; VIDPIDScanner().pretty_print()"
```

---

## 📡 What it does

* Detects Arduino / ESP / STM32 / Teensy boards
* Scans USB + Serial ports in real-time
* Identifies VID/PID + device fingerprints
* Matches signal waveforms
* Auto-connects to best available device
* Runs continuous runtime engine loop

---

## 🛑 Stop system

Press:

```
CTRL + C
```

---

## 📁 Project Entry Point

```
main.py
```

---

## ⚠️ Notes

* Requires USB serial drivers (CH340 / CP210x / FTDI depending on board)
* Works best with real connected hardware
* Some modules simulate signals if no device is connected
