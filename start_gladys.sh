#!/bin/sh

FILE=/tmp/gladys.log
GLADYS_LOCATION=$1

# Kill de tout les processus éventuellement existants
killall node
killall mplayer
# pm2 kill

rm /tmp/gladys*
touch $FILE
echo "file_not_empty" > $FILE
# echo "file_not_empty" > /tmp/gladys-0.log

# Lancement des processus
node $GLADYS_LOCATION/app.js &
sleep 10
cd $GLADYS_LOCATION/node_modules/gladys-voice/
node app.js >> $FILE &
# pm2 start app.js -o /tmp/gladys.log --name gladys-voice
echo "Listening..."

#TEXT=$(grep -Po '"text":.*?[^\\]",' $FILE)
#TEXT=$(echo ${TEXT:8:${#TEXT}-10})
#echo $TEXT
#echo ${#TEXT}