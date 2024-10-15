FROM python:3.12.3-alphine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /server/
COPY  requirements.txt /server/
RUN pip install -r requirements.txt
COPY . /server/
EXPOSE 8000
CMD [ "python", "manage.py", "runserver" ]