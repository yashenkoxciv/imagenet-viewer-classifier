# imagenet-viewer-classifier

The service uses pretrained ImageNet model (deployed to Triton) to classify incoming images.
It uses confidence threshold to "reject" image.

# Requirements

1. Ubuntu 20.04.3
2. Python 3.8.10
3. requirements.txt
4. python -m pip install git+https://github.com/yashenkoxciv/imagenet-viewer.git

# Expected environment variables

| Name                    | Description                                                               |
|-------------------------|:--------------------------------------------------------------------------|
| TRITON_HOST             | Triton's host                                                             |
| MODEL_NAME              | deployed model name                                                       |
| RABBITMQ_HOST           | RabbitMQ's host                                                           |
| INPUT_QUEUE             | RabbitMQ's queue with images to classify                                  |
| OUTPUT_SUCCESS_QUEUE    | RabbitMQ's queue to push recognized image                                 |
| OUTPUT_FAILURE_QUEUE    | RabbitMQ's queue to push unrecognized image                               |
| MONGODB_HOST            | MongoDB's connection string like this: mongodb://host:port/imagenetviewer |
| SUCCESS_SCORE_THRESHOLD | confidence threshold (0.85)                                               |


