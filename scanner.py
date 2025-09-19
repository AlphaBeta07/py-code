import serial
import webbrowser
import json
import sys

# ---------------------------
# Configure your serial port
# ---------------------------
# Try one of these if /dev/serial0 does not work:
#   /dev/ttyS0
#   /dev/ttyAMA0
#   /dev/ttyUSB0
PORT = "/dev/serial0"
BAUD = 9600   # default for most Waveshare scanners (try 115200 if not working)

try:
    ser = serial.Serial(PORT, BAUD, timeout=1)
except Exception as e:
    print(f"❌ Could not open serial port {PORT}: {e}")
    sys.exit(1)

print(f"✅ Listening on {PORT} at {BAUD} baud")
print("📷 Ready to scan QR codes...")

while True:
    try:
        # Read raw bytes from scanner
        raw = ser.readline()
        if not raw:
            continue

        # Decode safely
        qr_data = raw.decode("utf-8", errors="ignore").strip()
        if not qr_data:
            continue

        print("🔍 Scanned:", qr_data)

        # Check if JSON data
        if qr_data.startswith("{") and qr_data.endswith("}"):
            try:
                data = json.loads(qr_data)
                qr_id = data.get("id")
                if qr_id:
                    url = f"https://railfitqr.onrender.com/item/{qr_id}"
                    print("🌐 Opening:", url)
                    webbrowser.open(url)
                else:
                    print("⚠️ No 'id' field found in QR JSON")
            except Exception as e:
                print("⚠️ JSON parse error:", e)

        else:
            # If QR is plain text, just append to URL
            url = f"https://railfitqr.onrender.com/item/{qr_data}"
            print("🌐 Opening:", url)
            webbrowser.open(url)

    except KeyboardInterrupt:
        print("\n👋 Exiting...")
        break
    except Exception as e:
        print("⚠️ Error reading QR:", e)
