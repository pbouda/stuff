# -*- coding: utf-8 -*-

import os
from distutils.core import setup

target_dir = 'share'
data_files = []

# Übersetzungsdateien hinzufügen
#translation_files = []
#for qmfile in glob.glob('data/locale/*.qm'):
#    qmdir = os.path.dirname(qmfile).replace('data', target_dir + '/helloworld')
#    translation_files.append((qmdir, [qmfile]))

data_files += [
    (os.path.join(target_dir, 'applications'), ['data/helloworld.desktop'])]

setup(
    name             = 'helloworld',
    version          = '1.0',
    description      = 'Hello World Software',
    author           = 'Peter Bouda',
    author_email     = 'pbouda@dasskript.com',
    url              = 'http://www.dasskript.com',
    package_dir      = { '':'src' },
    packages         = [ 'helloworld', "helloworld.ui" ],
    scripts          = [ 'bin/helloworld' ],
    long_description = 'Hello World is a software that greets the world in a unique way.',
    data_files       = data_files
)
