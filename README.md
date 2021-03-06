# HABROPROXY

[![Build Status](https://travis-ci.org/ydanilin/habroproxy.svg?branch=master)](https://travis-ci.org/ydanilin/habroproxy)
[![Maintainability](https://api.codeclimate.com/v1/badges/58160aab1f244142509b/maintainability)](https://codeclimate.com/github/ydanilin/habroproxy/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/58160aab1f244142509b/test_coverage)](https://codeclimate.com/github/ydanilin/habroproxy/test_coverage)

## Описание

Проект выполнялся как тестовое задание в компанию [Ivelum](https://ivelum.com/).

Представляет собой прокси-сервер, который модифицирует html-страницы от сервера [habr.com](https://habr.com/) следующим образом:

* если длина слова на html странице равна 6 символов, к такому слову в конце добавляется значок ™.

Ответы от других серверов и/или с контентом, отличным от html, не модифицируются.

Прокси поддерживает `https` соединения, поэтому следует внимательно выполнить шаги раздела "Установка" **по настройке SSL сертификата**, который является неотъемлемой частью работы защищенного протокола. Подробности работы сервера в разделе "Схема работы прокси".

Тестировался с браузером Firefox в Ubuntu и Windows

## Установка

### Prerequisites

* `Python` версии **не выше 3.6.6**. Новейшая 3.7 на данный момент не поддерживает библиотеку OpenSSL.
* Пользователям Windows рекомендуется установить недостающий и очень удобный инструмент `make`, скачав его [отсюда](https://vorboss.dl.sourceforge.net/project/gnuwin32/make/3.81/make-3.81.exe) и прописав в путь.
* Браузер Firefox (с другими пока не тестировалось)

### Развертывание

```bash
git clone https://github.com/ydanilin/habroproxy.git
cd habroproxy
make install
```

### Генерация сертификата

По общему правилу сертификаты с приватными ключами не коммитятся в репозитории, но создаются локально на пользовательской машине. Для генерации сертификата наберите из корневой папки проекта:

```bash
make gencert
```

### Установка в браузер

Данная версия прокси тестировалась в первую очередь (пока только) с браузером Firefox. Причина тому то, что Firefox использует свое собственное хранилище сертификатов, что не требует их установки в систему.  
Требуемый файл сертификата: `<папка проекта>/cert/habroproxy-ca.pem`  
Настройка: Браузер -> Настройки -> Приватность и безопасность -> на дне кнопка "Просмотр сертификатов" -> Импорт

### Перенаправление трафика браузера через прокси

Браузер -> Настройки -> Общие -> на дне раздел "Прокси", кнопка "Настроить"  
Хост/порт: `localhost 8080`

### Запуск

Для запуска прокси набираем

```bash
make run
```

Получаем ответ  
`Habroproxy server is listening to '': 8080`

## Схема работы прокси

Большинство сайтов переходят на протокол `https`, поэтому пришлось вникать в основы TLS/SSL и реализовывать его поддержку.  
Схема работы по TLS выглядит следующим образом:

* Клиент, возжелавший секьюрности, присылает http-глагол `CONNECT` с указанием требуемого хоста;
* Сервер генерит на лету dummy сертификат для указанного хоста, ссылается в нем на самоподписной корневой сертификат (сооружает trust chain), который мы установили в клиента. С этой парочкой (и ключами) создается `SSL context`, в него заворачивается изначальный клиентский сокет и все это засовывается в клиента процедурой `do_handshake()`;
* После обмена криптографическими любезностями клиент присылает `GET` (или `POST`) с указанием того, что же он хочет на удаленном хосте (данные уже расшифрованы для нас библиотекой `OpenSSL`);
* Сервер форвардит клиентский запрос на удаленный хост. Чтобы не возиться с TLS/SSL с удаленным хостом вручную, коммуникация с ним поручена библиотеке [python requests](http://docs.python-requests.org/en/master/), которая делает все сама и отдает уже расшифрованный ответ;
* Приходящий ответ проверяется сервером нужно ли его модифицировать (`host == habr.com AND content-type == html`), после чего запихивается в клиентский сокет. Работу по зашифровыванию делает опять же `OpenSSL`.
