# syntax=docker/dockerfile:1

FROM python:3.12
ENV PYTHONUNBUFFERED True
ADD . .
RUN pip3 install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD ["python3", "./pywsgi.py"]