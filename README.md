# CISM_Test

## Описание

Необходимо разработать сервис для управления задачами с следующими функциональными требованиями:

1. Создание задач через REST API
2. Создание задач через очереди сообщений (RabbitMQ)
3. Реализация статусной модели для задач:
   - Новая задача
   - В процессе работы
   - Завершено успешно
   - Ошибка
4. Эмуляция процесса обработки задачи

## Технические требования

1. Язык программирования: Python
2. База данных: PostgreSQL
3. Очередь сообщений: RabbitMQ или Kafka
4. REST API: Реализовать с использованием соответствующего фреймворка (Flask, FastApi, Django)
5. Документация API: Swagger/OpenAPI
6. Контейнеризация: Docker

## Задачи

- [x] Разработать структуру базы данных для хранения задач и их статусов
- [x] Реализовать REST API с следующими эндпоинтами:
  - POST /tasks - создание новой задачи
  - GET /tasks/{id} - получение информации о задаче
  - GET /tasks - получение списка задач с возможностью фильтрации по статусу
- [x] Реализовать создание задач через очередь сообщений
- [x] Разработать worker для обработки задач:
  - Получение задачи из очереди
  - Изменение статуса задачи на "В процессе работы"
  - Эмуляция выполнения задачи (например, случайная задержка 5-10 секунд)
  - Изменение статуса задачи на "Завершено успешно" или "Ошибка" (с некоторой вероятностью)
- [x] Реализовать логирование процесса обработки задач
- [x] Написать unit-тесты для ключевых компонентов
- [x] Подготовить Docker Compose файл для запуска всех компонентов системы

## Инструкция по запуску приложения

1. Склонировать проект локально, создать файл .env в корне директории и перенести туда все параметры из файла .env-example
2. Запустить проект с использованием команды `make all`, которая выполнит миграции, сборку и развертывание миграций
3. Перейти по адресу <http://0.0.0.0:8000/docs#/> для просмотра интератктивной документации Swagger
4. Выполнить команду `make test` для выполнения unit-тестов
5. Для просмотра логов воркера использовать команду `make logs-worker`, для логов приложения - `make logs-app`
