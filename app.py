import os
import pika
import logging
from bson import ObjectId
from environs import Env
from mongoengine import connect, disconnect
from imagenetviewer.image import Image, ImageStatus
from inference import TritonImageNetClassifierModel


def on_request(ch, method, props, body):
    image_object_id = ObjectId(body.decode())
    image = Image.objects.get(pk=image_object_id)

    score, label_num, label = triton.inference(triton.preprocessing(image.get_pil_image()))
    #logger.debug(f'{image_object_id} recognized as {label} ({label_num}) with score {score}')

    if score >= env.float('SUCCESS_SCORE_THRESHOLD'):
        image.label = label
        image.status = ImageStatus.CLASSIFIED
        image.save()

        # ch.basic_publish(
        #     exchange='',
        #     routing_key=env('OUTPUT_SUCCESS_QUEUE'),
        #     body=str(image_object_id)
        # )
        #logger.info(f'[+] {image_object_id} recognized as {label}')
    else:
        image.status = ImageStatus.PENDING_ENCODING
        image.save()
        
        ch.basic_publish(
            exchange='',
            routing_key=env('OUTPUT_FAILURE_QUEUE'),
            body=str(image_object_id)
        )
        logger.info(f'[x] failed to classify {image_object_id}')
    ch.basic_ack(delivery_tag=method.delivery_tag)



if __name__ == '__main__':
    logger = logging.getLogger('imagenet-classifier')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s %(name)s %(levelname)s] %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    env = Env()
    env.read_env()

    triton = TritonImageNetClassifierModel(env('TRITON_HOST'), env('MODEL_NAME'))

    connect(host=env('MONGODB_HOST'), uuidRepresentation='standard')

    con_par = pika.ConnectionParameters(
        heartbeat=600,
        blocked_connection_timeout=300,
        host=env('RABBITMQ_HOST')
    )
    connection = pika.BlockingConnection(con_par)
    channel = connection.channel()

    channel.queue_declare(queue=env('INPUT_QUEUE'), durable=True)
    channel.queue_declare(queue=env('OUTPUT_SUCCESS_QUEUE'), durable=True)
    channel.queue_declare(queue=env('OUTPUT_FAILURE_QUEUE'), durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=env('INPUT_QUEUE'), on_message_callback=on_request)

    logger.info('[+] awaiting images to recognize')
    channel.start_consuming()




