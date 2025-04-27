FROM python:3.10-slim
WORKDIR /app
COPY ./backend /app
COPY ./frontend /app/frontend
RUN pip install fastapi uvicorn jinja2 requests
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
