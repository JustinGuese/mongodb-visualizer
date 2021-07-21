FROM guestros/python-alpine-pandas-nonroot:latest
USER root
COPY ./src/requirements.txt /app
RUN pip install -r requirements.txt
USER pythy
COPY ./src/app.py /app
ENTRYPOINT ["gunicorn","-b", "0.0.0.0:5000", "app:app"]