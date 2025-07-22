FROM python:3.12
WORKDIR /home/timmy/event-planner

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

COPY app ./app
COPY run.py ./

CMD ["python" , "run.py"]