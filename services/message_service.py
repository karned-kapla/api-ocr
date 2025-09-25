from typing import Any, Dict

from utils.kafka_util import KafkaProducer
from common_api.services.v0 import Logger
from models.message_model import Task

logger = Logger()

class MessageService:
    def __init__(self):
        self.producer = KafkaProducer()

    def send_task(self, topic: str, task: Task, payload: Dict[str, Any]):
        try:
            task_dict = task.model_dump()
            message_dict = {**task_dict, **payload}
            self.producer.send_message(topic=topic, message=message_dict)
            logger.info(f"Sent task for UUID {task.uuid} to topic {topic}")
        except Exception as e:
            logger.error(f"Error sending task: {e}")
            raise ValueError(f"Failed to send task: {e}")