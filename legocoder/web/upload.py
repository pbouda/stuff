#!/usr/bin/python
"""This demonstrates a minimal http upload cgi.
This allows a user to upload up to three files at once.
It is trivial to change the number of files uploaded.

This script has security risks. A user could attempt to fill
a disk partition with endless uploads. 
If you have a system open to the public you would obviously want
to limit the size and number of files written to the disk.
"""
import cgi
import cgitb; cgitb.enable()
import os, sys
import time

UPLOAD_DIR = "/var/www/tmp"

HTML_TEMPLATE = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html><head><title>File Upload</title>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<script type="text/javascript">
<!--
window.location = "index.html?filename=%(FILENAME)s"
//-->
</script>
</head><body>
<h1>File Upload</h1>
File upload complete. Redirect to <a href="index.html?filename=%(FILENAME)s">Lego Coding</a>.
</body>
</html>"""

def print_html_form(filename):
    """This prints out the html form. Note that the action is set to
      the name of the script which makes this is a self-posting form.
      In other words, this cgi both displays a form and processes it.
    """
    print "content-type: text/html\n"
    print HTML_TEMPLATE % {'FILENAME':filename}

def save_uploaded_file (form_field, upload_dir):
    """This saves a file uploaded by an HTML form.
       The form_field is the name of the file input field from the form.
       For example, the following form_field would be "file_1":
           <input name="file_1" type="file">
       The upload_dir is the directory where the file will be written.
       If no file was uploaded or if the field does not exist then
       this does nothing.
    """
    form = cgi.FieldStorage()
    if not form.has_key(form_field): return
    fileitem = form[form_field]
    _, fileextension = os.path.splitext(fileitem.filename) 

    filename = "image_{0}{1}".format(int(time.time()), fileextension)
    if not fileitem.file: return
    fout = file (os.path.join(upload_dir, filename), 'wb')
    while 1:
        chunk = fileitem.file.read(100000)
        if not chunk: break
        fout.write (chunk)
    fout.close()
    return filename

filename = save_uploaded_file ("imagefile", UPLOAD_DIR)

print_html_form(filename)
## end of http://code.activestate.com/recipes/273844/ }}}
