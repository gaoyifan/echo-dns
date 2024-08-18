FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir dnslib

EXPOSE 53/udp 53/tcp

COPY main.py /app

CMD ["python", "main.py"]
