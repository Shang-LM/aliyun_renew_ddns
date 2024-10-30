FROM registry.cn-beijing.aliyuncs.com/docker_images_shang/python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update && apt-get install -y cron

COPY crontab /etc/cron.d/my-cron

RUN chmod 0644 /etc/cron.d/my-cron

RUN crontab /etc/cron.d/my-cron

RUN touch /var/log/cron.log

CMD cron -f