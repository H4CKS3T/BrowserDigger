# BrowserDigger

BrowserDigger — инструмент для восстановления данных из кэша популярных браузеров. После сбора файлов скрипт проверяет их MIME-типы и сортирует результаты по подпапкам.

## Особенности
* Собирает кэш браузеров Chrome, Edge, Firefox и Yandex для каждого найденного пользователя.
* Копирует файлы в временную директорию (С:\Temp\browserdigger или /tmp/browserdigger).
* Определяет MIME-тип каждого файла с помощью `python-magic` и сортирует по категориям (images, videos, audio, documents, applications, fonts, 3d_models, unknown).

## Установка
1. Убедитесь, что на компьютере установлен Python 3.
2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск
```bash
python main.py
```
После запуска результаты появятся в папке `browser_cache` внутри временной директории. Файлы будут разложены по подпапкам в соответствии с их MIME-типам.

## Структура вывода
```
/tmp/browserdigger/
└── browser_cache/
    ├── images/
    ├── videos/
    ├── audio/
    ├── documents/
    ├── applications/
    ├── fonts/
    ├── 3d_models/
    └── unknown/
```
На Windows аналогичная директория находится в `C:\Temp\browserdigger`.

