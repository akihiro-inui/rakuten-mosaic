# Base Python image
FROM python:3.8

# API port to expose
EXPOSE $PORT

# Copy contents
COPY . .

# Install libraries
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

# Install python packages
RUN pip install --upgrade pip
RUN pip install cmake==3.21.2
RUN pip install -r requirements.txt

# Run API application
CMD ["gunicorn", "-w", "3", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:$PORT", "src.main:app"]