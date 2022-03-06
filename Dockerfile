FROM python:3.9.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN rm /app/requirements.txt
COPY ./app /app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers", "3", "skillactive.wsgi"]
