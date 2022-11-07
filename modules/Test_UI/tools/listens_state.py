import random
import time
from threading import Thread
from paho.mqtt import client as mqtt_client


class ListensState:
    def __init__(self):
        '初始默认数值等等,获取工作路径'
        self.broker = 'broker.emqx.io'
        self.port = 1883
        self.topic = "python/mqtt/wbl"
        self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.username = 'emqx'
        self.password = '**********'
        self.state = 0
        self.data_state = 0

    def connect_mqtt(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                pass
                # print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(self.client_id)
        client.username_pw_set(self.username, self.password)
        client.on_connect = on_connect
        client.connect(self.broker, self.port)
        return client

    def publish(self, client):
        msg = 0  # 初始数值
        while True:
            time.sleep(1)
            result = client.publish(self.topic, msg, qos=2)
            # result: [0, 1]  成功或失败状态捕获
            status = result[0]
            if status == 0:
                print(msg)
            else:
                print(f"Failed to send message to topic {self.topic}")
            msg = self.data_state

    # def publish(self, client):
    #     msg = 0  # 初始数值
    #     result = client.publish(self.topic, msg, qos=2)
    #     # result: [0, 1]  成功或失败状态捕获
    #     status = result[0]
    #     if status == 0:
    #         print(msg)
    #     else:
    #         print(f"Failed to send message to topic {self.topic}")
    #     msg = self.data_state

    def updata_out_run(self):
        client = self.connect_mqtt()
        client.loop_start()
        self.publish(client)

    def out_run(self):
        tt = Thread(target=self.updata_out_run())
        tt.start()

    # 订阅消息
    def subscribe(self, client: mqtt_client):
        def on_message(client, userdata, msg):
            # return
            print(msg.payload.decode())
            self.state = int(msg.payload.decode())

        client.subscribe(self.topic)
        client.on_message = on_message

    def updata_into_run(self):
        client = self.connect_mqtt()
        self.subscribe(client)
        client.loop_forever()

    def into_run(self):
        t1 = Thread(target=self.updata_into_run)
        t1.start()
