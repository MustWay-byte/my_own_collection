# My Own Collection

Репозиторий содержит несколько Ansible-коллекций, разработанных в рамках учебного курса.  
Основная коллекция – `my_own_namespace.yandex_cloud_elk` – включает модуль `my_own_module` и роль `file_creator` для создания текстовых файлов.

## Содержимое

- **Коллекция `my_own_namespace.yandex_cloud_elk`**  
  * модуль `my_own_module` – создаёт файлы с проверкой идемпотентности и поддержкой `check_mode`  
  * роль `file_creator` – использует модуль с предустановленными параметрами  

- **Playbook'и для тестирования** – лежат в `playbook/`  
  * `test_module.yml` – single-task вызов модуля  
  * `use_role.yml` – вызов роли `file_creator`  
  * `idempotency_test.yml` – проверка идемпотентности  

## Установка коллекции

```bash
ansible-galaxy collection install git+https://github.com/MustWay-byte/my_own_collection.git
```

## Документация

Подробное описание модуля и роли находится в [README коллекции](ansible_collections/my_own_namespace/yandex_cloud_elk/README.md).

## Лицензия

MIT

## Ссылки

- Репозиторий: [https://github.com/MustWay-byte/my_own_collection](https://github.com/MustWay-byte/my_own_collection)
- Тег `1.0.0`: [https://github.com/MustWay-byte/my_own_collection/releases/tag/1.0.0](https://github.com/MustWay-byte/my_own_collection/releases/tag/1.0.0)
