FROM oldtaoge/nmh_dep:latest
RUN git clone https://github.com/OldTaoge/NeteaseMusicHelper.git .
ENTRYPOINT  python NEM-main.py