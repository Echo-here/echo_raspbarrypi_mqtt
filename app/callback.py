# callback.py
import serial
import json
import sys
import config as c

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("MQTT 브로커에 성공적으로 연결되었습니다!")
        # 구독 토픽을 새로운 명세에 맞게 변경
        client.subscribe(c.MQTT_ORDER_TOPIC)
        print(f"토픽 구독 시작: {c.MQTT_ORDER_TOPIC}")
    else:
        print(f"MQTT 브로커 연결 실패, 에러 코드: {reason_code}")
        if c.ser and c.ser.is_open:
            c.ser.close()
        sys.exit(1)

def on_message(client, userdata, msg):
    raw_payload = msg.payload.decode().strip()
    print(f"\n--- MQTT 메시지 수신 ---")
    print(f"토픽: {msg.topic}")
    print(f"원본 메시지: '{raw_payload}'")
    print(f"---------------------------\n")

    try:
        data = json.loads(raw_payload)
        print("받아짐")
        # 수신된 JSON 데이터에 있는 모든 항목을 순회하며 아두이노로 명령 전송
        for ingredient, value in data.items():
            command_prefix = None
            
            # 각 재료에 맞는 시리얼 명령 접두사 설정
            if ingredient == "sugar":
                command_prefix = "S"
            elif ingredient == "water":
                command_prefix = "W"
            elif ingredient == "coffee":
                command_prefix = "C"
            elif ingredient == "icetea":
                command_prefix = "I"
            elif ingredient == "greentea":
                command_prefix = "G"

            if command_prefix:
                command_to_send = f"{command_prefix}{value}"
                print(f"아두이노로 전송할 명령: '{command_to_send}'")
                
                try:
                    c.ser.write(command_to_send.encode())
                    print(f"아두이노로 전송 완료 ('{ingredient}' 값): '{command_to_send}'")
                    # 아두이노의 응답을 기다리는 로직을 추가할 수도 있음 (선택 사항)
                except serial.SerialException as e:
                    print(f"아두이노로 전송 실패: {e}")
            else:
                print(f"경고: 알 수 없는 재료 '{ingredient}'입니다. 명령을 건너뜁니다.")

    except json.JSONDecodeError as e:
        print(f"오류: JSON 파싱 실패 - {e}")
        print(f"수신된 메시지가 올바른 JSON 형식이 아닙니다: '{raw_payload}'")
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")