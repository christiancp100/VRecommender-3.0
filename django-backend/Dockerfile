FROM python:3.8

WORKDIR /app
RUN apt-get update
RUN apt-get install -y --no-install-recommends binutils libproj-dev gdal-bin curl
COPY requirements.txt .
RUN pip install -r requirements.txt

# Remember to listen on 0.0.0.0
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]