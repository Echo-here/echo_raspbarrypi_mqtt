import os
import configparser

ser = None

# 설정 파일 경로 (app 폴더 기준으로 한 단계 위)
config_path = os.path.join(os.path.dirname(__file__), "..", "default.conf")

config = configparser.ConfigParser()
config.read(config_path)

# --- 시리얼 설정 ---
SERIAL_PORT = config["serial"]["port"]
BAUD_RATE = int(config["serial"]["baud_rate"])

# --- MQTT 설정 ---
BROKER_ADDRESS = config["mqtt"]["broker_address"]
BROKER_PORT = int(config["mqtt"]["broker_port"])
# MQTT 토픽 정의
MQTT_ORDER_TOPIC = "order/topic"