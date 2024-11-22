import sys
import json
from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit, QTabBar, QLabel,
    QVBoxLayout, QHBoxLayout, QStackedLayout, QFrame, QFileDialog, QShortcut, QKeySequenceEdit
)
from PyQt5.QtCore import Qt, QUrl, QProcess
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineDownloadItem

# AddressBar: tool for toolbar.
class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()
        self.setFocus(True)


class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(1080, 720)
        self.setWindowTitle("Otango Browser")
        self.setWindowIcon(QIcon("menu.png"))
        self.tabs = []  # List to store web view objects and tab data
        self.tab_count = 0
        self.CreateApp()

    def CreateApp(self):
        # Main Layout
        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)


        # Left Panel
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setSpacing(0)
        self.leftLayout.setContentsMargins(0, 0, 0, 0)


        # Menu Layout
        self.rightLayout = QVBoxLayout()
        self.rightLayout.setSpacing(0)
        self.rightLayout.setContentsMargins(0, 0, 0, 0)


        # Menu tools
        self.sidemenu = QWidget()
        self.sidemenu.setVisible(False)
        self.sidemenu.setObjectName("sidemenu")
        self.sidemenuLayout = QVBoxLayout()
        self.sidemenuLayout.setSpacing(0)
        # self.menuLayout.setContentsMargins(0, 0, 0,0)
        self.sidemenu.setMinimumWidth(300)


        self.sidemenuTitle = QLabel("Options")
        # self.menuExitButton.setMaximumWidth(50)
        self.sidemenuTitle.setObjectName("titleMenuSettings")

        self.sidemenuExitButton = QPushButton("⎋")
        self.sidemenuExitButton.setMaximumWidth(50)
        self.sidemenuExitButton.setObjectName("btnMenuExit")
        self.sidemenuExitButton.clicked.connect(self.toggleMenu)
        

        # Title Menu Bar
        self.titletool = QWidget()
        self.titletool.setObjectName("titletool")
        self.titletool.layout = QHBoxLayout()
        self.titletool.layout.addWidget(self.sidemenuTitle)
        self.titletool.layout.addStretch(1)
        self.titletool.layout.addWidget(self.sidemenuExitButton)
        
        self.titletool.setLayout(self.titletool.layout)
        
        # Adding the titletool to the sidemenulayout
        self.sidemenuLayout.addWidget(self.titletool)


        self.settings = QPushButton("Settings")
        self.settings.setObjectName("menyItems")
        self.gotoDownloads = QPushButton("Downloads")
        self.gotoDownloads.setObjectName("menyItems")
        self.history = QPushButton("History")
        self.history.setObjectName("menyItems")
        self.switchTheme = QPushButton("Toggle Dark Mode/Light Mode")
        self.switchTheme.setObjectName("menyItems")
        self.developer = QPushButton("Developer Mode")
        self.developer.setObjectName("menyItems")
        self.bookmarks = QPushButton("Bookmarks")
        self.bookmarks.setObjectName("menyItems")
        self.print = QPushButton("Print")
        self.print.setObjectName("menyItems")


        self.switchTheme.clicked.connect(self.ToggleTheme)

        # Adding options to the sidemenu
        self.sidemenuLayout.addWidget(self.settings)
        self.sidemenuLayout.addWidget(self.switchTheme)
        self.sidemenuLayout.addWidget(self.gotoDownloads)
        self.sidemenuLayout.addWidget(self.history)
        self.sidemenuLayout.addWidget(self.developer)
        self.sidemenuLayout.addWidget(self.bookmarks)
        self.sidemenuLayout.addWidget(self.print)
        self.sidemenuLayout.addStretch(1)

        self.sidemenu.setLayout(self.sidemenuLayout)


        self.rightLayout.addWidget(self.sidemenu)





        # Tabbar container
        self.tabbarContainer = QWidget()
        self.tabbarContainerLayout = QHBoxLayout()
        self.tabbarContainer.setObjectName("tabbarContainer")

        # Tabbar
        self.tabbar = QTabBar(tabsClosable=True, movable=True)
        self.tabbar.setExpanding(False)
        self.tabbar.setElideMode(Qt.ElideLeft)
        # Tabber Events
        self.tabbar.tabCloseRequested.connect(self.closeTab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)
        self.tabbar.setObjectName("TabBar")

        # Creating a add tab button
        self.btnAddTab = QPushButton()
        self.btnAddTab.setIcon(QIcon("icons/ic_add_black_24px.svg"))
        # btnAddTab event handler
        self.btnAddTab.clicked.connect(self.AddTab)
        self.btnAddTab.setObjectName("btnAddTab")

        self.tabbarContainerLayout.addWidget(self.tabbar)
        self.tabbarContainerLayout.addStretch(1) # All the layouts are using flex. stretch 1 pushes the addtab button to the right end 
        self.tabbarContainerLayout.addWidget(self.btnAddTab)
        self.tabbarContainer.setLayout(self.tabbarContainerLayout)

        # Toolbar
        self.toolbar = QWidget()
        self.toolbar_layout = QHBoxLayout()
        self.toolbar.setLayout(self.toolbar_layout)

        # Tools
        self.btnBack = QPushButton()
        self.btnBack.setObjectName("btnControl")
        self.btnBack.setIcon(QIcon("icons/ic_keyboard_arrow_left_black_24px.svg"))
        self.btnBack.clicked.connect(self.goBack)
        self.btnForward = QPushButton()
        self.btnForward.setObjectName("btnControl")
        self.btnForward.setIcon(QIcon("icons/ic_keyboard_arrow_right_black_24px.svg"))
        self.btnForward.clicked.connect(self.goForward)
        self.btnRefresh = QPushButton()
        self.btnRefresh.setObjectName("btnControl")
        self.btnRefresh.setIcon(QIcon("icons/ic_refresh_black_24px.svg"))
        self.btnRefresh.clicked.connect(self.refresh)

        self.addressbar = AddressBar()
        self.addressbar.returnPressed.connect(self.BrowseTo)

        self.menu = QPushButton()
        self.menu.setIcon(QIcon("icons/menu.png"))
        self.menu.clicked.connect(self.toggleMenu)


        self.toolbar_layout.addWidget(self.btnBack)
        self.toolbar_layout.addWidget(self.btnForward)
        self.toolbar_layout.addWidget(self.btnRefresh)
        self.toolbar_layout.addWidget(self.addressbar)
        self.toolbar_layout.addWidget(self.menu)

        # Container
        self.container = QWidget()
        self.container_layout = QStackedLayout()
        self.container.setLayout(self.container_layout)

        self.leftLayout.addWidget(self.tabbarContainer)
        self.leftLayout.addWidget(self.toolbar)
        self.leftLayout.addWidget(self.container)

        self.layout.addLayout(self.leftLayout)
        self.layout.addLayout(self.rightLayout)
        self.setLayout(self.layout)

        # Called the addTab method so a new tab is created when the program opens
        self.AddTab()

        self.show()

    def AddTab(self):
        i = self.tab_count  # intitally the number of tabs: 0.

        # Create a new tab
        self.tabs.append(QWidget())

        # Set the tab's properties and layout
        self.tabs[i].setObjectName("tab" + str(i))
        self.tabs[i].layout = QHBoxLayout()
        self.tabs[i].layout.setContentsMargins(0, 0, 0, 0)

        # Creating the Web Page
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl().fromUserInput("http://www.google.com"))
        self.tabs[i].content.page().profile().downloadRequested.connect(self.handleDownload)

        # Event handlers for the web page
        self.tabs[i].content.titleChanged.connect(lambda: self.getTitle(i))
        self.tabs[i].content.iconChanged.connect(lambda: self.getIcon(i))
        self.tabs[i].content.urlChanged.connect(lambda: self.updateAddressbar(i))

        # Adding Content page each of its on created layout. 
        self.tabs[i].layout.addWidget(self.tabs[i].content)
        self.tabs[i].setLayout(self.tabs[i].layout)

        # Add the tab to the container layout (the QStackedLayout from above.) and set the current tab
        self.container_layout.addWidget(self.tabs[i])
        self.container_layout.setCurrentWidget(self.tabs[i])
        self.container_layout.setCurrentIndex(i)

        # Add the tab to the tabbar
        self.tabbar.addTab("New Tab")
        self.tabbar.setCurrentIndex(i)
        # Adding some tab unique data to reference it in the future.
        self.tabbar.setTabData(i, "tab" + str(i))

        # increase the tab count, Having keep track of how many tabs are available.
        self.tab_count += 1

    def closeTab(self, i):
        # Getting tab data.
        tab_data = self.tabbar.tabData(i)
        tab_content = self.findChild(QWidget, tab_data)
        if tab_content is not None:
            # Get the current index before removing the tab
            current_index = self.tabbar.currentIndex()
            self.container_layout.removeWidget(tab_content)
            tab_content.deleteLater()  # Delete the web view widget
            self.tabs.pop(i)  # Remove the object from the list

            self.tabbar.removeTab(i)
            self.tab_count -= 1

            # If the current tab was closed, switch to the previous tab
            if i == current_index:
                if current_index > 0:
                    self.tabbar.setCurrentIndex(current_index - 1)
                    self.SwitchTab(current_index - 1)
                elif self.tab_count > 0:
                    self.tabbar.setCurrentIndex(0)
                    self.SwitchTab(0)
                else:
                    # No more tabs left, add a new tab
                    self.AddTab()

    def SwitchTab(self, i):
        # Code to switch tabs
        
        if self.tabs[i]:
            self.container_layout.setCurrentWidget(self.tabs[i])
            url = self.tabs[i].content.url()
            self.addressbar.setText(url.toString())

    def getTitle(self, i):
        # Getting the title of the tabbar and displaying it
        tab_data = self.tabbar.tabData(i)
        tab_content = self.findChild(QWidget, tab_data)
        title = tab_content.content.title()
        self.tabbar.setTabText(i, title)

    def getIcon(self, i):
        # Getting the icon of the tabbar and displaying it
        tab_data = self.tabbar.tabData(i)
        tab_content = self.findChild(QWidget, tab_data)
        icon = tab_content.content.icon()
        self.tabbar.setTabIcon(i, icon)

    def updateAddressbar(self, i, url=None):
        # Updating the address bar with the current url
        if url is None:
            tab_data = self.tabbar.tabData(i)
            tab_content = self.findChild(QWidget, tab_data)
            url = tab_content.content.url()
        self.addressbar.setText(url.toString())

    def goBack(self):
        # Code to go back to the previous page
        i = self.tabbar.currentIndex()
        if i >= 0:
            tab_content = self.tabs[i].content
            if tab_content.history().canGoBack():
                tab_content.back()

    def goForward(self):
        # Code to go forward to the next page
        i = self.tabbar.currentIndex()
        if i >= 0:
            tab_content = self.tabs[i].content
            if tab_content.history().canGoForward():
                tab_content.forward()

    def refresh(self):
        # Code to refresh the current page
        i = self.tabbar.currentIndex()
        if i >= 0:
            tab_content = self.tabs[i].content
            tab_content.reload()

    def BrowseTo(self):
        # Browse to the entered URL in the address bar
        text = self.addressbar.text()
        url = ""
        if 'http' not in text:
            if '.' not in text:
                if 'localhost' in text:
                    url = 'http://' + text
                else:
                    url = 'http://google.com/search?q=' + text
            else:
                url = 'http://' + text
        else:
            url = text

        i = self.tabbar.currentIndex()
        self.object = self.findChild(QWidget, self.tabbar.tabData(i))
        self.object.content.load(QUrl.fromUserInput(url))

    def showURLTooltip(self, url):
        # Show the URL as a tooltip when the mouse hovers over the content
        self.addressbar.setToolTip(url)

    def hideURLTooltip(self):
        # Hide the tooltip when the mouse hovers out
        self.addressbar.setToolTip('')

    def mouseMoveEvent(self, event):
        # Get the current tab index and the URL of the web view
        current_index = self.tabbar.currentIndex()
        if current_index >= 0:
            tab_data = self.tabbar.tabData(current_index)
            tab_content = self.findChild(QWidget, tab_data)
            url = tab_content.content.url().toString()

            # Show the URL as a tooltip when the mouse hovers over the content
            self.showURLTooltip(url)

    def leaveEvent(self, event):
        # Hide the tooltip when the mouse leaves the application
        self.hideURLTooltip()

    def toggleMenu(self):
        # Toggle the side menu visibility
        if self.sidemenu.isVisible() ==  True:
            self.sidemenu.setVisible(False)
        else:
            self.sidemenu.setVisible(True)

    def ToggleTheme(self):
        # Toggle the application theme.
        try:
            with open("theme_config.json", "r") as file:
                config = json.load(file)

            # Toggle the theme
            current_theme = config.get("theme", "light")
            new_theme = "dark" if current_theme == "light" else "light"
            config["theme"] = new_theme

            # Save the updated configuration
            with open("theme_config.json", "w") as file:
                json.dump(config, file, indent=4)

            # Apply the new theme
            self.load_theme()
        except Exception as e:
            print(f"Error toggling theme: {e}")

        self.reopen_app()


    def handleDownload(self, download: QWebEngineDownloadItem):
        # Handle file downloads.
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download.path())
        if path:
            download.setPath(path)
            download.accept()
            print(f"Download started: {path}")
        else:
            print("Download canceled.")

    def reopen_app(self):
        # Closes the current app and reopens it.
        QProcess.startDetached(sys.executable, sys.argv)
        QApplication.quit()  # Close the current application instance


if __name__ == "__main__":
    # Load theme configuration
    try:
        with open("theme_config.json", "r") as config_file:
            config = json.load(config_file)
            theme = config.get("theme", "dark")
            css_file = config.get("dark_mode_css" if theme == "dark" else "light_mode_css", "")
    except FileNotFoundError:
        print("Error: theme_config.json not found. Defaulting to dark mode.")
        css_file = "materiallight.css"

    app = QApplication(sys.argv)
    if css_file:
        try:
            with open(css_file) as style:
                app.setStyleSheet(style.read())
        except FileNotFoundError:
            print(f"Error: CSS file '{css_file}' not found. Skipping theme application.")

    window = App()
    sys.exit(app.exec_())
