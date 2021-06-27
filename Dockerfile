FROM python:3.7-alpine
WORKDIR /src
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]
