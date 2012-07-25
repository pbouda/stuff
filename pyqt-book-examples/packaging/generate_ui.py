# -*- coding: utf-8 -*-

import sys, os
from subprocess import call

if sys.platform == "win32":
    bindir = "c:/Python27/Lib/site-packages/PyQt4/bin"
else:
    bindir = "/usr/bin"

uic_path = os.path.join(bindir, "pyuic4")
rcc_path = os.path.join(bindir, "pyrcc4")
    
ui_path = "ui"
rc_path = ""
out_path = "src/helloworld/ui"

ui_files = { "helloworld.ui": "ui_helloworld.py" }
rc_files = { "helloworld.qrc": "helloworld_rc.py" }

for file in ui_files:
    file_path = os.path.join(ui_path, file)
    out_file_path = os.path.join(out_path, ui_files[file])
    call([uic_path, file_path, "-o", out_file_path])
    
for file in rc_files:
    file_path = os.path.join(rc_path, file)
    out_file_path = os.path.join(out_path, rc_files[file])
    call([rcc_path, file_path, "-o", out_file_path])
