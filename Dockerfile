FROM python:3.9

WORKDIR /monetas

COPY reqs.txt /monetas/
RUN pip install -r reqs.txt

COPY . /monetas/

CMD python charity_bot.py