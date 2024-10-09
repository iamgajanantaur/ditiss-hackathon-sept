#FROM drupalci/php-7.1-apache:production
#COPY . /var/www/html
#EXPOSE 80


#FROM python
#WORKDIR /src
#RUN pip install flask
#COPY . .
#EXPOSE 5000
#CMD python myapp.py


FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 4000

CMD [ "python", "./myapp.py" ]
