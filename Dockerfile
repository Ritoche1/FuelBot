FROM python:3

WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirement.txt

CMD ./bot.py