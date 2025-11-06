# main.py
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
            arduino_data_raw = c.ser.readline().decode('utf-8').strip()
            
            if arduino_data_raw:
                print(f"아두이노로부터 시리얼 수신: {arduino_data_raw}")

                try:
                    # 아두이노에서 보낸 JSON 데이터 파싱
                    arduino_data = json.loads(arduino_data_raw)
                    print(f"파싱된 아두이노 JSON: {arduino_data}")
                    
                    # 변경된 부분: 전체 데이터를 'stock' 토픽으로 한 번에 발행
                    publish_topic = "stock/topic"
                    
                    # 전체 JSON 객체를 페이로드로 사용
                    client.publish(publish_topic, json.dumps(arduino_data))
                    print(f"MQTT 발행 완료: 토픽='{publish_topic}', 값='{json.dumps(arduino_data)}'")
                   
                except json.JSONDecodeError as e:
                    print(f"오류: 수신된 데이터가 올바른 JSON 형식이 아닙니다: {e}")
                except Exception as e:
                    print(f"아두이노 데이터 처리 중 오류 발생: {e}")
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