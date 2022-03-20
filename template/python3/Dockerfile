FROM python:3.9-alpine

WORKDIR /bot-faas

COPY . .

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# RUN cd function && \
#     pip install -r requirements.txt

CMD ["python3","index.py"]
