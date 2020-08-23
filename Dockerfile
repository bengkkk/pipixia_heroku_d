FROM ubuntu
ADD dck/ /workarea
WORKDIR /workarea

RUN apt-get update --fix-missing \
    && apt-get -y install openssh-server \
    && service ssh start \
    && apt-get -y install wget \
    && wget https://cdn.jsdelivr.net/gh/drkoubst/warehouse/docker-ssh/autossh.sh \
    && sed -i 's/\r//' autossh.sh \
    && chmod +x autossh.sh \
    && /bin/bash autossh.sh \
    && mkdir \workarea \
    && apt install -y python3 python3-pip
RUN pip3 install -r requirements.txt
CMD bash /workarea/start.sh

EXPOSE 22
EXPOSE 8888