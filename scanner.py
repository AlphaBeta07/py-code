import serial
import webbrowser

# Open serial port (adjust ttyAMA0 or ttyS0 depending on Pi model)
ser = serial.Serial('/dev/serial0', 9600, timeout=1)

print("Ready to scan QR codes...")

while True:
    qr_data = ser.readline().decode('utf-8').strip()
    if qr_data:
        print("Scanned:", qr_data)
        try:
            # Extract only the ID if JSON is present
            if qr_data.startswith("{"):
                import json
                data = json.loads(qr_data)
                qr_id = data.get("id")
                if qr_id:
                    url = f"https://railfitqr.onrender.com/item/{qr_id}"
                    print("Opening:", url)
                    webbrowser.open(url)
            else:
                # Directly use scanned text as ID
                url = f"https://railfitqr.onrender.com/item/{qr_data}"
                print("Opening:", url)
                webbrowser.open(url)
        except Exception as e:
            print("Error:", e)
