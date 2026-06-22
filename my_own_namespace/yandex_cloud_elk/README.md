# Yandex Cloud ELK Collection

Коллекция `my_own_namespace.yandex_cloud_elk` предоставляет модуль и роль для создания текстовых файлов.

## Требования

- Ansible 2.14+ (рекомендуется, работает с текущей devel-версией)
- Python 3.10+ на управляемом хосте

## Содержимое коллекции

### Модуль `my_own_module`

Создаёт текстовый файл по заданному пути с указанным содержимым.

**Параметры:**
| Параметр   | Тип    | Обязательный | По умолчанию | Описание                                                                 |
|------------|--------|--------------|--------------|--------------------------------------------------------------------------|
| `path`     | `str`  | да           | –            | Путь к создаваемому файлу.                                               |
| `content`  | `str`  | да           | –            | Содержимое файла.                                                        |
| `force`    | `bool` | нет          | `false`      | Если `true`, файл будет перезаписан, даже если он уже существует.       |

**Примеры:**
```yaml
- name: Create a file
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/example.txt
    content: "Hello, World!"
    force: true

- name: Try to create without force (idempotent)
  my_own_namespace.yandex_cloud_elk.my_own_module:
    path: /tmp/example.txt
    content: "Will not overwrite if exists"
```
Возвращаемые значения:

original_message (str) – переданное содержимое.

message (str) – результат операции.

Роль file_creator
Использует модуль my_own_module для создания файла с параметрами, заданными через переменные.

Переменные роли:

ПеременнаяЗначение по умолчаниюОписание
file_path/tmp/default_output.txtПуть к создаваемому файлу.
file_content"Default content"Содержимое файла.
file_forcefalseПринудительная перезапись.
Пример playbook:

yaml
- name: Use file_creator role
  hosts: localhost
  connection: local
  roles:
    - role: my_own_namespace.yandex_cloud_elk.file_creator
      vars:
        file_path: "/tmp/custom.txt"
        file_content: "Custom content"
        file_force: true
Установка
bash
ansible-galaxy collection install git+https://github.com/MustWay-byte/my_own_collection.git
Лицензия
MIT
