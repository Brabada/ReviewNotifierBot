FROM python:3.10.12-alpine
WORKDIR /opt/notifier-bot
COPY requirements.txt ./
RUN pip3 install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
COPY main.py ./
COPY ".env" ./
CMD ["python3", "main.py"]