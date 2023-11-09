#!/usr/bin/env python
import pika
import sys
from in_class import webcrawl

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')
links = webcrawl("https://999.md/ro/list/computers-and-office-equipment/laptops")

for link in links:
    channel.basic_publish(
        exchange='logs',
        routing_key='',
        body=link,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )
    print(f" Link Sent: {link}")
connection.close()