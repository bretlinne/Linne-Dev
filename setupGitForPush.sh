#! /bin/bash

git config --global user.email "bretlinne@gmail.com"
git config --global user.name "bret linne"
eval $(ssh-agent)
ssh-add ~/.ssh/linne-learn-aws.pem
