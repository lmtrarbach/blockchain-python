FROM python:3.8-slim-buster
RUN apt-get update && \
    apt-get install -y git
WORKDIR /app
COPY blockchain/* .
RUN pip install -r requirements.txt
EXPOSE 50051
CMD ["python", "communication.py"]
