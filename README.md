# Конфигурационный конвертер (Вариант 9)

## Описание
Программа конвертирует файлы из учебного конфигурационного языка в формат TOML.

## Установка
```bash
pip install toml
```

## Использование
```bash
python converter.py -o результат.toml < входной_файл.conf
```

## Примеры
```bash
# Тестирование
python test_converter.py

# Конвертация примеров
python converter.py -o server.toml < example1.conf
python converter.py -o database.toml < example2.conf
python converter.py -o app.toml < example3.conf
```

## Структура файлов
- `converter.py` - основной скрипт
- `test_converter.py` - тесты
- `example1.conf`, `example2.conf`, `example3.conf` - примеры

## Язык поддерживает
- Комментарии: `*> текст`
- Строки: `"текст"`
- Числа: `123`, `3.14`
- Структуры: `struct {ключ = значение}`
- Константы: `имя: значение`