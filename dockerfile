FROM python:3

WORKDIR /opt/working/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .