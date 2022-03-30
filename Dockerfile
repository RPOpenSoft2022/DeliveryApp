FROM python:3.8

# Create a virtualenv for the application dependencies.
# # If you want to use Python 2, use the -p python2.7 flag.
RUN apt-get update && apt-get install -y binutils libproj-dev gdal-bin
ADD requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt 
ADD . /app
CMD cd app/delivery && python manage.py makemigrations --merge && python manage.py migrate && gunicorn -b :8080 delivery.wsgi:application