#FROM drupalci/php-7.1-apache:production
#COPY . /var/www/html
#EXPOSE 80


FROM python
WORKDIR /src
RUN pip install flask
COPY . .
EXPOSE 5000
CMD python ./hackathon-0824/myapp.py
