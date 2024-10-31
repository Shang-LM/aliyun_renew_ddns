FROM registry.cn-beijing.aliyuncs.com/docker_images_shang/python:3.10-slim

ENV PYTHONUNBUFFERED=1

ENV TZ=Asia/Shanghai

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "main.py"]