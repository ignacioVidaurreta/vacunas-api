## Set up

Either from a virtual environment (recommended) or not install the requirements:

```shell
pip install -r requirements.txt
```

## Run the server

### Locally

```shell
uvicorn main:app --reload
```

### Building docker image

```shell
docker build -t infovis-api .
```

### Running docker container

```shell
docker run --rm -it -v $PWD:/src --network host infovis-api
```
