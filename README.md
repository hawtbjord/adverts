Текущий функционал:

Основные сущности:

-Пользователи: кастомная модель с email вместо username; регистрация с подтверждением по почте; аутентификация и авторизация; восстановление пароля по email (назначение нового). Вход доступен только пользователям, подтвердившим свой email переходом по ссылке из полученного сообщения. После входа пользователь попадает в личный кабинет (состав личного кабинета зависит от группы пользователя);  
-Объявления: создание объявления с возможностью прикреплять изображения, редактирование объявления, скрыть объявление, отправка объявления на модерацию, модерация объявлений (отправка на доработку с указанием необходимых правок или активация для отображения в списке объявлений). Поиск объявлений на главной странице по заданным критериям


Личный кабинет: 

-пользователя: просмотр списка своих объявлений в любых состояниях;  
-модератора: возможности пользователя + просмотр списка объявлений, отправленных на модерацию, возможность проведения модерации;  
-администратора: возможности модератора + CRUD пользователей и справочников.


TODO:

-ограничение на выбор категории при создании объявления (сейчас возможно создание в любой "общей" категории);  
-поиск объявлений в дочерних категориях при выборе родительских;  
-пагинация;  
-оптимизация запросов к бд;  
-прочие доработки, обработки исключений;  
-bootstrap, вёрстка;  
-настройка отправки почты через rabbitmq;  
-смена бд на postgres;  
-изображения - thumbnails для экономии трафика при просмотре, при нажатии - доступ к оригинальному изображению;  
-тесты для основной бизнес логики;  
-реализация поиска через elasticsearch;  
-контейнеризация, запуск на linux.



Запуск проекта (пока на windows в служебном режиме):

-python manage.py migrate (создаем таблицы в бд);  
-python manage.py createsuperuser (делаем суперпользователя);  
-python manage.py runserver (стартуем сервер);  
-входим в стандартную админку %host%/admin;  
-создаем группы "Администраторы","Модераторы","Пользователи", добавляем свою учетную запись в группу "Администраторы";  
-заполняем справочники регионов, городов и категорий;  
-для регистрации пользователей в папке приложения accounts необходимо создать файл email_creds.py , создать почтовый ящик (желательно gmail, и разрешить доступ сторонних приложений) для отправки сообщений от имени сервера при регистрации/восстановления пароля, и указать данные как в файле email_creds_example.py
