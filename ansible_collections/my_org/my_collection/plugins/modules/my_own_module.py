#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2026, MustWay
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module

short_description: Создаёт текстовый файл с заданным содержимым

version_added: "1.0.0"

description:
    - Модуль создаёт файл по указанному пути и записывает в него переданный контент.
    - Если файл уже существует, используется параметр force для перезаписи.
    - Поддерживает check_mode.

options:
    path:
        description: Путь к создаваемому файлу.
        required: true
        type: str
    content:
        description: Содержимое файла.
        required: true
        type: str
    force:
        description: Перезаписать файл, если он существует.
        required: false
        type: bool
        default: false

author:
    - MustWay
'''

EXAMPLES = r'''
- name: Создать приветственный файл
  my_org.my_collection.my_own_module:
    path: /tmp/hello.txt
    content: "Hello, World!"

- name: Перезаписать существующий файл
  my_org.my_collection.my_own_module:
    path: /tmp/hello.txt
    content: "New content"
    force: true
'''

RETURN = r'''
original_message:
    description: Исходное содержимое, переданное в параметре content.
    type: str
    returned: always
    sample: "Hello, World!"
message:
    description: Сообщение о результате выполнения.
    type: str
    returned: always
    sample: "Файл /tmp/hello.txt успешно создан/перезаписан."
'''

import os
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        force=dict(type='bool', default=False),
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    force = module.params['force']

    result['original_message'] = content

    # Если файл существует и force не установлен, завершаем без изменений
    if os.path.exists(path) and not force:
        result['message'] = f'Файл {path} уже существует. Используйте force=true для перезаписи.'
        module.exit_json(**result)

    # Режим проверки (check mode) – только сообщаем, что было бы сделано
    if module.check_mode:
        result['changed'] = True
        result['message'] = f'Файл {path} был бы создан/перезаписан (check mode).'
        module.exit_json(**result)

    # Создание или перезапись файла
    try:
        with open(path, 'w') as f:
            f.write(content)
        result['changed'] = True
        result['message'] = f'Файл {path} успешно создан/перезаписан.'
    except Exception as e:
        module.fail_json(msg=f'Ошибка при записи файла: {str(e)}', **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
