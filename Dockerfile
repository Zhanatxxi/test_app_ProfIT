FROM  python:3.10-alpine

WORKDIR /app

COPY requirements.txt .

ENV PYTHONUNBUFFERED 1

RUN apk update && apk upgrade

RUN apk add --no-cache gcc && apk add libc-dev && apk add libffi-dev

RUN pip install --upgrade pip \
  pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

COPY . /app/

EXPOSE 8000

CMD ["/docker-entrypoint.sh"]
