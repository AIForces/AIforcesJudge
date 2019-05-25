import os
from pathlib import Path
from os.path import join

IP = "127.0.0.1"
PORT = 3001
RESULT_ENDPOINT = "http://127.0.0.1:3000/judge/receive_data"
TRUSTED_IPS = ['127.0.0.1']
DEBUG = True
BASIC_PATH = str(Path(os.path.dirname(os.path.realpath(__file__))).parent)
SANDBOX_PROFILE_PATH = join(BASIC_PATH, "config/firejail.profile")
PYTHON_VENV_PATH = '/etc/judge/python_venv/bin'

# TODO: add sandboxing of a tmp folder of other workers
SANDBOX = {
    "command": ["firejail", "--profile={}".format(SANDBOX_PROFILE_PATH)],
    "blacklisted_dirs": [
        '/bin',
        # '/usr',
        '/home',
        '/lib32',
        '/sys',
        '/vmlinuz',
        '/boot',
        '/initrd.img',
        '/vmlinuz.old',
        '/dev',
        '/initrd.img.old',
        '/libx32',
        '/opt',
        '/sbin',
        '/lost+found',
        '/srv',
        '/var'
    ],

    "options": [
        'read-only /',
        'disable-mnt',
        'private-etc judge',
        'private-tmp judge',
        'apparmor',
        'caps.drop all',
        'seccomp',
        'memory-deny-write-execute',
        'nonewprivs',
        'noroot',
        'x11 none',
        'nodvd',
        'nogroups',
        'shell none',
        'nodbus',
        'nosound',
        'noautopulse',
        'notv',
        'nou2f',
        'novideo',
        'no3d',
        'net none'
    ],

    "rlimits": [
        'rlimit-as 123456789012',
        'rlimit-cpu 123',
        'rlimit-nproc 0',
        'rlimit-sigpending 0'
    ]
}
