import sys

from PyQt5 import QtCore, QtGui, QtWebEngineWidgets, QtWidgets


class FlaskThread(QtCore.QThread):
	def __init__(self, flask_app):
		super(FlaskThread, self).__init__()
		self.app = flask_app

	def __del__(self):
		self.wait()

	def run(self):
		self.app.run(threaded=True)


class WebPage(QtWebEngineWidgets.QWebEnginePage):
	def __init__(self, root_url):
		super(WebPage, self).__init__()
		self.root_url = root_url
		self.profile().setHttpCacheType(self.profile().NoCache)

	def home(self):
		self.load(QtCore.QUrl(self.root_url))

	def acceptNavigationRequest(self, url, kind, is_main_frame):
		"""Open external links in browser and internal links in the webview"""
		ready_url = url.toEncoded().data().decode()
		is_clicked = kind == self.NavigationTypeLinkClicked
		if is_clicked and self.root_url not in ready_url:
			QtGui.QDesktopServices.openUrl(url)
			return False
		return super(WebPage, self).acceptNavigationRequest(url, kind, is_main_frame)


# noinspection PyArgumentList
def init_app(app, title='TGD Kiosk', icon='appicon.png'):
	# setup qt and flask app
	qt = QtWidgets.QApplication(sys.argv)
	flask = FlaskThread(app)
	flask.start()
	qt.aboutToQuit.connect(flask.terminate)

	# create window
	window = QtWidgets.QMainWindow()
	app.qt_window = window

	# borderless fullscreen
	# config setting for testing
	if app.config['BORDERLESS_FULLSCREEN']:
		window.setWindowState(QtCore.Qt.WindowMaximized)
		window.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		window.move(0, 0)
	else:
		window.resize(1920, 1080)

	# set info
	window.setWindowTitle(title)
	window.setWindowIcon(QtGui.QIcon(icon))

	# embed web view
	view = QtWebEngineWidgets.QWebEngineView(window)
	view.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)

	window.setCentralWidget(view)
	page = WebPage('http://localhost:{}'.format(app.config['FLASK_PORT']))

	page.home()
	view.setPage(page)

	window.show()
	return qt.exec_()
