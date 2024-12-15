# AWR Auto

## Инструкция
1. `git clone https://github.com/oustrix/awr_auto && cd awr_auto`
2. `cp .env.example .env`
3. Установить зависимости с помощьюу `pip install -r requiremenets.txt`
4. В файле `.env` ввести свои значения:
   + _INPUT_DIRECTORY_PATH_ - путь к директории с .emp файлами
   + _OUTPUT_DIRECTORY_PATH_ - путь к дя CST Studio. Подробнее можно прочитать в [документации](https://space.mit.edu/RADIO/CST_online/Python/main.html)
5. Скомпилировать исполняемый файл `make build`
6. Исполняемый файл находится в директории `dist/start`, рядом с ним необходимо расположить файл `.env` с конфигурацией