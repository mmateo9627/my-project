#!/bin/python3

import re
import os

root = r'/home/mmarkiel/GIT/xyz'


def main():
    for dirpath, subdirs, files in os.walk(root):
        if dirpath != root:
            if subdirs != root:
                for f in files:
                    if f.endswith('terragrunt.hcl'):
                        print(f"Patch: ", os.path.join(dirpath, f))
                        path = os.path.join(dirpath, f)
                        terragrunt_patch(path)


def terragrunt_patch(path):
    with open(path, "r") as f:
        data = f.read()
    added_data = '''
  after_hook "post_component_info" {
    commands = ["apply"]
    execute  = ["${get_parent_terragrunt_dir()}/../infra-release-notification.sh", local.component, local.tag, get_aws_caller_identity_arn()]
  }'''
    new_data = ()
    if 'after_hook "post_component_info' in data:
        print('alredy in file')
    else:
        new_data = re.sub('(before_hook "tag_version" {[^}]*})', r'\1' + f'\n{added_data}', data)
        # print(new_data)
        # REMOVE ME TO WORK
        # return
        with open(path, "w") as f:
            f.write(new_data)


