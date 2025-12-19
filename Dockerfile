FROM ultralytics/ultralytics:latest-python


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY app/ .

EXPOSE 5000

# Lance l'application
CMD ["python", "app.py"]
