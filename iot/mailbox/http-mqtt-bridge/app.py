import os
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel
import paho.mqtt.client as mqtt
from collections import deque

MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "set_a_topic_fool")

app = FastAPI()
messages = deque(maxlen=100)

client = mqtt.Client()

def on_message(client, userdata, msg):
    messages.append({
        "topic": msg.topic,
        "payload": msg.payload.decode(errors="replace")
    })
    print("Received message:", msg.payload.decode(errors="replace"))

client.on_message = on_message

@app.on_event("startup")
async def startup():
    # run paho loop in a background thread
    def loop():
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.subscribe(MQTT_TOPIC)
        client.loop_forever()
    asyncio.get_running_loop().run_in_executor(None, loop)

@app.get("/messages")
async def get_messages(limit: int = 20):
    return list(messages)[-limit:]

@app.get("/send")
async def send(topic:str = MQTT_TOPIC, msg: str | None = None):
    if msg is None:
        return {"error": "msg parameter is required"}
    client.publish(topic, msg)
    return {"published": True, "topic": topic, "msg": msg}

class Msg(BaseModel):
    message: str
    topic: str | None = None

@app.post("/publish")
async def publish(msg: Msg):
    topic = msg.topic or MQTT_TOPIC
    client.publish(topic, msg.message)
    return {"published": True, "topic": topic}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
