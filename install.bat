@echo off

echo "Install Python Anaconda 2 & 3 (manually)"
pause

pip install --upgrade pip

pip install autobahn[twisted]
pip install futures

pause
