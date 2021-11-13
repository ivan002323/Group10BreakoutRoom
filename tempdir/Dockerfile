FROM python
COPY  ./static /home/myapp/static/
COPY  ./templates /home/myapp/templates/
COPY  testingmap.py /home/myapp/
COPY  requirements.txt /home/myapp/
RUN pip install -r /home/myapp/requirements.txt
EXPOSE 5050
CMD python3 /home/myapp/testingmap.py
