FROM python:3.12.5-alpine
RUN apk update && apk add alpine-conf
RUN setup-timezone -z Canada/Pacific

EXPOSE 8000

EXPOSE 5432

RUN apk add postgresql

WORKDIR /src/app
COPY slackGitPrBot/bitbucket bitbucket
COPY slackGitPrBot/slackGitPrBot slackGitPrBot
COPY slackGitPrBot/bot_logging bot_logging
COPY slackGitPrBot/manage.py manage.py
COPY slackGitPrBot/requirements.txt requirements.txt
COPY slackGitPrBot/db-requirements.txt db-requirements.txt
COPY CI/validate_and_deploy/2_deploy/server_scripts/run_docker.sh run_docker.sh
COPY CI/validate_and_deploy/2_deploy/server_scripts/wait-for-postgres.sh wait-for-postgres.sh

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r db-requirements.txt


CMD ["./wait-for-postgres.sh", "./run_docker.sh"]
#CMD ["sh"]
