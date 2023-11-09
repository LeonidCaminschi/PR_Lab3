#!/usr/bin/env python
import pika
from homework import analyzeproduct
import concurrent.futures
import signal
import sys
from tinydb import TinyDB 
import threading

db = TinyDB('database.json')
db_lock = threading.Lock()

def save_to_db(body, attr):
    with db_lock:
        db.insert({'body': body, 'attr': attr})

def consumer(name):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='logs', exchange_type='fanout')

    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue

    channel.queue_bind(exchange='logs', queue=queue_name)

    print(f'{name} Waiting for logs. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(f"{name} Received {body.decode()}")
        attr = analyzeproduct(f'{body.decode()}')
        save_to_db(body.decode(), attr)
        print(f"{name} Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

    channel.start_consuming()

def handler(signum, frame):
    print("Exiting program now :)")
    pool.shutdown(wait=False)
    sys.exit(1)

signal.signal(signal.SIGINT, handler)

consumers = int(input("Please input the number of consumers: "))

pool = concurrent.futures.ThreadPoolExecutor(max_workers=consumers)

for i in range(0, consumers):
    pool.submit(consumer, f"[Thread {i+1}]")

while 1:
    pass


