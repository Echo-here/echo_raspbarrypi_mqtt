import serial
import time
import sys
import config as c
def connect_by_arduino(SERIAL_PORT, BAUD_RATE = 9600):
    try:
        c.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        print(f"Arduino에 시리얼 연결 성공: {SERIAL_PORT}")
    except serial.SerialException as e:
        print(f"시리얼 연결 실패: {e}")
        sys.exit(1)
def connect_by_mqtt(client):
    try:
        print(f"MQTT 브로커 '{c.BROKER_ADDRESS}:{c.BROKER_PORT}'에 연결 시도 중...")
        client.connect(c.BROKER_ADDRESS, c.BROKER_PORT, 60)
    except Exception as e:
        print(f"MQTT 연결 실패: {e}")
        if c.ser and c.ser.is_open:
            c.ser.close()
        sys.exit(1)