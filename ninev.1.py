#pip install pyserial pylsl
import serial
from pylsl import StreamInlet, resolve_stream

# ตั้งค่าการเชื่อมต่อกับ Arduino (เปลี่ยน COM3 เป็นพอร์ตของ Arduino ที่ใช้)
arduino = serial.Serial('COM7', 9600)  # ตรวจสอบว่า Arduino ใช้พอร์ต COM อะไรบนระบบของคุณ

# ค้นหา LSL Stream ที่ส่งจาก OpenViBE
print("Looking for an SSVEP stream...")
streams = resolve_stream('name', 'eeg')

# เริ่มรับข้อมูลจาก LSL Stream
inlet = StreamInlet(streams[0])

while True:
    # รับข้อมูลจาก LSL Stream
    sample, timestamp = inlet.pull_sample()
    
    # ตัวอย่างค่า sample[0] เป็นความถี่ที่ตรวจจับได้จาก OpenViBE
    if sample[0] == 3:
        # ส่งคำสั่งไปยัง Arduino เพื่อเปิดไฟสีแดง (3 Hz)
        arduino.write(b'3')
        print("Detected 3 Hz - Red LED on")
        
    elif sample[0] == 5:
        # ส่งคำสั่งไปยัง Arduino เพื่อเปิดไฟสีเขียว (7 Hz)
        arduino.write(b'5')
        print("Detected 5 Hz - Green LED on")
        
    elif sample[0] == 9:
        # ส่งคำสั่งไปยัง Arduino เพื่อเปิดไฟสีน้ำเงิน (19 Hz)
        arduino.write(b'9')
        print("Detected 9 Hz - Blue LED on")
        
    else:
        # ส่งคำสั่งไปยัง Arduino เพื่อปิดไฟทุกสี
        arduino.write(b'0')
        print("No SSVEP detected - All LEDs off")
