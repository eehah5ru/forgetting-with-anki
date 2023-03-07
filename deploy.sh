#!/bin/bash

# pi version
USER=pi
HOST=pi4.local

rsync -avz * $USER@$HOST:/home/pi/.local/share/Anki2/addons21/forgetting/
rsync -avz * $USER@$HOST:/home/pi/.anki/en/Anki2/addons21/forgetting/
rsync -avz * $USER@$HOST:/home/pi/.anki/ru/Anki2/addons21/forgetting/

ssh $USER@$HOST "sudo systemctl restart anki.service"
