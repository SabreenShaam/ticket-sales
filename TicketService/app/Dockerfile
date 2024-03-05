FROM python:3.9
ENV PYTHONUNBUFFERED 1
ADD . /app
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["app.py"]
