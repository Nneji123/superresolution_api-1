FROM python:3.7.13-slim-bullseye

WORKDIR /app

RUN apt-get -y update  && apt-get install -y \
  python3-dev \
  apt-utils \
  python-dev \
  python3-opencv \
  build-essential \
&& rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade setuptools 
    
COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000:8000

CMD uvicorn app:app --reload --host 0.0.0.0 --port 8000


#CMD gunicorn -w 3 -k uvicorn.workers.UvicornWorker app:app --bind 0.0.0.0:$PORT

# uncomment this command to download the model and convert it to onnx and also start the container
#CMD ./setup.sh
