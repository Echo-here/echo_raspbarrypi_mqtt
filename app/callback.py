import serial
import json
import sys
import config as c

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("MQTT 브로커에 성공적으로 연결되었습니다!")
        client.subscribe(c.MQTT_COMMON_TOPIC)
        print(f"토픽 구독 시작: {c.MQTT_COMMON_TOPIC}")
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

        if "sugar" in data:
            print("JSON 데이터 파싱 완료 (디스펜서 명령):")
            for key, value in data.items():
                print(f"  {key}: {value}")
            print("---------------------------\n")

            value_to_send = str(data["sugar"])
            try:
                c.ser.write(value_to_send.encode())
                print(f"아두이노로 전송 완료 ('sugar' 값): '{value_to_send}'")
            except serial.SerialException as e:
                print(f"아두이노로 전송 실패: {e}")
        elif "light_sensor" in data:
            print("JSON 데이터 파싱 완료 (조도 센서 값 - 자체 발행):")
            print(f"  light_sensor: {data['light_sensor']}")
            print("---------------------------\n")
        else:
            print("오류: 알 수 없는 JSON 형식 또는 필수 키('sugar', 'light_sensor')가 없습니다.")

    except json.JSONDecodeError as e:
        print(f"오류: JSON 파싱 실패 - {e}")
        print(f"수신된 메시지가 올바른 JSON 형식이 아닙니다: '{raw_payload}'")
    except Exception as e:
        print(f"알 수 없는 오류 발생: {e}")