FROM python:3.14.3-alpine
RUN apk update && apk add alpine-conf
RUN setup-timezone -z Canada/Pacific

EXPOSE 8000

EXPOSE 5432

RUN apk add postgresql

WORKDIR /src/app
COPY git-notification-bot/atlassian atlassian
COPY git-notification-bot/bitbucket_webhook bitbucket_webhook
COPY git-notification-bot/core core
COPY git-notification-bot/python_logging python_logging
COPY git-notification-bot/slack slack
COPY git-notification-bot/manage.py manage.py
COPY requirements.txt requirements.txt
COPY .ci/db-requirements.txt db-requirements.txt
COPY .ci/entrypoint.sh entrypoint.sh


RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r db-requirements.txt

RUN rm db-requirements.txt


ENTRYPOINT ["./entrypoint.sh"]

CMD ["python", "-u", "manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["sh"]
