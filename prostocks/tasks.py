from celery import Celery

app = Celery('prostocks', broker='redis://localhost')

@app.task
def say_hello():
    print("Olá mundo!")