#!/usr/bin/env python

import sys, os
import pickle, base64
from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork

def main(argv):
    app = QtGui.QApplication(argv)
    MainWindow = BrowserWindow()
    MainWindow.show()
    sys.exit(app.exec_())

class BrowserWindow(QtWebKit.QWebView):
    """Das Hauptfenster des Browsers."""

    def __init__(self, *args):
        QtGui.QMainWindow.__init__(self, *args)
        self.resize(400,500)
        self.setWindowTitle("Google Tasks")

        # Cookies laden
        self.cookiejar = QtNetwork.QNetworkCookieJar(self)
        settings = QtCore.QSettings("dasskript.com", "GoogleTasks")
        cookie_list = settings.value("cookies", "").toString()
        if cookie_list != "":
            cookie_list = pickle.loads(base64.b64decode(cookie_list))
            cookies = self._cookiesFromCookieList(cookie_list)
            self.cookiejar.setCookiesFromUrl(
                cookies,
                QtCore.QUrl("https://mail.google.com/tasks/ig")
            )
        self.page().networkAccessManager().setCookieJar(self.cookiejar)
        
        self.load(QtCore.QUrl("https://mail.google.com/tasks/ig"))
        
    def closeEvent(self, event):
        cookies = self.cookiejar.cookiesForUrl(
                       QtCore.QUrl("https://mail.google.com/tasks/ig")
                  )
        cookie_list = self._cookieListFromCookies(cookies)
        
        settings = QtCore.QSettings("dasskript.com", "GoogleTasks")
        settings.setValue("cookies", QtCore.QString(
            base64.b64encode(pickle.dumps(cookie_list))));
        event.accept()

    def _cookieListFromCookies(self, cookies):
        cookie_list = []
        for cookie in cookies:
            cookie_list.append((cookie.name(), cookie.value()))
        return cookie_list
    
    def _cookiesFromCookieList(self, cookie_list):
        cookies = []
        for (name, value) in cookie_list:
            c = QtNetwork.QNetworkCookie(name, value)
            cookies.append(c)
        return cookies
        
if __name__ == "__main__":
    main(sys.argv)
