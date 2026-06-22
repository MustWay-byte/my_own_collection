# Yandex Cloud ELK Collection

Коллекция `my_own_namespace.yandex_cloud_elk` предоставляет модуль и роль для создания текстовых файлов на удалённых хостах.

## Требования

- Ansible 2.14+ (рекомендуется; работает с текущей devel-версией)
- Python 3.10+ на управляемом хосте (на control node достаточно 3.8+)

## Содержимое

### Модуль `my_own_module`

Создаёт текстовый файл по заданному пути с указанным содержимым.  
Поддерживает `check_mode` и флаг принудительной перезаписи.

**Параметры:**

| Параметр  | Тип    | Обязательный | По умолчанию | Описание                                                         |
|-----------|--------|--------------|--------------|------------------------------------------------------------------|
| `path`    | `str`  | да           | –            | Абсолютный путь к создаваемому файлу.                            |
| `content` | `str`  | да           | –            | Содержимое, которое будет записано в файл.                       |
| `force`   | `bool` | нет          | `false`      | Если `true`, существующий файл будет перезаписан.               |

**Возвращаемые значения:**

| Поле               | Тип  | Описание                                      |
|--------------------|------|-----------------------------------------------|
| `original_message` | `str`| Переданное содержимое (параметр `content`).   |
| `message`          | `str`| Сообщение о результате выполнения.            |

**Примеры:**

```yaml
- name: Создать файл
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/example.txt
    content: "Hello, World!"
    force: true

- name: Проверить идемпотентность (файл не будет перезаписан)
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/example.txt
    content: "Will not overwrite if exists"
```

## Роль `file_creator`

Использует модуль `my_own_module` для создания файла с параметрами, заданными через переменные.  
Все параметры имеют значения по умолчанию.

### Переменные роли

| Переменная     | По умолчанию               | Описание                              |
|----------------|----------------------------|---------------------------------------|
| `file_path`    | `/tmp/default_output.txt`  | Путь к создаваемому файлу.           |
| `file_content` | `"Default content"`        | Содержимое файла.                     |
| `file_force`   | `false`                    | Перезаписывать ли существующий файл. |

### Пример playbook с ролью

```yaml
- name: Использовать роль file_creator
  hosts: localhost
  connection: local
  roles:
    - role: my_own_namespace.yandex_cloud_elk.file_creator
      vars:
        file_path: "/tmp/custom.txt"
        file_content: "Custom content"
        file_force: true
```

## Установка коллекции

```bash
ansible-galaxy collection install git+https://github.com/MustWay-byte/my_own_collection.git
```

## Лицензия

MIT
