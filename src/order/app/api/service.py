import pika
import uuid
import json
from bson import ObjectId


class OrderCreatedClient:
    def __init__(self, host, queue):
        self.host = host
        self.queue = queue
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()
        
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)
        
        self.response = None
        self.corr_id = None
        
    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
        
    def call(self, order_data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(order_data)
        )
        
        self.connection.process_data_events(time_limit=None)
        return json.loads(self.response)


orderproduct_rpc = OrderCreatedClient('rabbitmq', 'product')
orderuser_rpc = OrderCreatedClient('rabbitmq', 'user')