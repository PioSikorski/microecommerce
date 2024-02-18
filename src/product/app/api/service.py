from typing import Dict

import pika
import json
from sqlmodel import Session

from src.product.app.api.crud import product as crud
from src.product.app.deps import engine


class ProductRabbit:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='product')
        self.channel.basic_consume(queue='product', on_message_callback=self.on_request)
        

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
            

def start_product_rabbit():
    product_rabbit = ProductRabbit()
    product_rabbit.channel.start_consuming()