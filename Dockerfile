FROM python:3.10.12
RUN pip3 install --upgrade pip
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt && rm tmp/requirements.txt
COPY . /opt/bot_v1
WORKDIR /opt/bot_v1
CMD python3 main.py
