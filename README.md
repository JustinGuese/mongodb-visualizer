# description

really basic tool to print contents of a mongodb table to a pandas to_html() output

# usage

## docker

```
version: "3.9"
services:
    mongo:
        image: "bitnami/mongodb"
        container_name: "bwcontactformbackend-mongodb"
        ports:
        - 27017:27017
        environment:
            MONGODB_USERNAME: mongo
            MONGODB_PASSWORD: mongopw
            MONGODB_DATABASE: bwnosql
    
```

## kubernetes