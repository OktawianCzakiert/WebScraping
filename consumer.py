import pika
import sys
import connect
from models import Contact

def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='contacts_id')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        _id = body.decode()
        contact_to_update = Contact.objects(id=_id)
        contact_to_update.update(message_sent=True)


    channel.basic_consume(queue='contacts_id', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
