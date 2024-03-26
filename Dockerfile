FROM python:3.10.12-slim-bookworm
WORKDIR /opt/notifier-bot
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
pip3 install -r /tmp/requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org 
COPY main.py ./
CMD ["python3", "main.py"]