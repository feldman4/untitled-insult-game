#!/usr/bin/env bash
# home=DF
# PYTHONPATH=$home/src:$PYTHONPATH python $home/src/game/app.py $@
python game/app.py $@ 1> logs/server.out