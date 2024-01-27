# docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management


import pika
from faker import Faker
from models import Contact
import connect

NO_OF_CONTACTS = 3

fake = Faker()


def generate_fake_contacts(no_of_contacts):
    for _ in range(no_of_contacts):
        fake_contact = Contact(fullname=fake.name(), email=fake.email())
        fake_contact.save()


def add_to_rabbitmq():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    contacts_to_send = Contact.objects(message_sent=False)
    contacts_id = [contact.id for contact in contacts_to_send]

    channel.queue_declare(queue='contacts_id')
    for id in contacts_id:
        channel.basic_publish(exchange='', routing_key='contacts_id', body=str(id).encode())
        print(f" [x] Sent contact_id: {id}")
    connection.close()


if __name__ == '__main__':
    generate_fake_contacts(NO_OF_CONTACTS)
    add_to_rabbitmq()
