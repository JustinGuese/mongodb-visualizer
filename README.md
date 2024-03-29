# description

really basic tool to print contents of a mongodb table to a pandas to_html() output

# usage

the tool uses basic auth, meaning you have to add vieweruser and viewerpwhash to the environment variables.
generate a hash running python generatepassword.py or

```
from werkzeug.security import generate_password_hash

user = input("please enter user")
pwhash = generate_password_hash(input("please enter password"))

print("please add the following to app.py at users = { '%s':'%s'}"%(user,pwhash))
```

if no env variable set the default user and password are:
USER: `test`
PW: `test`

### Environment Variables

MONGO_HOST: mongodb # container name of mongodb
MONGO_PORT: 27017 # is default value
MONGO_USERNAME: mongouser
MONGO_PASSWORD: mongopw # please change all this
MONGO_DATABASE: mongodb
MONGO_COLLECTION: test

## docker

```
version: "3.9"
services:
    mongo:
        image: "bitnami/mongodb"
        container_name: "mongodb"
        # ports:
        # - 27017:27017
        environment:
            MONGODB_USERNAME: mongouser
            MONGODB_PASSWORD: mongopw
            MONGODB_DATABASE: mongodb
    mongodb-visualizer:
        image: guestros/mongodb-visualizer
        container_name: "mongodb-visualizer"
        ports:
        - 5000:5000
        environment:
            MONGO_HOST: mongodb # container name of mongodb
            MONGO_PORT: 27017 # is default value
            MONGO_USERNAME: mongouser
            MONGO_PASSWORD: mongopw # please change all this
            MONGO_DATABASE: mongodb
            MONGO_COLLECTION: test
            
```

## kubernetes

### 1. Create MongoDB Database using e.g. bitnami helm

E.g. using bitnami mongodb helm chart:

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install mongodb bitnami/mongodb \
    --set persistence.size=1Gi \
    --set auth.database=mongodb \
    --set auth.username=mongouser \
    --set auth.password=mongopw
```

### 2. create a secret containing the login credentials

`kubectl create secret generic mongo-creds --from-literal=MONGO_PASSWORD='mongopw'`


### 3. And the matching deployment and service

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongodb-visualizer-deployment
  labels:
    app: mongodb-visualizer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongodb-visualizer
  template:
    metadata:
      labels:
        app: mongodb-visualizer
    spec:
      containers:
      - name: mongodb-visualizer
        imagePullPolicy: "Always"
        image: guestros/mongodb-visualizer:latest
        ports:
        - containerPort: 5000
        env:
          - name: MONGO_HOST
            value: "mongodb"
          - name: MONGO_PORT
            value: "27017"
          - name: MONGO_USER
            value: "mongouser"
          - name: MONGO_DATABASE
            value: "mongodb"
          - name: MONGO_COLLECTION
            value: "test"
          - name: MONGO_PASSWORD
            valueFrom:
              secretKeyRef:
                name: mongo-creds
                key: MONGO_PASSWORD
---
apiVersion: v1
kind: Service
metadata:
  name: mongodb-visualizer-service
spec:
  ports:
  - port: 8002
    targetPort: 5000
    protocol: TCP
    name: http
  selector:
    app: mongodb-visualizer
```