#!/bin/bash
cd packer
wget https://dl.bintray.com/mitchellh/packer/packer_0.7.5_linux_amd64.zip
unzip -o  packer_0.7.5_linux_amd64.zip
sudo mv packer* /usr/bin/
