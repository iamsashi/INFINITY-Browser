import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *


# Tab Class
class Tab(QWebEngineView):
    title_changed = pyqtSignal(str)

    def __init__(self, parent, url):
        super().__init__(parent)
        self.setUrl(QUrl(url))
        self.titleChanged.connect(self.update_tab_name)

    def update_tab_name(self, title):
        self.title_changed.emit(title)


# Main Window Class
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        self.tab_counter = 1
        self.create_tab("https://brave.com/en-in/search/")
        self.showMaximized()

        # Navigation Bar (Compact)
        navbar = QToolBar()
        navbar.setIconSize(QSize(20, 20))  # Compact icon size
        navbar.setFixedHeight(36)  # Slim toolbar height
        navbar.setStyleSheet("""
            QToolBar {
                spacing: 6px;
                padding: 3px;
            }
            QToolButton {
                font-size: 12px;
                padding: 3px 6px;
            }
        """)
        self.addToolBar(navbar)

        # Back Button
        back_btn = QAction('Back', self)
        back_btn.triggered.connect(self.navigate_back)
        navbar.addAction(back_btn)

        # Forward Button
        forward_btn = QAction('Forward', self)
        forward_btn.triggered.connect(self.navigate_forward)
        navbar.addAction(forward_btn)

        # Reload Button
        reload_btn = QAction('Reload', self)
        reload_btn.triggered.connect(self.navigate_reload)
        navbar.addAction(reload_btn)

        # Home Button
        home_btn = QAction('Home', self)
        home_btn.triggered.connect(self.navigate_home)
        navbar.addAction(home_btn)

        # New Tab Button
        new_tab_btn = QAction('New Tab', self)
        new_tab_btn.triggered.connect(self.create_blank_tab)
        navbar.addAction(new_tab_btn)

        # Close Tab Button
        close_tab_btn = QAction('Close Tab', self)
        close_tab_btn.triggered.connect(self.close_current_tab)
        navbar.addAction(close_tab_btn)

        # Google Search Button
        google_tab_btn = QAction('Google Search', self)
        google_tab_btn.triggered.connect(self.navigate_google)
        navbar.addAction(google_tab_btn)

        # Bing Search Button
        bing_tab_btn = QAction('Bing Search', self)
        bing_tab_btn.triggered.connect(self.navigate_bing)
        navbar.addAction(bing_tab_btn)

        # Yahoo Search Button
        yahoo_tab_btn = QAction('Yahoo Search', self)
        yahoo_tab_btn.triggered.connect(self.navigate_yahoo)
        navbar.addAction(yahoo_tab_btn)

        # URL Bar (Compact)
        self.url_bar = QLineEdit()
        self.url_bar.setFixedHeight(26)
        self.url_bar.setStyleSheet("font-size: 12px; padding: 3px;")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        # Tab change updates URL
        self.central_widget.currentChanged.connect(self.update_url)

        # Tab close event
        self.central_widget.tabCloseRequested.connect(self.close_tab)

        self.active_tab_index = 0
        self.central_widget.setStyleSheet("QTabWidget::pane { background: #f0f0f0; }")

        self.current_web_view = self.central_widget.currentWidget()
        self.update_url(0)

    # Tab Creation
    def create_tab(self, url):
        new_tab = Tab(self.central_widget, url)
        tab_text = f"Tab {self.tab_counter}"
        self.tab_counter += 1
        self.central_widget.addTab(new_tab, tab_text)
        self.central_widget.setCurrentWidget(new_tab)
        self.active_tab_index = self.central_widget.indexOf(new_tab)
        new_tab.title_changed.connect(self.update_tab_text)

    def create_blank_tab(self):
        self.create_tab("https://search.brave.com/")

    # Close Tabs
    def close_tab(self, index):
        if self.central_widget.count() > 1:
            self.central_widget.removeTab(index)

    def close_current_tab(self):
        if self.central_widget.count() > 1:
            index = self.central_widget.currentIndex()
            self.central_widget.removeTab(index)

    # Navigation
    def navigate_home(self):
        tab = self.central_widget.currentWidget()
        if tab:
            tab.setUrl(QUrl("https://search.brave.com/"))

    def navigate_back(self):
        tab = self.central_widget.currentWidget()
        if tab:
            tab.back()

    def navigate_forward(self):
        tab = self.central_widget.currentWidget()
        if tab:
            tab.forward()

    def navigate_reload(self):
        tab = self.central_widget.currentWidget()
        if tab:
            tab.reload()

    def navigate_to_url(self):
        url = self.url_bar.text()
        tab = self.central_widget.currentWidget()
        if tab:
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            tab.setUrl(QUrl(url))

    # Update URL Bar
    def update_url(self, index):
        tab = self.central_widget.currentWidget()
        if tab:
            self.current_web_view = tab
            self.url_bar.setText(tab.url().toString())

    # Tab Title
    def update_tab_text(self, title):
        index = self.central_widget.indexOf(self.sender())
        if title:
            self.central_widget.setTabText(index, title)
        else:
            self.central_widget.setTabText(index, self.sender().url().host())

    # Search Engine Shortcuts
    def navigate_google(self):
        self.create_tab("https://www.google.com/")

    def navigate_bing(self):
        self.create_tab("https://www.bing.com/")

    def navigate_yahoo(self):
        self.create_tab("https://www.yahoo.com/")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName('INFINITY Browser')
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
