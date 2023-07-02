FROM  python:3.10.11-slim

WORKDIR /app
COPY . .
RUN apt-get update
RUN apt-get install libgomp1
RUN pip install -r requirements.txt
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "80"]