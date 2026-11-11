# Depviz — визуализатор графа зависимостей

Учебный проект по дисциплине «Конфигурационное управление».
Утилита командной строки, которая строит граф зависимостей пакета
и экспортирует его в формат Graphviz (DOT), а также может рендерить его в PNG.

## Возможности

- `--graphviz` — путь к файлу `dot`, в который будет сохранён граф.
- `--repo` — путь к локальному репозиторию (папке с `requirements.txt`).
- `--package` — имя анализируемого пакета (необязательно).
- `--filter` — регулярное выражение для фильтрации имён зависимостей.
- `--render` — отрендерить граф в PNG с помощью утилиты `dot` (требуется установленный Graphviz).

## Требования

- Python 3.8+
- Git
- [Graphviz](https://graphviz.org/download/) (опционально, для флага `--render`)

## Установка

```bash
git clone https://github.com/NnMm7/Depviz.git
cd Depviz
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt