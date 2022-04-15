FROM python:3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

WORKDIR /app

CMD ["python", "-m", "uvicorn", "me_visualization:app", "--host", "0.0.0.0", "--port", "8000"]




