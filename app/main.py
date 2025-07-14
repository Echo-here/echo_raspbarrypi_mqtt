import os
import paho.mqtt.client as mqtt
import serial
import time
import sys
import json
from connect import connect_by_arduino, connect_by_mqtt
from callback import on_connect, on_message
import config as c

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

connect_by_arduino(c.SERIAL_PORT)
connect_by_mqtt(client)

client.loop_start()

print("MQTT 메시지 수신/발신 대기 중입니다. 프로그램을 종료하려면 Ctrl+C를 누르세요.")

try:
    while True:
        if c.ser.in_waiting > 0:
            arduino_data = c.ser.readline().decode('utf-8').strip()
            if arduino_data:
                print(f"아두이노로부터 시리얼 수신: {arduino_data}")

                try:
                    light_value = None

                    if arduino_data.startswith("CDS: "):
                        light_value = int(arduino_data.replace("CDS: ", ""))
                        print(f"파싱된 조도 아날로그 값: {light_value}")
                    elif arduino_data.startswith("조도 센서 상태: "):
                        light_value = arduino_data.replace("조도 센서 상태: ", "")
                        print(f"파싱된 조도 디지털 상태: {light_value}")

                    if light_value is not None:
                        light_sensor_json = {"light_sensor": light_value}
                        client.publish(c.MQTT_COMMON_TOPIC, json.dumps(light_sensor_json))
                        print(f"MQTT 발행 완료 (조도 센서): 토픽='{c.MQTT_COMMON_TOPIC}', 값='{json.dumps(light_sensor_json)}'")
                    else:
                        print(f"오류: 알 수 없는 아두이노 시리얼 데이터 형식 (발행하지 않음): {arduino_data}")

                except ValueError:
                    print(f"오류: 조도 센서 값이 숫자로 변환할 수 없습니다: '{arduino_data}'")
                except Exception as e:
                    print(f"조도 센서 값 처리 중 오류 발생: {e}")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n프로그램 종료 요청 감지. 연결을 해제합니다...")
finally:
    if client:
        client.loop_stop()
        client.disconnect()
        print("MQTT 클라이언트 연결 해제 완료.")
    if c.ser and c.ser.is_open:
        c.ser.close()
        print("아두이노 시리얼 포트 닫기 완료.")
    print("프로그램이 종료되었습니다.")
