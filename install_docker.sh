#!/bin/bash
sudo apt-get install python3.6
sudo apt-get install python3-pip

sudo apt-get remove docker docker-engine

sudo apt-get remove docker.io

sudo apt-get install linux-image-extra-virtual

sudo apt-get install \
  apt-transport-https \
  ca-certificates \
  curl \
  software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"

sudo add-apt-repository \
  "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) \
  stable"

sudo apt-get install docker-ce

# test docker
sudo docker run hello-world 

sudo usermod -aG docker $USER

sudo systemctl enable docker

pip3 install docker-compose

# test docker
~/.local/bin/docker-compose version

