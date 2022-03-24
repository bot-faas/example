FROM python:3.9-bullseye

WORKDIR /bot-faas

COPY . .

RUN sed -i "s/deb.debian.org/mirrors.cloud.tencent.com/g" /etc/apt/sources.list && \
    sed -i "s/security.debian.org/mirrors.cloud.tencent.com/g" /etc/apt/sources.list && \
    cat /etc/apt/sources.list && \
    apt update && \
    apt install git gcc g++ make && \
    pip install -i https://mirrors.cloud.tencent.com/pypi/simple -r requirements.txt

RUN cd function && \
    pip install -i https://mirrors.cloud.tencent.com/pypi/simple -r requirements.txt

CMD ["python3","index.py"]
