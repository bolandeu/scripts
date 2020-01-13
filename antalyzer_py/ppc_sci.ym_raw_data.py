from openpyxl import load_workbook
import requests
import json
import datetime
import pandas as pd

class YandexMetrikaConnectorAPI:
    
    # статусы запросов
    STATUS = {'processed': 'обработан (готов к выгрузке)',
              'canceled': 'отменён',
              'processing_failed': 'ошибка при обработке',
              'created': 'создан (не готов к выгрузке)',
              'cleaned_by_user': 'очищен пользователем',
              'cleaned_automatically_as_too_old': 'очищен автоматически'}
    
    def __init__(self, token='', counterId=''):
        self.token = str(input('Введите ваш токен: ')) if not token else token
        self.counterId = str(input('Введите номер счетчика(ов): ')) if not counterId else counterId
    
    # основной диалог
    def start(self):
        print("""\
------------------------------------------
            ГЛАВНОЕ МЕНЮ
------------------------------------------
    Операции, доступные для ввода:
    '1' - Получить список идентификаторов запросов логов с сервера
    '2' - Создать новый запрос логов на сервере 
    '3' - Удалить запрос(ы) логов на сервере 
    '4' - Записать результат в excel файл
    '0' - Выйти из меню и завершить работу (также команда 'exit')""")
        while True:
            self.answer = str(input('Введите код операции: ')).lower().strip()
            if self.answer in ['0','1','2','3','4','exit']:
                self.answer = self.answer
                break
            else:
                print("Неверный ввод. Выберите код операции из списка доступных.")
        if self.answer == '1':
            return __class__.get_id_requests(self)
        elif self.answer == '2':
            return __class__.make_request(self)
        elif self.answer == '3':
            return __class__.clean_requests(self)
        elif self.answer == '4':
            return __class__.write_excel(self)
        elif self.answer in ['0', 'exit']:
            return 'Работа завершена.'
        
    # список запросов с сервера
    def get_id_requests(self):
        url = f'https://api-metrika.yandex.ru/management/v1/counter/{self.counterId}/logrequests'
        logs = json.loads(requests.get(url, 
                                       headers={"Authorization": f'OAuth {self.token}'}).text)['requests']
        print("------------------------------------------\nСПИСОК ЗАПРОСОВ ЛОГОВ:\n------------------------------------------")
        for n, log in enumerate(logs):
            print(f"{n+1}. Идентификатор запроса логов: {log['request_id']}")
            print(f"   Идентификатор счётчика: {log['counter_id']}")
            print(f"   Источник логов: {'визиты (visits)' if log['source'] == 'visits' else 'показы (hits)'}")
            print(f"   Даты запроса: {log['date1'].replace('-', '.')} - {log['date2'].replace('-', '.')}")
            print(f"   Статус запроса: {__class__.STATUS[log['status']]}")
        if not logs:
            print('На сервере нет запросов.')
        return __class__.start(self)
    
    # удаление запросов на сервере
    def clean_requests(self):
        url = f'https://api-metrika.yandex.ru/management/v1/counter/{self.counterId}/logrequests'
        logs = json.loads(requests.get(url,
                                      headers={"Authorization": f'OAuth {self.token}'}).text)['requests']
        request_id = [log['request_id'] for log in logs]
        if not request_id:
            return 'На сервере нет запросов.'
        print(f"Список запросов логов хранящихся на сервере: ", ", ".join(map(str, request_id)))
        while True:
            answer = str(input("Введите id запроса для удаления или введите 'all' для удаления всех запросов: ")).lower().strip()
            if (answer in ['a', 'all']) or (int(answer) in request_id):
                break
            if answer in ['exit', '0']:
                return __class__.start(self)
            else:
                print("Введите идентификатор запроса из списка или укажите значение 'all'." )
        if (answer in ['a', 'all']) or (int(answer) in request_id):
            request_id = request_id if answer in ['a', 'all'] else [answer]
            for requestId in request_id:
                url = f'https://api-metrika.yandex.ru/management/v1/counter/{self.counterId}/logrequest/{requestId}/clean?'
                post = requests.post(url,
                                     headers={"Authorization": f'OAuth {self.token}'})
                print(f'Запрос id {requestId} удален.')
        else:
            print(f'Вы ввели неправильный идентификатор запроса.')
        return __class__.start(self)
    
    # создание запроса на сервере
    def make_request(self):
        self.fields_hits = 'ym:pv:watchID,ym:pv:counterID,ym:pv:date,ym:pv:dateTime,ym:pv:title,ym:pv:URL,ym:pv:referer,ym:pv:UTMCampaign,ym:pv:UTMContent,ym:pv:UTMMedium,ym:pv:UTMSource,ym:pv:UTMTerm,ym:pv:browser,ym:pv:browserMajorVersion,ym:pv:browserMinorVersion,ym:pv:browserCountry,ym:pv:browserEngine,ym:pv:browserEngineVersion1,ym:pv:browserEngineVersion2,ym:pv:browserEngineVersion3,ym:pv:browserEngineVersion4,ym:pv:browserLanguage,ym:pv:clientTimeZone,ym:pv:cookieEnabled,ym:pv:deviceCategory,ym:pv:flashMajor,ym:pv:flashMinor,ym:pv:from,ym:pv:hasGCLID,ym:pv:GCLID,ym:pv:ipAddress,ym:pv:javascriptEnabled,ym:pv:mobilePhone,ym:pv:mobilePhoneModel,ym:pv:openstatAd,ym:pv:openstatCampaign,ym:pv:openstatService,ym:pv:openstatSource,ym:pv:operatingSystem,ym:pv:operatingSystemRoot,ym:pv:physicalScreenHeight,ym:pv:physicalScreenWidth,ym:pv:regionCity,ym:pv:regionCountry,ym:pv:regionCityID,ym:pv:regionCountryID,ym:pv:screenColors,ym:pv:screenFormat,ym:pv:screenHeight,ym:pv:screenOrientation,ym:pv:screenWidth,ym:pv:windowClientHeight,ym:pv:windowClientWidth,ym:pv:params,ym:pv:lastTrafficSource,ym:pv:lastSearchEngine,ym:pv:lastSearchEngineRoot,ym:pv:lastAdvEngine,ym:pv:artificial,ym:pv:pageCharset,ym:pv:link,ym:pv:download,ym:pv:notBounce,ym:pv:lastSocialNetwork,ym:pv:httpError,ym:pv:clientID,ym:pv:networkType,ym:pv:lastSocialNetworkProfile,ym:pv:goalsID,ym:pv:shareService,ym:pv:shareURL,ym:pv:shareTitle,ym:pv:iFrame'
        self.fields_visits ='ym:s:visitID,ym:s:counterID,ym:s:watchIDs,ym:s:date,ym:s:dateTime,ym:s:dateTimeUTC,ym:s:isNewUser,ym:s:startURL,ym:s:endURL,ym:s:pageViews,ym:s:visitDuration,ym:s:bounce,ym:s:ipAddress,ym:s:regionCountry,ym:s:regionCity,ym:s:regionCountryID,ym:s:regionCityID,ym:s:params,ym:s:clientID,ym:s:networkType,ym:s:goalsID,ym:s:goalsSerialNumber,ym:s:goalsDateTime,ym:s:goalsPrice,ym:s:goalsOrder,ym:s:goalsCurrency,ym:s:lastTrafficSource,ym:s:lastAdvEngine,ym:s:lastReferalSource,ym:s:lastSearchEngineRoot,ym:s:lastSearchEngine,ym:s:lastSocialNetwork,ym:s:lastSocialNetworkProfile,ym:s:referer,ym:s:lastDirectClickOrder,ym:s:lastDirectBannerGroup,ym:s:lastDirectClickBanner,ym:s:lastDirectClickOrderName,ym:s:lastClickBannerGroupName,ym:s:lastDirectClickBannerName,ym:s:lastDirectPhraseOrCond,ym:s:lastDirectPlatformType,ym:s:lastDirectPlatform,ym:s:lastDirectConditionType,ym:s:lastCurrencyID,ym:s:from,ym:s:UTMCampaign,ym:s:UTMContent,ym:s:UTMMedium,ym:s:UTMSource,ym:s:UTMTerm,ym:s:openstatAd,ym:s:openstatCampaign,ym:s:openstatService,ym:s:openstatSource,ym:s:hasGCLID,ym:s:lastGCLID,ym:s:firstGCLID,ym:s:lastSignificantGCLID,ym:s:browserLanguage,ym:s:browserCountry,ym:s:clientTimeZone,ym:s:deviceCategory,ym:s:mobilePhone,ym:s:mobilePhoneModel,ym:s:operatingSystemRoot,ym:s:operatingSystem,ym:s:browser,ym:s:browserMajorVersion,ym:s:browserMinorVersion,ym:s:browserEngine,ym:s:browserEngineVersion1,ym:s:browserEngineVersion2,ym:s:browserEngineVersion3,ym:s:browserEngineVersion4,ym:s:cookieEnabled,ym:s:javascriptEnabled,ym:s:flashMajor,ym:s:flashMinor,ym:s:screenFormat,ym:s:screenColors,ym:s:screenOrientation,ym:s:screenWidth,ym:s:screenHeight,ym:s:physicalScreenWidth,ym:s:physicalScreenHeight,ym:s:windowClientWidth,ym:s:windowClientHeight,ym:s:purchaseID,ym:s:purchaseDateTime,ym:s:purchaseAffiliation,ym:s:purchaseRevenue,ym:s:purchaseTax,ym:s:purchaseShipping,ym:s:purchaseCoupon,ym:s:purchaseCurrency,ym:s:purchaseProductQuantity,ym:s:productsPurchaseID,ym:s:productsID,ym:s:productsName,ym:s:productsBrand,ym:s:productsCategory,ym:s:productsCategory1,ym:s:productsCategory2,ym:s:productsCategory3,ym:s:productsCategory4,ym:s:productsCategory5,ym:s:productsVariant,ym:s:productsPosition,ym:s:productsPrice,ym:s:productsCurrency,ym:s:productsCoupon,ym:s:productsQuantity,ym:s:impressionsURL,ym:s:impressionsDateTime,ym:s:impressionsProductID,ym:s:impressionsProductName,ym:s:impressionsProductBrand,ym:s:impressionsProductCategory,ym:s:impressionsProductCategory1,ym:s:impressionsProductCategory2,ym:s:impressionsProductCategory3,ym:s:impressionsProductCategory4,ym:s:impressionsProductCategory5,ym:s:impressionsProductVariant,ym:s:impressionsProductPrice,ym:s:impressionsProductCurrency,ym:s:impressionsProductCoupon,ym:s:offlineCallTalkDuration,ym:s:offlineCallHoldDuration,ym:s:offlineCallMissed,ym:s:offlineCallTag,ym:s:offlineCallFirstTimeCaller,ym:s:offlineCallURL'
        # выбираем тип источника запроса
        while True:
            self.sourсe = str(input("Укажите источник запроса:\n'1' - визиты (visits)\n'2' - показы (hits): "))
            if self.sourсe in ['1','2']:
                self.fields = self.fields_visits if self.sourсe == '1' else self.fields_hits
                break
            if self.sourсe in ['exit', '0']:
                return __class__.start(self)
            else:
                print("Неверный ввод. Доступные варианты '1'(визиты) или '2'(показы)")
        # задаем даты запроса
        self.dates = []
        while len(self.dates) < 2:
            dt = str(input(f"Укажите {'конечную' if len(self.dates) else 'начальную'} дату в формате 'ГГГГ-ММ-ДД': "))
            y,m,d = dt.split('-')
            try:
                newDate = datetime.datetime(int(d),int(m),int(m))
                self.dates.append(dt)
            except:
                print('Вы ввели некорректную дату!')
        self.dt1, self.dt2 = self.dates
        # формируем url для запроса к API и создаем POST запрос
        url = f'https://api-metrika.yandex.ru/management/v1/counter/{self.counterId}/logrequests?&date1={self.dt1}&date2={self.dt2}&fields={self.fields}&source={"visits" if self.sourсe == "1" else "hits"}'
        post = requests.post(url,
                             headers={"Authorization": f'OAuth {self.token}'})
        logs = json.loads(post.text)
        print(f"Cоздан запрос id: {logs['log_request']['request_id']}, со статусом: {logs['log_request']['status']} ({__class__.STATUS[logs['log_request']['status']]})")
        return __class__.start(self)
    
    # записать сохранненый в виде DataFrame в Excel файл
    def write_excel(self):
        url = f'https://api-metrika.yandex.ru/management/v1/counter/{self.counterId}/logrequests?'
        logs = json.loads(requests.get(url,
                                       headers={"Authorization": f'OAuth {self.token}'}).text)['requests']
        request_id_source = [f"{log['request_id']}({log['source']})" for log in logs]
        request_id = [log['request_id'] for log in logs]
        if not request_id:
            return 'На сервере нет запросов.'
        print(f"Список запросов логов хранящихся на сервере: ", ", ".join(map(str, request_id_source)))
        while True:
            answer = str(input("Введите id запроса для записи данных в excel файл (из списка): ")).lower().strip()
            if int(answer) in request_id:
                break
            if answer in ['exit', '0']:
                return __class__.start(self)
            else:
                print("Некорректный ввод. Введите идентификатор запроса из списка.")
        log = [log for log in logs if log['request_id'] == int(answer)][0]
        head_hits = ['Идентификатор просмотра','Номер счетчика','Дата события','Дата и время события','Заголовок страницы','Адрес страницы','Реферер','UTM Campaign','UTM Content','UTM Medium','UTM Source','UTM Term','Браузер','Major-версия браузера','Minor-версия браузера','Страна браузера','Движок браузера','Major-версия движка браузера','Minor-версия движка браузера','Build-версия движка браузера','Revision-версия движка браузера','Язык браузера','Часовой пояс на компьютере посетителя','Наличие Cookie','Тип устройства. Возможные значения: 1 — десктоп, 2 — мобильные телефоны, 3 — планшеты, 4 — TV','Major-версия Flash. Может принимать значение 0, если у посетителя не поддерживается Flash','Minor-версия Flash','Метка from','Наличие GCLID','GCLID','IP адрес','Наличие JavaScript','Производитель устройства','Модель устройства','Openstat Ad','Openstat Campaign','Openstat Service','Openstat Source','Операционная система (детально)','Группа операционных систем','Физическая высота','Физическая ширина','Город (английское название)','Страна (ISO)','ID города','ID страны','Глубина цвета','Соотношение сторон','Логическая высота','Ориентация экрана','Логическая ширина','Высота окна','Ширина окна','Параметры. Одинарные кавычки дополнительно экранируются как \\u0027','Источник трафика','Поисковая система (детально)','Поисковая система','Рекламная система','Искусственный хит, переданный с помощью функций hit(), event() и пр.','Кодировка страницы сайта','Переход по ссылке','Загрузка файла','Специальное событие «неотказ» (для точного показателя отказов)','Социальная сеть','Код ошибки','Идентификатор пользователя на сайте','Тип соединения','Страница социальной сети, с которой был переход','Идентификаторы достигнутых целей','Кнопка «Поделиться», имя сервиса','Кнопка «Поделиться», URL','Кнопка «Поделиться», заголовок страницы','Просмотр из iframe']
        head_visits =['Идентификатор визита','Номер счетчика','Просмотры, которые были в данном визите. Ограничение массива — 500 просмотров','Дата визита','Дата и время визита','Unix timestamp времени первого хита','Первый визит посетителя','Страница входа','Страница выхода','Глубина просмотра (детально)','Время на сайте (детально)','Отказность','IP адрес','Страна (ISO)','Город (английское название)','ID страны','ID города','Параметры визита. Одинарные кавычки дополнительно экранируются как \\u0027','Идентификатор пользователя на сайте','Тип соединения','Идентификатор целей, достигнутых за данный визит','Порядковые номера достижений цели с конкретным идентификатором','Время достижения каждой цели','Ценность цели','Идентификатор заказов','Идентификатор валюты','Источник трафика','Рекламная система','Переход с сайтов','Поисковая система','Поисковая система (детально)','Cоциальная сеть','Группа социальной сети','Реферер','Кампания Яндекс.Директа','Группа объявлений','Объявление Яндекс.Директа','Название кампании Яндекс.Директа','Название группы объявлений','Название объявления Яндекс.Директа','Условие показа объявления','Тип площадки','Площадка','Тип условия показа объявления','Валюта','Метка from','UTM Campaign','UTM Content','UTM Medium','UTM Source','UTM Term','Openstat Ad','Openstat Campaign','Openstat Service','Openstat Source','Наличие метки GCLID','GCLID последнего визита','GCLID первого визита','GCLID последнего значимого визита','Язык браузера','Страна браузера','Часовой пояс на компьютере посетителя','Тип устройства. Возможные значения: 1 — десктоп, 2 — мобильные телефоны, 3 — планшеты, 4 — TV','Производитель устройства','Модель устройства','Группа операционных систем','Операционная система (детально)','Браузер','Major-версия браузера','Minor-версия браузера','Движок браузера','Major-версия движка браузера','Minor-версия движка браузера','Build-версия движка браузера','Revision-версия движка браузера','Наличие Cookie','Наличие JavaScript','Старший номер версии Flash. Может принимать значение 0, если у посетителя не поддерживается Flash','Младший номер версии Flash','Соотношение сторон','Глубина цвета','Ориентация экрана','Логическая ширина','Логическая высота','Физическая ширина','Физическая высота','Ширина окна','Высота окна','Идентификатор покупки','Дата и время покупки','Магазин или филиал, в котором произошла транзакция','Полученный доход','Сумма всех налогов, связанных с транзакцией','Стоимость доставки, связанная с транзакцией','Промокод, ассоциированный со всей покупкой целиком','Валюта','Количество товаров в покупке','Идентификатор покупки','Идентификатор товара','Название товара','Производитель товара','Категория, к которой относится товар','Категория, к которой относится товар, уровень 1','Категория, к которой относится товар, уровень 2','Категория, к которой относится товар, уровень 3','Категория, к которой относится товар, уровень 4','Категория, к которой относится товар, уровень 5','Разновидность товара','Положение товара в списке','Цена товара','Валюта товара','Промокод ассоциированный с товаром','Количество товара','URL страницы с товаром','Дата и время просмотра','Идентификатор просмотренного товара','Название просмотренного товара','Производитель просмотренного товара','Категория, к которой относится просмотренный товар','Категория, к которой относится просмотренный товар, уровень 1','Категория, к которой относится просмотренный товар, уровень 2','Категория, к которой относится просмотренный товар, уровень 3','Категория, к которой относится просмотренный товар, уровень 4','Категория, к которой относится просмотренный товар, уровень 5','Разновидность просмотренного товара','Цена просмотренного товара','Валюта для товара','Промокод ассоциированный с просмотренным товаром','Длительность звонка в секундах','Длительность ожидания звонка в секундах','Пропущен ли звонок','Произвольная метка','Первичный ли звонок','URL, с которого был звонок (ассоциированная с событием страница)']
        fields = head_visits if log['source'] == 'visits' else head_hits
        requestId, counterId = log['request_id'], log['counter_id']
        url = f'https://api-metrika.yandex.net/management/v1/counter/{self.counterId}/logrequest/{requestId}/part/0/download'
        r = requests.get(url, 
                         headers={"Authorization": f'OAuth {self.token}'})
        data = [x.split('\t') for x in r.content.decode('utf-8').split('\n')[:-1]]
        df_ym = pd.DataFrame(data[1:], columns = fields)                     
        file_name = log['source'] + '_' + str(requestId) + '_' + log['date1'].replace('-','') + '_' + log['date2'].replace('-','') + '.xlsx'
        writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
        df_ym.to_excel(writer, sheet_name=f'request_id_{requestId}')
        writer.save()
        print(f"Лист 'request_id_{requestId}' записан в исходный файл '{file_name}'.")
        return __class__.start(self)