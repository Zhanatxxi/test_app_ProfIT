#!/bin/sh

alembic upgrade head

uvicorn currency.api:app --proxy-headers --host 0.0.0.0 --port 8000 --workers 4