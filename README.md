# Depviz — визуализатор графа зависимостей

Учебный проект по дисциплине «Конфигурационное управление».
Утилита командной строки, которая строит граф зависимостей пакета
и экспортирует его в формат Graphviz (DOT).

## Возможности

- `--graphviz` — путь к файлу `dot`, в который будет сохранён граф.
- `--package` — имя анализируемого пакета.
- `--repo` — URL репозитория пакета.
- `--filter` — регулярное выражение для фильтрации имён зависимостей.

## Требования

- Python 3.8+
- Git

## Установка

```bash
git clone https://github.com/NnMm7/Depviz.git
cd Depviz
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt