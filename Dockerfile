FROM python:3.10.10
# Using nvidia/cuda image when you want to get GPU support

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app

EXPOSE 8080

ARG WORKER=1
ARG HOST=0.0.0.0
ARG PORT=8080

ENV _WORKER=$WORKER
ENV _HOST=$HOST
ENV _PORT=$PORT

CMD ["sh", "-c", "uvicorn main:app --workers ${_WORKER} --host ${_HOST} --port ${_PORT}"]
