FROM python:3.11.9

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

CMD ["uvicorn", "fundapi.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]

