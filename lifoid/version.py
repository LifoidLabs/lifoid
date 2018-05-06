# version
#
# Author:   Romary Dupuis <romary@me.com>
#
# Copyright (C) 2017-2018 Romary Dupuis

"""
Stores version information such that it can be read by setuptools.
"""

__version_info__ = {
    'major': 0,
    'minor': 1,
    'micro': 0,
    'releaselevel': 'alpha',
    'serial': 0,
}


def get_version(short=False):
    """
    Computes a string representation of the version from __version_info__.
    """
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ["%(major)i.%(minor)i" % __version_info__, ]
    if __version_info__['micro']:
        vers.append(".%(micro)i" % __version_info__)
    if __version_info__['releaselevel'] != 'final' and not short:
        vers.append('%s%i' % (__version_info__['releaselevel'][0],
                              __version_info__['serial']))
    return ''.join(vers)


if __name__ == '__main__':
    print('version {}'.format(get_version()))
