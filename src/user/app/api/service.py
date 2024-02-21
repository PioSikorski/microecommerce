import logging
import time
from threading import Thread
from typing import Dict

import pika
import json
from sqlmodel import Session

from src.user.app.api.crud import crud
from src.user.app.deps import engine


class UserRabbitConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.thread = None
      
    def start(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='user')
        self.channel.basic_consume(queue='user', on_message_callback=self.on_request)
        self.thread = Thread(target=self._start_consuming)
        self.thread.start()

    def _start_consuming(self):
        try:
            self.channel.start_consuming()
        except Exception as e:
            logging.warning("Connection to RabbitMQ failed. Retrying in 5 seconds...")
            time.sleep(5)
            self._start_consuming()

    def stop(self):
        self.channel.stop_consuming()
        if self.thread is not None:
            self.thread.join()
        self.connection.close()
        
    def on_request(self, ch, method, props, body):
        order_data = json.loads(body)
        with Session(engine) as session:
            response = self.proccess_order(session, order_data)
            session.close()
            ch.basic_publish(exchange='',
                            routing_key=props.reply_to,
                            properties=pika.BasicProperties(correlation_id = \
                                                                props.correlation_id),
                            body=json.dumps(response))
            ch.basic_ack(delivery_tag = method.delivery_tag)

    def proccess_order(self, session, order_data: Dict) -> Dict:
        user_id = order_data.get("user_id")
        user_data = crud.get_user_orders(db=session, id=user_id)
        if not user_data:
            return {"status": "failed", "message": "User not found"}
        if user_data.orders_ids is None:
            user_data.orders_ids = set()
        user_data.orders_ids.add(order_data.get("order_id"))
        update_data = {"orders_ids": user_data.orders_ids}
        crud.update(db=session, db_obj=user_data, obj_in=update_data)
        return {"status": "success", "message": "Order add to user successfully"}


user_consumer = UserRabbitConsumer()