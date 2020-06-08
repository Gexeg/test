## Задача

Перенести тестовую базу кандидатов из Экселя и файлов в Хантфлоу, используя [Хантфлоу API](https://github.com/huntflow/api). 

## Решение

Запуск скрипта производится через main.py

```bash
$ python main.py -t=<token> -bd=<path_to_directory>
```

Из командной строки можно передать 3 аргумента:

- токен для доступа к апи (обязательный)
- путь к директории с файлами (обязательный)
- строку, с которой необходимо начать обработку файла (опциональный)

Чтобы можно было определить, на какой строке произошла ошибка, добавил запись в лог.

## Вопросы

В коде отметил несколько `TODO` моментов: 

- Приоритетность источников (что приоритетнее эксель файл или информация распознанная из резюме?).
- Наименование статусов или этапов собеседований. В файле задания и примерах есть этапы на русском, но в ответе приходят только на английском. Нужно дополнять таблицу соответствий или  статусы будут поменяны в источнике?
- Имя файла с базой имеет значение? В составе задачи оно выделено, но не поставлено в аргументы командной строки. Выделять его в отдельный конфиг немного странно, пока оно висит переменной.

Натолкнулся на проблему с распознаванием файлов. `.doc` - не распознает корректную вакансию в резюме. На данный момент проблема не решена, не хватает понимания процесса, в какую сторону двигаться дальше (настраивать валидацию результата от распознавателя или все-таки проблема в запросе).

## Развитие

По ощущениям для оценки кода объем достаточный. Для дальнейшего развития нужно больше вникнуть в процесс, навскидку сейчас вижу следующие моменты:

- Покрыть код тестами
- Добавить валидацию
- Добавить алертинг