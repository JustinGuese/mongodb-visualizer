FROM python:3.8
RUN mkdir /app
WORKDIR /app
COPY ./src/requirements.txt /app
RUN pip install -r requirements.txt
COPY ./src/app.py /app
ENTRYPOINT ["python","app.py"]