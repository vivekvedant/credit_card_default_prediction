#!/bin/bash

sudo apt update && sleep 5;

sudo apt install -y software-properties-common  && sleep 5;
sudo add-apt-repository --yes --update ppa:ansible/ansible  && sleep 5;
sudo apt install -y ansible;
