# -*- coding: utf-8 -*-
# Distributed under the terms of the GNU General Public License v2
import re
import subprocess

__all__ = [
    'extract_bash_file_vars',
]


def extract_bash_file_vars(path, output_vars, context=None):
    context = context or {}
    proc = subprocess.Popen(
        ['bash', '-c', 'source {} && set'.format(path)],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=context)

    raw_vars = {}
    var_re = re.compile('^({})='.format('|'.join(output_vars)))
    for line in proc.stdout:
        if not var_re.search(line.decode('utf-8')):
            continue
        key, _, value = line.partition(b'=')
        key = key.decode('ascii')
        raw_vars[key] = value

    proc.communicate()

    cleaned_vars = {}
    for k, v in raw_vars.items():
        v = re.sub(rb'\n$', b'', v)
        v = re.sub(rb"^\$?'(.*)'$", rb'\1', v)
        cleaned_vars[k] = v.decode('unicode_escape')
    return cleaned_vars
