#!/bin/bash
export PATH=$PATH:/usr/local/bin
source ~/.bashrc
source ~/.profile
echo "path = $PATH"
cd /home/ubuntu/RSF_Crowd_Analysis
python3 rsf_alert.py

