#!/bin/bash

ENV_FILE="git_notification_bot.env"

if [ "$#" -eq 1 ]
then
    ENV_FILE=$1
fi



DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

set -o allexport
source "${DIR}"/"${ENV_FILE}"
set +o allexport
