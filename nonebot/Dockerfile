FROM python:3.9-alpine

WORKDIR /bot-faas

COPY . .

RUN chmod +x ./function/build_script && \
    ./function/build_script

RUN pip install -r requirements.txt

RUN cd function && \
    pip install -r requirements.txt

CMD ["python3","index.py"]
