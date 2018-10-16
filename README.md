# HABROPROXY

[![Build Status](https://travis-ci.org/ydanilin/habroproxy.svg?branch=master)](https://travis-ci.org/ydanilin/habroproxy)
[![Maintainability](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/maintainability)](https://codeclimate.com/github/codeclimate/codeclimate/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/a99a88d28ad37a79dbf6/test_coverage)](https://codeclimate.com/github/codeclimate/codeclimate/test_coverage)

## Описание

Проект выполнялся как тестовое задание в компанию [Ivelum](https://ivelum.com/).

Представляет собой прокси-сервер, который модифицирует html-страницы от сервера habr.com следующим образом:

* если длина слова на html странице равна 6 символов, к такому слову в конце добавляется значок тм.

Ответы от других серверов и/или с контентом, отличным от html, не модифицируются.

Прокси поддерживает `https` соединения, поэтому следует внимательно выполнить шаги раздела "Установка" по настройке SSL сертификата, который является неотъемлемой частью работы защищенного протокола. Подробности работы сервера в разделе "Схема работы по SSL".

## Установка

