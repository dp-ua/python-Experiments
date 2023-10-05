@echo off
color 02

echo "<========== INSTALLING REQUIREMENTS =========>"
pip install -r requirements.txt

echo "<========== START BOT  =========>"
python -u "apibot_bot.py"
