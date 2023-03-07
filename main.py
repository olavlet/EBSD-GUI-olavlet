# Copyright (c) 2022 EBSD-GUI developers
#
# This file is part of EBSD-GUI.

# EBSD-GUI is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

# EBSD-GUI is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.
import platform
import multiprocessing
import sys
import json
import os
import logging
logging.getLogger("pyopencl").setLevel(logging.WARNING)
logging.getLogger("hyperspy").setLevel(logging.WARNING)
from contextlib import redirect_stdout, redirect_stderr

try:
    import pyopencl.tools
except:
    print("PyOpenCL could not be imported")
import platform

from contextlib import redirect_stdout, redirect_stderr
import resources_rc
from PySide6.QtCore import QDir, Qt, QThreadPool, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QMessageBox
from PySide6.QtGui import QIcon
#try: 
#    import pyi_splash
#except:
#    pass
# Modules available from start in the console
import kikuchipy as kp
import hyperspy.api as hs

# Import something from kikutchipy to avoid load times during dialog initalizations
from kikuchipy import load
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

from ui.ui_main_window import Ui_MainWindow
from scripts.system_explorer import SystemExplorerWidget
from scripts.hough_indexing import HiSetupDialog
from scripts.pattern_processing import PatternProcessingDialog
from scripts.dictionary_indexing import DiSetupDialog
from scripts.refinement import RefineSetupDialog
from scripts.pre_indexing_maps import (
    save_adp_map,
    save_mean_intensity_map,
    save_rgb_vbse,
    save_iq_map,
)
from scripts.advanced_settings import AdvancedSettingsDialog
from scripts.console import Console
from utils import Redirect, SettingFile, FileBrowser, sendToWorker
from scripts.pattern_center import PatterCenterDialog
from scripts.region_of_interest import RegionOfInteresDialog
from scripts.signal_navigation_widget import SignalNavigationWidget

hs.set_log_level("CRITICAL")

KP_EXTENSIONS = (".h5", ".dat")
IMAGE_EXTENSIONS = ()


