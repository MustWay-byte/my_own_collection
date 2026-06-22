# My Own Collection

Репозиторий содержит несколько Ansible-коллекций, разработанных в рамках учебного курса.

## Коллекции

### my_own_namespace.yandex_cloud_elk
- **Модуль `my_own_module`** – создаёт текстовый файл по заданному пути с указанным содержимым.
- **Роль `file_creator`** – использует модуль `my_own_module` с параметрами по умолчанию.
- Документация: см. `my_own_namespace/yandex_cloud_elk/README.md`

### my_org.my_collection (устаревшая, оставлена для истории)
- Первая версия коллекции с аналогичным модулем.

## Использование

```bash
ansible-galaxy collection install git+https://github.com/MustWay-byte/my_own_collection.git
```
