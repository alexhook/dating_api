Dating API
===========

Описание
----------

Данная работа является тестовым заданием при прохождении собеседования. Основная цель - написать API для сайта знакомств, используя Django Rest Framework.

Тех. задание
----------

1.	Создать модель участников. У участника должна быть аватарка, пол, имя и фамилия, почта.
2.	Создать эндпоинт регистрации нового участника: /api/clients/create.
3.	При регистрации нового участника необходимо обработать его аватарку: наложить на него водяной знак.
4.	Создать эндпоинт оценивания участником другого участника: /api/clients/{id}/match. В случае, если возникает взаимная симпатия, то ответом выдаем почту клиенту и отправляем на почты участников: «Вы понравились <имя>! Почта участника: <почта>».
5.	Создать эндпоинт списка участников: /api/list. Должна быть возможность фильтрации списка по полу, имени, фамилии.
6.	Реализовать определение дистанции между участниками. Добавить поля долготы и широты. В api списка добавить дополнительный фильтр, который показывает участников в пределах заданной дистанции относительно авторизованного пользователя.
