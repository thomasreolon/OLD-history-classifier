FROM python:3-alpine
#LABEL author="Thomas"

COPY app /app

WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]