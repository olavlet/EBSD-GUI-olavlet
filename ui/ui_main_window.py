# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QDockWidget, QGridLayout,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPlainTextEdit,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)

from mplwidget import MplWidget
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(1233, 824)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setLayoutDirection(Qt.LeftToRight)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
        self.actionOpen_Workfolder = QAction(MainWindow)
        self.actionOpen_Workfolder.setObjectName(u"actionOpen_Workfolder")
        icon = QIcon()
        icon.addFile(u":/linea icons/resources/linea basic icons/basic_folder.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen_Workfolder.setIcon(icon)
        self.actionProcessingMenu = QAction(MainWindow)
        self.actionProcessingMenu.setObjectName(u"actionProcessingMenu")
        self.actionProcessingMenu.setEnabled(True)
        self.actionSignalNavigation = QAction(MainWindow)
        self.actionSignalNavigation.setObjectName(u"actionSignalNavigation")
        self.actionSignalNavigation.setCheckable(False)
        self.actionSignalNavigation.setEnabled(True)
        self.actionDictionaryIndexing = QAction(MainWindow)
        self.actionDictionaryIndexing.setObjectName(u"actionDictionaryIndexing")
        self.actionPattern_Center = QAction(MainWindow)
        self.actionPattern_Center.setObjectName(u"actionPattern_Center")
        self.actionROI = QAction(MainWindow)
        self.actionROI.setObjectName(u"actionROI")
        self.actionHoughIndexing = QAction(MainWindow)
        self.actionHoughIndexing.setObjectName(u"actionHoughIndexing")
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        icon1 = QIcon()
        icon1.addFile(u":/linea icons/resources/linea basic icons/basic_gear.svg", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSettings.setIcon(icon1)
        self.actionImage_quality = QAction(MainWindow)
        self.actionImage_quality.setObjectName(u"actionImage_quality")
        self.actionMean_intensity = QAction(MainWindow)
        self.actionMean_intensity.setObjectName(u"actionMean_intensity")
        self.actionVirtual_backscatter_electron = QAction(MainWindow)
        self.actionVirtual_backscatter_electron.setObjectName(u"actionVirtual_backscatter_electron")
        self.actionAverage_dot_product = QAction(MainWindow)
        self.actionAverage_dot_product.setObjectName(u"actionAverage_dot_product")
        self.actionGenerate_images = QAction(MainWindow)
        self.actionGenerate_images.setObjectName(u"actionGenerate_images")
        self.actionGenerate_images.setEnabled(False)
        font = QFont()
        font.setKerning(False)
        font.setStyleStrategy(QFont.NoAntialias)
        self.actionGenerate_images.setFont(font)
        self.actionGenerate_images.setMenuRole(QAction.NoRole)
        self.actionToggleSystem_Explorer = QAction(MainWindow)
        self.actionToggleSystem_Explorer.setObjectName(u"actionToggleSystem_Explorer")
        self.actionToggleSystem_Explorer.setCheckable(True)
        self.actionToggleSystem_Explorer.setChecked(True)
        self.actionToggleTerminal = QAction(MainWindow)
        self.actionToggleTerminal.setObjectName(u"actionToggleTerminal")
        self.actionToggleTerminal.setCheckable(True)
        self.actionToggleTerminal.setChecked(True)
        self.actionToggleImage_Viewer = QAction(MainWindow)
        self.actionToggleImage_Viewer.setObjectName(u"actionToggleImage_Viewer")
        self.actionToggleImage_Viewer.setCheckable(True)
        self.actionToggleImage_Viewer.setChecked(True)
        self.actionToggleJob_Manager = QAction(MainWindow)
        self.actionToggleJob_Manager.setObjectName(u"actionToggleJob_Manager")
        self.actionToggleJob_Manager.setCheckable(True)
        self.actionToggleJob_Manager.setChecked(True)
        self.actionToggleSignal_Navigation = QAction(MainWindow)
        self.actionToggleSignal_Navigation.setObjectName(u"actionToggleSignal_Navigation")
        self.actionToggleSignal_Navigation.setCheckable(True)
        self.actionToggleSignal_Navigation.setChecked(True)
        self.actionRefineOrientations = QAction(MainWindow)
        self.actionRefineOrientations.setObjectName(u"actionRefineOrientations")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1233, 26))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuProcessing = QMenu(self.menubar)
        self.menuProcessing.setObjectName(u"menuProcessing")
        self.menuProcessing.setEnabled(False)
        self.menuPatternInspection = QMenu(self.menubar)
        self.menuPatternInspection.setObjectName(u"menuPatternInspection")
        self.menuPatternInspection.setEnabled(False)
        self.menuPre_indexing_maps = QMenu(self.menuPatternInspection)
        self.menuPre_indexing_maps.setObjectName(u"menuPre_indexing_maps")
        self.menuPre_indexing_maps.setEnabled(False)
        self.menuIndexing = QMenu(self.menubar)
        self.menuIndexing.setObjectName(u"menuIndexing")
        self.menuIndexing.setEnabled(False)
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        self.menuRefinement = QMenu(self.menubar)
        self.menuRefinement.setObjectName(u"menuRefinement")
        self.menuRefinement.setEnabled(False)
        MainWindow.setMenuBar(self.menubar)
        self.dockWidgetTerminal = QDockWidget(MainWindow)
        self.dockWidgetTerminal.setObjectName(u"dockWidgetTerminal")
        self.dockWidgetTerminalContents = QWidget()
        self.dockWidgetTerminalContents.setObjectName(u"dockWidgetTerminalContents")
        self.gridLayout_2 = QGridLayout(self.dockWidgetTerminalContents)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.consoleLog = QPlainTextEdit(self.dockWidgetTerminalContents)
        self.consoleLog.setObjectName(u"consoleLog")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.consoleLog.sizePolicy().hasHeightForWidth())
        self.consoleLog.setSizePolicy(sizePolicy1)

        self.verticalLayout_3.addWidget(self.consoleLog)

        self.inputLayout = QHBoxLayout()
        self.inputLayout.setObjectName(u"inputLayout")
        self.consolePrompt = QLabel(self.dockWidgetTerminalContents)
        self.consolePrompt.setObjectName(u"consolePrompt")

        self.inputLayout.addWidget(self.consolePrompt)


        self.verticalLayout_3.addLayout(self.inputLayout)

        self.verticalLayout_3.setStretch(0, 1)

        self.gridLayout_2.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.dockWidgetTerminal.setWidget(self.dockWidgetTerminalContents)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidgetTerminal)
        self.dockWidgetSystemExplorer = QDockWidget(MainWindow)
        self.dockWidgetSystemExplorer.setObjectName(u"dockWidgetSystemExplorer")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.dockWidgetSystemExplorer.sizePolicy().hasHeightForWidth())
        self.dockWidgetSystemExplorer.setSizePolicy(sizePolicy2)
        self.dockWidgetSystemExplorerContents = QWidget()
        self.dockWidgetSystemExplorerContents.setObjectName(u"dockWidgetSystemExplorerContents")
        self.gridLayout = QGridLayout(self.dockWidgetSystemExplorerContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalSpacer = QSpacerItem(320, 320, QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer, 0, 0, 1, 1)

        self.dockWidgetSystemExplorer.setWidget(self.dockWidgetSystemExplorerContents)
        MainWindow.addDockWidget(Qt.TopDockWidgetArea, self.dockWidgetSystemExplorer)
        self.dockWidgetImageViewer = QDockWidget(MainWindow)
        self.dockWidgetImageViewer.setObjectName(u"dockWidgetImageViewer")
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy3.setHorizontalStretch(10)
        sizePolicy3.setVerticalStretch(10)
        sizePolicy3.setHeightForWidth(self.dockWidgetImageViewer.sizePolicy().hasHeightForWidth())
        self.dockWidgetImageViewer.setSizePolicy(sizePolicy3)
        self.dockWidgetImageViewer.setMinimumSize(QSize(342, 368))
        self.dockWidgetContentsImageViewer = QWidget()
        self.dockWidgetContentsImageViewer.setObjectName(u"dockWidgetContentsImageViewer")
        sizePolicy.setHeightForWidth(self.dockWidgetContentsImageViewer.sizePolicy().hasHeightForWidth())
        self.dockWidgetContentsImageViewer.setSizePolicy(sizePolicy)
        self.gridLayout_4 = QGridLayout(self.dockWidgetContentsImageViewer)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.MplWidget = MplWidget(self.dockWidgetContentsImageViewer)
        self.MplWidget.setObjectName(u"MplWidget")
        sizePolicy4 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.MplWidget.sizePolicy().hasHeightForWidth())
        self.MplWidget.setSizePolicy(sizePolicy4)
        self.MplWidget.setMinimumSize(QSize(320, 320))
        self.MplWidget.setAutoFillBackground(False)
        self.MplWidget.setStyleSheet(u"background-color: transparent")

        self.gridLayout_4.addWidget(self.MplWidget, 0, 0, 1, 1)

        self.dockWidgetImageViewer.setWidget(self.dockWidgetContentsImageViewer)
        MainWindow.addDockWidget(Qt.TopDockWidgetArea, self.dockWidgetImageViewer)
        self.dockWidgetJobManager = QDockWidget(MainWindow)
        self.dockWidgetJobManager.setObjectName(u"dockWidgetJobManager")
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.gridLayout_3 = QGridLayout(self.dockWidgetContents)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.jobList = QListWidget(self.dockWidgetContents)
        self.jobList.setObjectName(u"jobList")
        self.jobList.setMinimumSize(QSize(400, 0))
        self.jobList.setSelectionMode(QAbstractItemView.NoSelection)

        self.gridLayout_3.addWidget(self.jobList, 1, 0, 1, 1)

        self.threadsLabel = QLabel(self.dockWidgetContents)
        self.threadsLabel.setObjectName(u"threadsLabel")
        self.threadsLabel.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.threadsLabel, 0, 0, 1, 1)

        self.dockWidgetJobManager.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(Qt.TopDockWidgetArea, self.dockWidgetJobManager)
        self.dockWidgetSignalNavigation = QDockWidget(MainWindow)
        self.dockWidgetSignalNavigation.setObjectName(u"dockWidgetSignalNavigation")
        sizePolicy5 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.dockWidgetSignalNavigation.sizePolicy().hasHeightForWidth())
        self.dockWidgetSignalNavigation.setSizePolicy(sizePolicy5)
        self.dockWidgetSignalNavigation.setMinimumSize(QSize(346, 144))
        self.dockWidgetContents_2 = QWidget()
        self.dockWidgetContents_2.setObjectName(u"dockWidgetContents_2")
        self.dockWidgetSignalNavigation.setWidget(self.dockWidgetContents_2)
        MainWindow.addDockWidget(Qt.BottomDockWidgetArea, self.dockWidgetSignalNavigation)
        self.dockWidgetTerminal.raise_()
        self.dockWidgetSystemExplorer.raise_()
        self.dockWidgetImageViewer.raise_()
        self.dockWidgetJobManager.raise_()
        self.dockWidgetSignalNavigation.raise_()

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProcessing.menuAction())
        self.menubar.addAction(self.menuPatternInspection.menuAction())
        self.menubar.addAction(self.menuIndexing.menuAction())
        self.menubar.addAction(self.menuRefinement.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionOpen_Workfolder)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSettings)
        self.menuProcessing.addAction(self.actionProcessingMenu)
        self.menuProcessing.addAction(self.actionROI)
        self.menuProcessing.addAction(self.actionPattern_Center)
        self.menuPatternInspection.addAction(self.actionSignalNavigation)
        self.menuPatternInspection.addAction(self.menuPre_indexing_maps.menuAction())
        self.menuPre_indexing_maps.addAction(self.actionAverage_dot_product)
        self.menuPre_indexing_maps.addAction(self.actionImage_quality)
        self.menuPre_indexing_maps.addAction(self.actionMean_intensity)
        self.menuPre_indexing_maps.addAction(self.actionVirtual_backscatter_electron)
        self.menuIndexing.addAction(self.actionDictionaryIndexing)
        self.menuIndexing.addAction(self.actionHoughIndexing)
        self.menuView.addAction(self.actionToggleSystem_Explorer)
        self.menuView.addAction(self.actionToggleTerminal)
        self.menuView.addAction(self.actionToggleImage_Viewer)
        self.menuView.addAction(self.actionToggleJob_Manager)
        self.menuView.addAction(self.actionToggleSignal_Navigation)
        self.menuRefinement.addAction(self.actionRefineOrientations)

        self.retranslateUi(MainWindow)
        self.dockWidgetTerminal.visibilityChanged.connect(self.actionToggleTerminal.setChecked)
        self.dockWidgetSystemExplorer.visibilityChanged.connect(self.actionToggleSystem_Explorer.setChecked)
        self.actionToggleSystem_Explorer.triggered["bool"].connect(self.dockWidgetSystemExplorer.setVisible)
        self.actionToggleTerminal.triggered["bool"].connect(self.dockWidgetTerminal.setVisible)
        self.actionToggleImage_Viewer.triggered["bool"].connect(self.dockWidgetImageViewer.setVisible)
        self.dockWidgetImageViewer.visibilityChanged.connect(self.actionToggleImage_Viewer.setChecked)
        self.dockWidgetJobManager.visibilityChanged.connect(self.actionToggleJob_Manager.setChecked)
        self.actionToggleJob_Manager.triggered["bool"].connect(self.dockWidgetJobManager.setVisible)
        self.dockWidgetSignalNavigation.visibilityChanged.connect(self.actionToggleSignal_Navigation.setChecked)
        self.actionToggleSignal_Navigation.triggered["bool"].connect(self.dockWidgetSignalNavigation.setVisible)
        self.actionSignalNavigation.triggered["bool"].connect(self.dockWidgetSignalNavigation.show)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"EBSD-GUI", None))
        self.actionOpen_Workfolder.setText(QCoreApplication.translate("MainWindow", u"Open Workfolder...", None))
