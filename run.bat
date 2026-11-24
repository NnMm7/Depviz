@echo off
echo Запуск depviz (Этап 1)...
python src/main.py --package A --source tests.txt --test-mode
pause