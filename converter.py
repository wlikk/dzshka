import sys
import argparse
import toml


def parse_config(text):
    data = {}
    lines = text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Пропускаем комментарии
        if line.startswith('*>'):
            i += 1
            continue

        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip()

            # Обработка строк
            if val.startswith('"') and val.endswith('"'):
                data[key] = val[1:-1]
            # Обработка структур
            elif val.startswith('struct'):
                # Собираем многострочную структуру
                struct_lines = [val]
                while i < len(lines) - 1 and '}' not in struct_lines[-1]:
                    i += 1
                    struct_lines.append(lines[i])

                struct_text = '\n'.join(struct_lines)
                data[key] = parse_struct(struct_text)
            elif val.isdigit() or (val[0] == '-' and val[1:].isdigit()):
                # Обработка чисел
                data[key] = int(val)
            else:
                data[key] = val

        i += 1

    return data


def parse_struct(text):
    struct = {}
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if line.startswith('struct{') or line.startswith('struct'):
            continue
        if line.startswith('}'):
            break
        if '=' in line:
            key, val = line.split('=', 1)
            key = key.strip().rstrip(',')
            val = val.strip().rstrip(',')

            if val.startswith('"') and val.endswith('"'):
                struct[key] = val[1:-1]
            elif val.isdigit() or (val[0] == '-' and val[1:].isdigit()):
                # Преобразуем в число
                struct[key] = int(val)
            elif val.lower() == 'true':
                struct[key] = True
            elif val.lower() == 'false':
                struct[key] = False
            else:
                # Пробуем как float
                try:
                    struct[key] = float(val)
                except ValueError:
                    struct[key] = val

    return struct


def main():
    parser = argparse.ArgumentParser(
        description='Конвертер учебного конфигурационного языка в TOML'
    )
    parser.add_argument('-o', '--output', required=True,
                        help='Путь к выходному файлу TOML')

    args = parser.parse_args()

    # Читаем из stdin
    input_text = sys.stdin.read()

    # Парсим конфигурацию
    config = parse_config(input_text)

    # Записываем в TOML
    with open(args.output, 'w', encoding='utf-8') as f:
        toml.dump(config, f)

    print(f"Конфигурация сохранена в {args.output}")


if __name__ == '__main__':
    main()