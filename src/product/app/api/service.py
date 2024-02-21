import logging
import time
from threading import Thread
from typing import Dict

import pika
import json
from sqlmodel import Session

from src.product.app.api.crud import crud
from src.product.app.deps import engine


class ProductRabbitConsumer:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.thread = None
        
    def start(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='product')
        self.channel.basic_consume(queue='product', on_message_callback=self.on_request)
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
        for product in order_data:
            product_id = product.get("product_id")
            db_product = crud.get(db=session, id=product_id)
            product_quantity = product.get("quantity")
            if not db_product:
                return {"status": "failed", "message": "Product not found"}
            if db_product.quantity < product_quantity:
                return {"status": "failed", "message": "Product not available"}
            quantity = db_product.quantity - product_quantity
            update_data = {"quantity": quantity}
            crud.update(db=session, db_obj=db_product, obj_in=update_data)
        return {"status": "success", "message": "Products updated successfully"}

    
product_consumer = ProductRabbitConsumer()