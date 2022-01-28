FROM python:3.8

LABEL maintainer="synodriver"

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt -i https://pypi.org/simple

#COPY ./start.sh /start.sh
#RUN chmod +x /start.sh
WORKDIR /
#COPY . /
COPY ./config.py /config.py
COPY ./main.py /main.py

#COPY ./start-reload.sh /start-reload.sh
#RUN chmod +x /start-reload.sh

COPY ./app /app
COPY ./log /log

#ENV PYTHONPATH=/app

EXPOSE 9000

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
#CMD ["/start.sh"]
#CMD python /main.py
CMD python -m gunicorn -c ./config.py