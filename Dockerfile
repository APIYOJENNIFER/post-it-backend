FROM python:3.7

WORKDIR /postit

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
