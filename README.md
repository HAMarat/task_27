# Домашнее задание №28

Для начала работы скопируйте репозиторий на локальную машину: c помощью команды в терминале

- [task_28](https://github.com/HAMarat/course_work_5.git)

Откройте склонированный репозиторий в PyCharm.

## Cоздайте виртуальное окружение:
Простой вариант:
- Pycharm может предложить вам сделать это после того, как вы откроете папку с проектом. В этом случае после открытия папки с проектом в PyCharm появляется всплывающее окно, Creating virtual environment c тремя полями. В первом поле выбираем размещение папки с виртуальным окружением, как правило, это папка venv в корне проекта Во втором поле выбираем устанавливаемый интерпритатор по умолчанию (можно оставить без изменений) В 3 поле выбираем список зависимостей (должен быть выбран файл requirements.txt, находящийся в корне папки проекта)

Если этого не произошло, тогда следует выполнить следующие действия вручную:
Установка виртуального окружения:
- Во вкладке File выберите пункт Settings
- В открывшемся окне, с левой стороны найдите вкладку с именем вашего репозитория (Project: task_27)
- В выбранной вкладке откройте настройку Python Interpreter
- В открывшейся настройке кликните на значок ⚙ (шестеренки) расположенный сверху справа и выберите опцию Add
- В открывшемся окне слева выберите Virtualenv Environment, а справа выберите New Environment и нажмите ОК

## Запуск приложения локально

Для запуска у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой `pip install -r requirements.txt`
- Запустите сервер командой `flask --app scp/app run`
    - `--app scp/app` - использовать файл для запуска `scp/app`

## Создание образа docker

Для запуска у вас уже должен быть установлен Docker.

- Используйте ранее скаченный код
- Запустите создание образа командой `docker build -t cw_5 ./scp`
  - `docker build` - создание образа
  - `-t cw_5` - присвоение названия образа `cw_5`
  - `./scp` - путь нахождения `Dockerfile`
- Приложение будет запущено по адресу http://127.0.0.1:80

## Создание и запуск контейнера docker

- Запустите создание и запуск контейнера командой `docker run --name cw_5 -d -p 80:80 cw_5` 
  - `docker run` - создание и запуск контейнера
  - `--name cw_5` - присвоить название контейнеру `cw_5`
  - `-d` - запуск контейнера в качестве отдельного процесса
  - `-p 80:80` - публикация открытого порта в интерфейсе хоста (HOST:CONTAINER) (проброс порта)
  - `cw_5` - использовать образ с названием `cw_5`
- Контейнер с приложением будет запущен по адресу http://127.0.0.1:80

## Дополнительные команды docker

- `docker images` - просмотр загруженных образов


- `docker ps [OPTIONS]` - просмотр запущенных контейнеров
    - -a - показать все контейнеры (как запущенные, так и остановленные)
    - -f - фильтрация вывода на основе условия (`id`, `name`, `status` и т.д.)
    - -n - показать n последних созданных контейнеров
    - -l - показать последний созданный контейнер


- `docker start [CONTAINER]` - запуск остановленного контейнера


- `docker stop [CONTAINER]` - остановка контейнера

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python [Skypro](https://sky.pro).