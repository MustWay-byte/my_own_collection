#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r'''
---
module: yc_compute_instance

short_description: Создаёт ВМ в Yandex Cloud или получает inventory

description:
    - Создаёт виртуальную машину в Yandex Cloud или возвращает список ВМ в формате inventory.
    - Поддерживает state: present (создание) и state: list (получение inventory).

options:
    name:
        description: Имя ВМ (для state=present).
        required: false
        type: str
    folder_id:
        description: ID каталога.
        required: false
        type: str
    zone:
        description: Зона доступности.
        required: false
        type: str
        default: ru-central1-a
    platform:
        description: Платформа.
        required: false
        type: str
        default: standard-v2
    cores:
        description: Количество vCPU.
        required: false
        type: int
        default: 2
    memory:
        description: Объём RAM в ГБ.
        required: false
        type: int
        default: 2
    image_family:
        description: Семейство образов.
        required: false
        type: str
        default: ubuntu-2204-lts
    image_folder_id:
        description: ID папки с образами.
        required: false
        type: str
        default: standard-images
    subnet_name:
        description: Имя подсети.
        required: false
        type: str
        default: default
    state:
        description: present (создать) или list (получить inventory).
        required: false
        type: str
        default: present
        choices: ['present', 'list']

author:
    - MustWay
'''

EXAMPLES = r'''
- name: Создать ВМ
  my_own_namespace.yandex_cloud_elk.yc_compute_instance:
    name: test-vm
    folder_id: b1g5m6nu8f7nl3dmsjot
    zone: ru-central1-a
    cores: 2
    memory: 2
    image_family: ubuntu-2204-lts
    image_folder_id: standard-images
    subnet_name: default-ru-central1-a

- name: Получить inventory всех ВМ
  my_own_namespace.yandex_cloud_elk.yc_compute_instance:
    state: list
    folder_id: b1g5m6nu8f7nl3dmsjot
'''

RETURN = r'''
inventory:
    description: Inventory в формате Ansible (для state=list).
    type: dict
    returned: when state is list
vm_id:
    description: ID созданной ВМ.
    type: str
    returned: when state is present
vm_name:
    description: Имя созданной ВМ.
    type: str
    returned: when state is present
'''

import subprocess
import json
from ansible.module_utils.basic import AnsibleModule


def run_module():
    module_args = dict(
        name=dict(type='str', required=False),
        folder_id=dict(type='str', default=''),
        zone=dict(type='str', default='ru-central1-a'),
        platform=dict(type='str', default='standard-v2'),
        cores=dict(type='int', default=2),
        memory=dict(type='int', default=2),
        image_family=dict(type='str', default='ubuntu-2204-lts'),
        image_folder_id=dict(type='str', default='standard-images'),
        subnet_name=dict(type='str', default='default'),
        state=dict(type='str', default='present', choices=['present', 'list']),
    )

    result = dict()

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    state = module.params['state']
    name = module.params.get('name')
    folder_id = module.params['folder_id']
    zone = module.params['zone']
    platform = module.params['platform']
    cores = module.params['cores']
    memory = module.params['memory']
    image_family = module.params['image_family']
    image_folder_id = module.params['image_folder_id']
    subnet_name = module.params['subnet_name']

    if state == 'list':
        # Получение списка ВМ в формате inventory
        try:
            cmd = ['yc', 'compute', 'instance', 'list', '--format', 'json']
            if folder_id:
                cmd += ['--folder-id', folder_id]
            output = subprocess.check_output(cmd)
            instances = json.loads(output)
            inventory = {}
            for instance in instances:
                hostname = instance.get('name')
                external_ip = None
                internal_ip = None
                for iface in instance.get('network_interfaces', []):
                    external_ip = iface.get('primary_v4_address', {}).get('one_to_one_nat', {}).get('address')
                    internal_ip = iface.get('primary_v4_address', {}).get('address')
                    break  # берём первый интерфейс
                if hostname:
                    inventory[hostname] = {
                        'ansible_host': external_ip or internal_ip,
                        'ansible_user': 'ubuntu',  # можно сделать настраиваемым
                        'yc_zone': instance.get('zone_id'),
                        'yc_platform': instance.get('platform_id'),
                        'yc_cores': instance.get('resources', {}).get('cores'),
                        'yc_memory': instance.get('resources', {}).get('memory'),
                    }
            result['inventory'] = inventory
            result['changed'] = False
            module.exit_json(**result)
        except subprocess.CalledProcessError as e:
            module.fail_json(msg='Ошибка получения списка ВМ: {}'.format(e.output.decode()))

    # state == 'present'
    # Проверка существования
    try:
        check_cmd = ['yc', 'compute', 'instance', 'get', '--name', name]
        if folder_id:
            check_cmd += ['--folder-id', folder_id]
        subprocess.check_output(check_cmd, stderr=subprocess.STDOUT)
        result['vm_name'] = name
        result['changed'] = False
        module.exit_json(**result)
    except subprocess.CalledProcessError:
        pass

    if module.check_mode:
        result['changed'] = True
        result['vm_name'] = name
        module.exit_json(**result)

    # Создание
    try:
        create_cmd = [
            'yc', 'compute', 'instance', 'create',
            '--name', name,
            '--zone', zone,
            '--platform', platform,
            '--cores', str(cores),
            '--memory', '{}GB'.format(memory),
            '--create-boot-disk', 'image-family=' + image_family + ',image-folder-id=' + image_folder_id + ',size=20,type=network-hdd',
            '--network-interface', 'subnet-name=' + subnet_name + ',nat-ip-version=ipv4'
        ]
        if folder_id:
            create_cmd += ['--folder-id', folder_id]
        output = subprocess.check_output(create_cmd, stderr=subprocess.STDOUT)
        vm_id = None
        for line in output.decode().splitlines():
            if 'id:' in line:
                vm_id = line.split()[-1]
                break
        result['changed'] = True
        result['vm_id'] = vm_id or 'unknown'
        result['vm_name'] = name
    except subprocess.CalledProcessError as e:
        module.fail_json(msg='Ошибка создания ВМ: {}'.format(e.output.decode()))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
