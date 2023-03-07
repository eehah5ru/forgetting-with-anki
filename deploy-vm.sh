#!/bin/bash

# pi version
USER=forgetting
HOST=forgetting.eeefff

# deploy plugin to the virtual machine
rsync -avz * $USER@$HOST:/home/$USER/.local/share/Anki2/addons21/forgetting/
