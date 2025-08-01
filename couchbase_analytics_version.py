#!/usr/bin/env python

#  Copyright 2016-2024. Couchbase, Inc.
#  All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import print_function

import datetime
import os.path
import re
import subprocess
import warnings
from typing import Optional


class CantInvokeGit(Exception):
    pass


class VersionNotFound(Exception):
    pass


class MalformedGitTag(Exception):
    pass


RE_XYZ = re.compile(r'(\d+)\.(\d+)\.(\d+)(?:-(.*))?')

VERSION_FILE = os.path.join(os.path.dirname(__file__), 'couchbase_analytics', '_version.py')


class VersionInfo:
    def __init__(self, rawtext: str):
        self.rawtext = rawtext
        t = self.rawtext.rsplit('-', 2)
        if len(t) != 3:
            raise MalformedGitTag(self.rawtext)

        vinfo, ncommits, self.sha = t
        self.ncommits = int(ncommits)

        # Split up the X.Y.Z
        match = RE_XYZ.match(vinfo)
        if match is not None:
            (self.ver_maj, self.ver_min, self.ver_patch, self.ver_extra) = match.groups()

        # Per PEP-440, replace any 'DP' with an 'a', and any beta with 'b'
        if self.ver_extra:
            self.ver_extra = re.sub(r'^dp', 'dev', self.ver_extra, count=1)
            self.ver_extra = re.sub(r'^alpha', 'a', self.ver_extra, count=1)
            self.ver_extra = re.sub(r'^beta', 'b', self.ver_extra, count=1)
            m = re.search(r'^([ab]|dev|rc|post)\.?(\d+)?', self.ver_extra)
            if m is not None:
                if m.group(1) in ['dev', 'post']:
                    self.ver_extra = '.' + self.ver_extra.replace('.', '')
                if m.group(2) is None:
                    # No suffix, then add the number
                    first = self.ver_extra[0]
                    self.ver_extra = first + '0' + self.ver_extra[1:]

    @property
    def is_final(self) -> bool:
        return self.ncommits == 0

    @property
    def is_prerelease(self) -> bool:
        return self.ver_extra is not None and not self.ver_extra.isspace()

    @property
    def xyz_version(self) -> str:
        return '.'.join((self.ver_maj, self.ver_min, self.ver_patch))

    @property
    def base_version(self) -> str:
        """Returns the actual upstream version (without dev info)"""
        components = [self.xyz_version]
        if self.ver_extra:
            components.append(self.ver_extra)
        return ''.join(components)

    @property
    def package_version(self) -> str:
        """Returns the well formed PEP-440 version"""
        vbase = self.base_version
        if self.ncommits:
            if self.ver_extra:
                vbase += f'+{self.sha}'
            else:
                vbase += f'.dev{self.ncommits}+{self.sha}'
        return vbase


def get_version() -> str:
    """
    Returns the version from the generated version file without actually
    loading it (and thus trying to load the extension module).
    """
    if not os.path.exists(VERSION_FILE):
        raise VersionNotFound(VERSION_FILE + ' does not exist')
    fp = open(VERSION_FILE, 'r')
    vline = None
    for x in fp.readlines():
        x = x.rstrip()
        if not x:
            continue
        if not x.startswith('__version__'):
            continue

        vline = x.split('=')[1]
        break
    if not vline:
        raise VersionNotFound('version file present but has no contents')

    return vline.strip().rstrip().replace("'", '')


def get_git_describe() -> str:
    if not os.path.exists(os.path.join(os.path.dirname(__file__), '.git')):
        raise CantInvokeGit('Not a git build')

    try:
        po = subprocess.Popen(
            ('git', 'describe', '--tags', '--long', '--always'), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
    except OSError as e:
        raise CantInvokeGit(e) from None

    stdout, stderr = po.communicate()
    if po.returncode != 0:
        raise CantInvokeGit("Couldn't invoke git describe", stderr)

    return stdout.decode('utf-8').rstrip()


def gen_version(
    do_write: Optional[bool] = True, txt: Optional[str] = None, update_pyproject: Optional[bool] = False
) -> None:
    """
    Generate a version based on git tag info. This will write the
    couchbase_analytics/_version.py file. If not inside a git tree it will
    raise a CantInvokeGit exception - which is normal
    (and squashed by setup.py) if we are running from a tarball
    """

    if txt is None:
        txt = get_git_describe()

    t = txt.rsplit('-', 2)
    if len(t) != 3:
        only_sha = re.match('[a-z0-9]+', txt)
        if only_sha is not None and only_sha.group():
            txt = f'0.0.1-0-{txt}'

    try:
        info = VersionInfo(txt)
        vstr = info.package_version
    except MalformedGitTag:
        warnings.warn("Malformed input '{0}'".format(txt), stacklevel=2)
        vstr = '0.0.0' + txt

    if not do_write:
        print(vstr)
        return

    lines = (
        '# This file automatically generated by',
        '#    {0}'.format(__file__),
        '# at',
        '#    {0}'.format(datetime.datetime.now().isoformat(' ')),
        "__version__ = '{0}'".format(vstr),
        '',
    )
    with open(VERSION_FILE, 'w') as fp:
        fp.write('\n'.join(lines))

    if update_pyproject is True:
        update_pyproject_version(os.path.join(os.path.dirname(__file__), 'pyproject.toml'), vstr)


# uv does not support a dynamic project version (yet), this is a workaround in the interim
def update_pyproject_version(pyproject_path: str, new_version: str) -> bool:
    import tomli
    import tomli_w  # type: ignore[import-not-found]

    if not os.path.exists(pyproject_path):
        print(f"Error: pyproject.toml file not found at '{pyproject_path}'")
        return False

    try:
        with open(pyproject_path, 'rb') as f:
            data = tomli.load(f)

        if 'project' in data and isinstance(data['project'], dict):
            current_version = data['project'].get('version')
            if current_version == new_version:
                print(f"Version is already '{new_version}'. No update needed.")
                return True

            data['project']['version'] = new_version
            print(f"Updated version from '{current_version}' to '{new_version}' in '{pyproject_path}'")

            # Write the modified content back to the file
            with open(pyproject_path, 'wb') as f:
                tomli_w.dump(data, f)
            return True
        else:
            print(f"Error: '[project]' section not found or is malformed in '{pyproject_path}'.")
            return False

    except tomli.TOMLDecodeError as e:
        print(f"Error: Failed to parse pyproject.toml at '{pyproject_path}'. Invalid TOML format: {e}")
        return False
    except Exception as e:
        print(f'An unexpected error occurred: {e}')
        return False


if __name__ == '__main__':
    from argparse import ArgumentParser

    ap = ArgumentParser(description='Parse git version to PEP-440 version')
    ap.add_argument('-c', '--mode', choices=('show', 'make', 'parse'))
    ap.add_argument('--update-pyproject', help='Update pyproject.toml with the version', action='store_true')
    ap.add_argument('-i', '--input', help='Sample input string (instead of git)')
    options = ap.parse_args()

    cmd = options.mode
    if cmd == 'show':
        print(get_version())
    elif cmd == 'make':
        gen_version(do_write=True, txt=options.input, update_pyproject=options.update_pyproject)
        print(get_version())
    elif cmd == 'parse':
        gen_version(do_write=False, txt=options.input)

    else:
        raise Exception("Command must be 'show' or 'make'")
