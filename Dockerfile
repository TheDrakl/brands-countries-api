FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN adduser -D -g '' appuser && \
    mkdir /app && \
    chown -R appuser /app

WORKDIR /app

RUN apk update && apk add --no-cache build-base libffi-dev

COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "core.wsgi:application"]