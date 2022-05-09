FROM python:3.10-slim
WORKDIR /app/server
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 50051
ENTRYPOINT [ "python", "server.py" ]