#if QT_CONFIG(statustip)
        self.actionOpen_Workfolder.setStatusTip(QCoreApplication.translate("MainWindow", u"Select a folder containing patterns", u"LOL"))
#endif // QT_CONFIG(statustip)
        self.actionProcessingMenu.setText(QCoreApplication.translate("MainWindow", u"Signal-to-noise improvement", None))
#if QT_CONFIG(statustip)
        self.actionProcessingMenu.setStatusTip(QCoreApplication.translate("MainWindow", u"Perform processing on a pattern", None))
#endif // QT_CONFIG(statustip)
        self.actionSignalNavigation.setText(QCoreApplication.translate("MainWindow", u"Signal navigation", None))
        self.actionDictionaryIndexing.setText(QCoreApplication.translate("MainWindow", u"Dictionary indexing", None))
        self.actionPattern_Center.setText(QCoreApplication.translate("MainWindow", u"Refine pattern center", None))
        self.actionROI.setText(QCoreApplication.translate("MainWindow", u"Region of interest", None))
        self.actionHoughIndexing.setText(QCoreApplication.translate("MainWindow", u"Hough indexing", None))
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"Settings", None))
#if QT_CONFIG(statustip)
        self.actionSettings.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.actionImage_quality.setText(QCoreApplication.translate("MainWindow", u"Image quality map", None))
        self.actionMean_intensity.setText(QCoreApplication.translate("MainWindow", u"Mean intensity map", None))
        self.actionVirtual_backscatter_electron.setText(QCoreApplication.translate("MainWindow", u"Virtual backscatter electron", None))
        self.actionAverage_dot_product.setText(QCoreApplication.translate("MainWindow", u"Average dot product", None))
        self.actionGenerate_images.setText(QCoreApplication.translate("MainWindow", u"Generate images...", None))
        self.actionToggleSystem_Explorer.setText(QCoreApplication.translate("MainWindow", u"System Explorer", None))
        self.actionToggleTerminal.setText(QCoreApplication.translate("MainWindow", u"Terminal", None))
        self.actionToggleImage_Viewer.setText(QCoreApplication.translate("MainWindow", u"Image Viewer", None))
        self.actionToggleJob_Manager.setText(QCoreApplication.translate("MainWindow", u"Job Manager", None))
        self.actionToggleSignal_Navigation.setText(QCoreApplication.translate("MainWindow", u"Signal Navigation", None))
        self.actionRefineOrientations.setText(QCoreApplication.translate("MainWindow", u"Refine Crystal Map Orientations", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuProcessing.setTitle(QCoreApplication.translate("MainWindow", u"Processing", None))
        self.menuPatternInspection.setTitle(QCoreApplication.translate("MainWindow", u"Pattern inspection", None))
        self.menuPre_indexing_maps.setTitle(QCoreApplication.translate("MainWindow", u"Pre-indexing maps", None))
        self.menuIndexing.setTitle(QCoreApplication.translate("MainWindow", u"Indexing", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
        self.menuRefinement.setTitle(QCoreApplication.translate("MainWindow", u"Refinement", None))
        self.dockWidgetTerminal.setWindowTitle(QCoreApplication.translate("MainWindow", u"Terminal", None))
        self.consolePrompt.setText(QCoreApplication.translate("MainWindow", u">>>", None))
        self.dockWidgetSystemExplorer.setWindowTitle(QCoreApplication.translate("MainWindow", u"System Viewer", None))
        self.dockWidgetImageViewer.setWindowTitle(QCoreApplication.translate("MainWindow", u"Image Viewer", None))
        self.dockWidgetJobManager.setWindowTitle(QCoreApplication.translate("MainWindow", u"Job Manager", None))
        self.threadsLabel.setText(QCoreApplication.translate("MainWindow", u"0 out of 0 active jobs", None))
        self.dockWidgetSignalNavigation.setWindowTitle(QCoreApplication.translate("MainWindow", u"Signal Navigation", None))
    # retranslateUi

