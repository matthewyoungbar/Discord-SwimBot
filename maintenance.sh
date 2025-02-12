#!/usr/bin/env bash
if [[ $1 == "on" ]]
then
    heroku maintenance:on -a discord-swimbot
    heroku ps:scale worker=0 -a discord-swimbot
elif [[ $1 == "off" ]]
then
    heroku maintenance:off -a discord-swimbot
    heroku ps:scale worker=1 -a discord-swimbot
else
    echo "Usage: $0 on|off"
fi
