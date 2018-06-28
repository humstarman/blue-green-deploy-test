FROM lowyard/docker-flask:latest 
ADD img /static/img/
ADD js /static/js/
ADD app.py /
ADD templates /templates/
ADD entrypoint.sh /
