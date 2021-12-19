# Simple system of home video monitoring

#### Contains:
1. Telegram bot for sending camera captures
2. Program for motion detection and write video and images
3. Config for systemd service for start telegram bot

#### Get startted

#### Install dependencies:
```
sudo apt install python3-pip
sudo pip3 install python-telegram-bot
sudo apt install python3-watchdog
sudo apt install python3-opencv
sudo apt install python3-matplotlib
```
 
##### Setup service:
```
copy file telegrambot.service to /etc/ststemd/service
sudo systemctl daemon-reload
sudo systemctl enable telegrambot.service
sudo systemctl start telegrambot.service
```
 
##### Launch motion detection
```
python3 ./motion_detect.py
```
---
Author TechnoMag 2021
