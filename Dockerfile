FROM registry.cn-beijing.aliyuncs.com/docker_images_shang/python:3.10-slim
LABEL authors="shang"

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN apt-get update && apt-get install -y cron

COPY corntab /etc/cron.d/my-cron

RUN chmod 0644 /etc/corn.d/my-cron

RUN corntab /etc/corn.d/my-cron

RUN touch /var/log/cron.log

CMD ["cron", "-f"]