class AppWindow(QMainWindow):
    """
    The main app window that is present at all times
    """

    working_dir = QDir.currentPath()

    def __init__(self) -> None:
        super(AppWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setCentralWidget(
            None
        )  # NB! Only set to none if there are nothing inside the central widget
        self.showMaximized()

        self.systemExplorer = SystemExplorerWidget(self)
        self.fileBrowserOD = FileBrowser(FileBrowser.OpenDirectory)
        self.console = Console(parent=self, context=globals())
        self.signalNavigationWidget = SignalNavigationWidget(mainWindow=self)

        # Check platform and set windowStayOnTopHint
        if platform.system() == "Darwin":
            self.stayOnTopHint = True
        else:
            self.stayOnTopHint = False

        self.setupConnections()
        self.showImage(self.getSelectedPath())
        self.importSettings()
        QThreadPool.globalInstance().setMaxThreadCount(1)
        self.updateActiveJobs()
        #try:
        #    pyi_splash.close()
        #except Exception as e:
        #    pass

    def setupConnections(self):
        self.ui.dockWidgetSystemExplorer.setWidget(self.systemExplorer)
        # self.ui.dockWidgetSystemExplorer.adjustSize()
        self.systemExplorer.pathChanged.connect(
            lambda new_path: self.updateMenuButtons(new_path)
        )
        self.systemExplorer.pathChanged.connect(
            lambda new_path: self.showImage(new_path)
        )
        self.systemExplorer.requestSignalNavigation.connect(
            lambda signal_path: self.selectSignalNavigation(signal_path)
        )
        self.ui.dockWidgetSignalNavigation.setWidget(self.signalNavigationWidget)
        self.ui.actionOpen_Workfolder.triggered.connect(
            lambda: self.selectWorkingDirectory()
        )
        self.ui.actionSettings.triggered.connect(lambda: self.openSettings())
        self.ui.actionProcessingMenu.triggered.connect(lambda: self.selectProcessing())
        self.ui.actionROI.triggered.connect(lambda: self.selectROI())
        self.ui.actionSignalNavigation.triggered.connect(
            lambda: self.selectSignalNavigation(signal_path=self.getSelectedPath())
        )
        self.ui.actionDictionaryIndexing.triggered.connect(
            lambda: self.selectDictionaryIndexingSetup(
                pattern_path=self.getSelectedPath()
            )
        )
        self.ui.actionHoughIndexing.triggered.connect(
            lambda: self.selectHoughIndexingSetup(pattern_path=self.getSelectedPath())
        )
        self.ui.actionRefineOrientations.triggered.connect(
            lambda: self.selectRefineOrientations(file_path=self.getSelectedPath())
        )
        self.ui.actionPattern_Center.triggered.connect(
            lambda: self.selectPatternCenter()
        )
        self.ui.actionAverage_dot_product.triggered.connect(
            lambda: sendToWorker(
                self, save_adp_map, pattern_path=self.getSelectedPath()
            )
        )
        self.ui.actionImage_quality.triggered.connect(
            lambda: sendToWorker(self, save_iq_map, pattern_path=self.getSelectedPath())
        )
        self.ui.actionMean_intensity.triggered.connect(
            lambda: sendToWorker(
                self, save_mean_intensity_map, pattern_path=self.getSelectedPath()
            )
        )
        self.ui.actionVirtual_backscatter_electron.triggered.connect(
            lambda: sendToWorker(
                self, save_rgb_vbse, pattern_path=self.getSelectedPath()
            )
        )

    def selectWorkingDirectory(self):
        if self.fileBrowserOD.getFile():
            self.working_dir = self.fileBrowserOD.getPaths()[0]
            self.fileBrowserOD.setDefaultDir(self.working_dir)
            if os.path.exists("advanced_settings.txt"):
                setting_file = SettingFile("advanced_settings.txt")
                try:
                    file_types = json.loads(setting_file.read("File Types"))
                    system_view_filter = ["*" + x for x in file_types]
                    self.systemExplorer.setSystemViewer(
                        self.working_dir, system_view_filter
                    )
                except:
                    self.systemExplorer.setSystemViewer(self.working_dir)
            else:
                self.systemExplorer.setSystemViewer(self.working_dir)

            self.setWindowTitle(f"EBSD-GUI - {self.working_dir}")

    def getSelectedPath(self) -> str:
        return self.systemExplorer.selected_path

    def importSettings(self):
        if os.path.exists("advanced_settings.txt"):
            setting_file = SettingFile("advanced_settings.txt")
            try:
                file_types = json.loads(setting_file.read("File Types"))
                system_view_filter = ["*" + x for x in file_types]
            except:
                system_view_filter = [
                    "*.h5",
                    "*.dat",
                    "*.ang",
                    "*.jpg",
                    "*.png",
                    "*.txt",
                ]

            if os.path.exists(setting_file.read("Default Directory")):
                self.working_dir = setting_file.read("Default Directory")
                self.systemExplorer.setSystemViewer(
                    self.working_dir, system_view_filter
                )
        else:
            AdvancedSettingsDialog(parent=self).createSettingsFile()
            setting_file = SettingFile("advanced_settings.txt")
            file_types = json.loads(setting_file.read("File Types"))
            self.system_view_filter = ["*" + x for x in file_types]

    def openSettings(self):
        try:
            self.settingsDialog = AdvancedSettingsDialog(parent=self)
            self.settingsDialog.setWindowFlag(
                Qt.WindowStaysOnTopHint, self.stayOnTopHint
            )
            self.settingsDialog.exec()
        except Exception as e:
            self.console.errorwrite(
                f"Could not initialize settings dialog:\n{str(e)}\n"
            )

        # TODO: This whole thing should be changed to inside AdvancedSettingsDialog, and should only be executed when ok is pressed
        # updates file browser to changes:
        setting_file = SettingFile("advanced_settings.txt")
        file_types = json.loads(setting_file.read("File Types"))
        system_view_filters = ["*" + x for x in file_types]
        if setting_file.read("Default Directory") not in ["False", ""]:
            if self.working_dir == QDir.currentPath():
                self.working_dir = setting_file.read("Default Directory")
            self.systemExplorer.setSystemViewer(
                self.working_dir, filters=system_view_filters
            )

    def selectRefineOrientations(self, file_path: str):
        try:
            self.refineDialog = RefineSetupDialog(
                parent=self, file_path=file_path
            )
            self.refineDialog.setWindowFlag(
                Qt.WindowStaysOnTopHint, self.stayOnTopHint
            )
            self.refineDialog.exec()
        except Exception as e:
            self.console.errorwrite(
                f"Could not initialize refinement dialog:\n{str(e)}\n"
            )

    def selectProcessing(self):
        try:
            self.processingDialog = PatternProcessingDialog(
                parent=self, pattern_path=self.getSelectedPath()
            )
            self.processingDialog.setWindowFlag(
                Qt.WindowStaysOnTopHint, self.stayOnTopHint
            )
            self.processingDialog.exec()
        except Exception as e:
            self.console.errorwrite(
                f"Could not initialize processing dialog:\n{str(e)}\n"
            )

    def selectROI(self):
        try:
            plt.close("all")
        except Exception as e:
            print(e)
            pass
        try:
            self.ROIDialog = RegionOfInteresDialog(
                parent=self, pattern_path=self.getSelectedPath()
            )
            self.ROIDialog.setWindowFlag(Qt.WindowStaysOnTopHint, self.stayOnTopHint)
            self.ROIDialog.exec()
        except Exception as e:
            self.console.errorwrite(f"Could not initialize ROI dialog:\n{str(e)}\n")

    # def onSystemModelChanged(self, new_selected, old_selected):
    #     if new_selected.empty():
    #         self.file_selected = ""
    #     else:
    #         self.file_selected = self.systemModel.filePath(
    #             self.ui.systemViewer.currentIndex()
    #         )
    #     self.updateMenuButtons(self.file_selected)
    #     self.showImage(self.file_selected)

    # def doubleClickEvent(self):
    #     index = self.ui.systemViewer.currentIndex()
    #     self.file_selected = self.systemModel.filePath(index)

    #     if path.splitext(self.file_selected)[1] in [".txt"]:
    #         if platform.system().lower() == "darwin":
    #             subprocess.call(["open", "-a", "TextEdit", self.file_selected])
    #         if platform.system().lower() == "windows":
    #             startfile(self.file_selected)

    #     # TODO: more functionality, open dataset for signal navigation
    #     if splitext(self.file_selected)[1] in [".h5", ".dat"]:
    #         self.selectSignalNavigation()

    def selectSignalNavigation(self, signal_path: str):
        try:
            self.signalNavigationWidget.load_dataset(signal_path)

        except Exception as e:
            if self.getSelectedPath() == "":
                dlg = QMessageBox(self)
                dlg.setWindowTitle("No file")
                dlg.setText("You have to choose a pattern.")
                dlg.setStandardButtons(QMessageBox.Ok)
                dlg.setIcon(QMessageBox.Warning)
                dlg.exec()
            self.console.errorwrite(
                f"Could not initialize signal navigation:\n{str(e)}\n"
            )

    def selectDictionaryIndexingSetup(self, pattern_path: str):
        try:
            self.diSetup = DiSetupDialog(self, pattern_path)
            self.diSetup.setWindowFlag(Qt.WindowStaysOnTopHint, self.stayOnTopHint)
            self.diSetup.show()
        except Exception as e:
            self.console.errorwrite(
                f"Could not initialize dictionary indexing:\n{str(e)}\n"
            )

    def selectHoughIndexingSetup(self, pattern_path: str):
        try:
            self.hiSetup = HiSetupDialog(self, pattern_path)
            self.hiSetup.setWindowFlag(Qt.WindowStaysOnTopHint, self.stayOnTopHint)
            self.hiSetup.show()
        except Exception as e:
            self.console.errorwrite(f"Could not initialize hough indexing:\n{str(e)}\n")

    def selectPatternCenter(self):
        try:
            self.patternCenter = PatterCenterDialog(
                parent=self, file_selected=self.getSelectedPath()
            )
            self.patternCenter.setWindowFlag(
                Qt.WindowStaysOnTopHint, self.stayOnTopHint
            )
            self.patternCenter.show()
        except Exception as e:
            self.console.errorwrite(
                f"Could not initialize pattern center refinement:\n{str(e)}\n"
            )

    def showImage(self, image_path):
        try:
            if image_path == None or not os.path.splitext(image_path)[1] in [
                ".jpg",
                ".png",
                ".gif",
                ".bmp",
            ]:
                image = mpimg.imread("resources/ebsd_gui.png")
                self.ui.dockWidgetImageViewer.setWindowTitle(f"Image Viewer")
            else:
                image = mpimg.imread(image_path)
                self.ui.dockWidgetImageViewer.setWindowTitle(f"Image Viewer - {image_path}")
            self.ui.MplWidget.canvas.ax.clear()
            self.ui.MplWidget.canvas.ax.axis(False)
            self.ui.MplWidget.canvas.ax.imshow(image)
            self.ui.MplWidget.canvas.draw()
        except:
            pass

    def updateMenuButtons(self, file_path):
        """
        Updates the menu buttons based on the extension of file_path
        """

        def setAvailableMenuActions(enabled):
            self.ui.menuProcessing.setEnabled(enabled)
            self.ui.menuPatternInspection.setEnabled(enabled)
            self.ui.menuIndexing.setEnabled(enabled)
            self.ui.menuPre_indexing_maps.setEnabled(enabled)
            self.ui.actionSignalNavigation.setEnabled(enabled)
            self.ui.menuRefinement.setEnabled(enabled)

        if file_path == "":
            setAvailableMenuActions(False)
            return
        file_extension = os.path.splitext(file_path)[1]

        if file_extension in KP_EXTENSIONS:
            kp_enabled = True
        else:
            kp_enabled = False
        setAvailableMenuActions(kp_enabled)

        # Special case for plotting calibration patterns from Settings.txt
        if os.path.basename(file_path) == "Setting.txt":
            self.ui.menuPatternInspection.setEnabled(True)
            self.ui.actionSignalNavigation.setEnabled(True)
            self.ui.menuPre_indexing_maps.setEnabled(False)

    #TODO Move removeWorker and updateActiveJobs to a jobmanagerlist class
    @Slot(int)
    def removeWorker(self, worker_id: int):
        jobList = self.ui.jobList
        for i in range(jobList.count()):
            item = jobList.item(i)
            if jobList.itemWidget(item).id == worker_id:
                jobList.takeItem(jobList.row(item))
                break

    @Slot()
    def updateActiveJobs(self):
        self.ui.threadsLabel.setText(
            f"{QThreadPool.globalInstance().activeThreadCount()} out of {QThreadPool.globalInstance().maxThreadCount()} active jobs"
        )


if __name__ == "__main__":
    # Pyinstaller fix
    multiprocessing.freeze_support()

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(':/icons/app_icon.ico'))
    APP = AppWindow()
    # Redirect stdout to console.write and stderr to console.errorwrite
    with redirect_stdout(APP.console), redirect_stderr(
        Redirect(APP.console.errorwrite)
    ):
        APP.show()
        print(
            """EBSD-GUI  Copyright (C) 2023  EBSD-GUI developers 
This program comes with ABSOLUTELY NO WARRANTY; for details see COPYING.txt.
This is free software, and you are welcome to redistribute it under certain conditions; see COPYING.txt for details.""",
        )
        try:
            sys.exit(app.exec())
        except Exception as e:
            print(e)
            print("A clean exit was not performed")
