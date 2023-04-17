FROM python:3.8

WORKDIR /app/backend
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python3 -u server_v2.py