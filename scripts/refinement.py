import json
import warnings
from datetime import date
from os import path
from typing import Optional, Sequence

import kikuchipy as kp
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from kikuchipy.indexing._merge_crystal_maps import merge_crystal_maps
from kikuchipy.signals.ebsd import EBSD, LazyEBSD
from kikuchipy.signals.ebsd_master_pattern import LazyEBSDMasterPattern
from kikuchipy.signals.util._crystal_map import _equal_phase
from orix import io, plot
from orix.crystal_map import CrystalMap, PhaseList
from orix.vector import Vector3d
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
)

from ui.ui_refine_setup import Ui_RefineSetupDialog
from utils import (
    FileBrowser,
    SettingFile,
    get_setting_file_bottom_top,
    sendToJobManager,
)

# Ignore warnings to avoid crash with integrated console
warnings.filterwarnings("ignore")


class RefineSetupDialog(QDialog):
    def __init__(self, parent: QMainWindow, file_path: Optional[str] = ""):
        super().__init__(parent)

        parameter_file, self.xmap_dir = get_setting_file_bottom_top(
            file_path, "indexing_parameters.txt", return_dir_path=True
        )
        self.setting_file, self.working_dir = get_setting_file_bottom_top(
            file_path, "project_settings.txt", return_dir_path=True
        )
        self.program_settings = SettingFile("advanced_settings.txt")
        self.pattern_path = ""
        self.xmap_path = ""
        self.ui = Ui_RefineSetupDialog()
        self.ui.setupUi(self)
        self.setWindowTitle(f"{self.windowTitle()} - {file_path}")
        self.fileBrowserOF = FileBrowser(
            mode=FileBrowser.OpenFile, filter_name="Hierarchical Data Format (*.h5);"
        )
        self.fileBrowserOF.setDefaultDir(self.working_dir)
        # Load file
        try:
            try:
                s_prew = kp.load(file_path, lazy=True)
                if isinstance(s_prew, (EBSD, LazyEBSD)):
                    self.pattern_path = file_path
            except:
                xmap = io.load(file_path)
                if isinstance(xmap, (CrystalMap)):
                    self.xmap_path = file_path
                    if parameter_file is None:
                        print(
                            "No indexing parameters associated with selected crystal map"
                        )
                        raise Exception
                    self.pattern_path = path.join(
                        self.working_dir, parameter_file.read("Pattern name")
                    )
                    self.load_crystal_map(self.xmap_path)
                    try:
                        s_prew = kp.load(self.pattern_path)
                    except Exception as e:
                        print("Could not load patterns associated with crystal map")
                        raise e
        except Exception as e:
            raise e
        self.ui.labelNavigationShape.setText(
            f"Navigation shape: {str(s_prew.axes_manager.navigation_shape[::-1])}"
        )
        self.binnings = self.getBinningShapes(s_prew)
        self.mp_paths = {}
        self.phases = PhaseList()
        self.colors = [
            "blue",
            "orange",
            "lime",
            "yellow",
        ]

        self.setupConnections()
        self.load_parameters()
        self.setAvailableButtons()

        # Matplotlib configuration
        mpl.use("agg")
        plt.rcParams.update({"font.size": 20})
        self.savefig_kwds = dict(pad_inches=0, bbox_inches="tight", dpi=150)

    def setupConnections(self):
        self.ui.buttonBox.accepted.connect(lambda: self.run_refinement())
        self.ui.buttonBox.rejected.connect(lambda: self.reject())
        self.ui.pushButtonLoadMP.clicked.connect(lambda: self.load_master_pattern())
        self.ui.pushButtonRemoveMP.clicked.connect(lambda: self.remove_master_pattern())
        self.ui.pushButtonLoadXmap.clicked.connect(lambda: self.load_crystal_map())
        self.ui.comboBoxBinning.currentTextChanged.connect(
            lambda: self.ui.labelSignalShape.setText(
                f"Signal Shape: {self.binnings[self.ui.comboBoxBinning.currentText()]}"
            )
        )
        self.ui.comboBoxBinning.addItems(self.binnings.keys())
        self.ui.labelSignalPath.setText(self.pattern_path)

    def getOptions(self) -> dict:
        return {
            "mask": self.ui.checkBoxMask.isChecked(),
            "binning": self.ui.comboBoxBinning.currentText(),
            "lazy": self.ui.checkBoxLazy.isChecked(),
            "ncc": [
                self.ui.checkBoxNCC.isChecked(),
                self.save_ncc_map,
            ],
            "phase": [self.ui.checkBoxPhase.isChecked(), self.save_phase_map],
            "orientation": [
                self.ui.checkBoxOrientation.isChecked(),
                self.save_ipf_map,
            ],
            "ckey_direction": self.ui.lineEditColorKey.text(),
            "convention": self.ui.comboBoxConvention.currentText().lower(),
            "pc": (
                self.ui.patternCenterX.value(),
                self.ui.patternCenterY.value(),
                self.ui.patternCenterZ.value(),
            ),
            "method": self.ui.comboBoxMethod.currentText(),
            "ref_kwargs": self.ui.lineEditRefKwargs.text(),
        }

    def load_parameters(self):
        # read current setting from project_settings.txt, advanced_settings.txt
        try:
            convention = self.setting_file.read("Convention")
        except:
            convention = self.program_settings.read("Convention")
        self.ui.comboBoxConvention.setCurrentText(convention)
        pc_params = (self.ui.patternCenterX, self.ui.patternCenterY, self.ui.patternCenterZ)
        try:
            pc = eval(self.setting_file.read("PC"))
            for i, param in enumerate(pc_params): 
                param.setValue(float(pc[i]))
        except:
            for param in pc_params: 
                param.setValue(0.5)
        try:
            self.colors = json.loads(self.program_settings.read("Colors"))
        except:
            pass
        try:
            if self.program_settings.read("Lazy Loading") == "False":
                self.ui.checkBoxLazy.setChecked(False)
        except:
            pass

        binningBox = self.ui.comboBoxBinning
        try:
            binning = json.loads(self.setting_file.read("Binning"))
            binningBox.setCurrentIndex(binningBox.findText(str(binning)))
        except:
            binningBox.setCurrentIndex(binningBox.findText("None"))

        i = 1
        while True:
            try:
                mp_path = self.setting_file.read(f"Master pattern {i}")
                self.load_master_pattern(mp_path)
                i += 1
            except:
                break

    # TODO Make settings_file better to handle writing to file more convenient
    # def save_parameters(self):
    #     self.setting_file.delete_all_entries()  # Clean up initial dictionary
    #     options = self.getOptions()
    #     for idx, mp_path in enumerate(self.mp_paths):
    #         self.setting_file.write(
    #             f"Master pattern {idx}", mp_path
    #         )
    #     self.setting_file.write("Convention", options["convention"].upper())
    #     pc = options["pc"]
    #     self.setting_file.write("X star", pc[0])
    #     self.setting_file.write("Y star", pc[1])
    #     self.setting_file.write("Z star", pc[2])
    #     self.setting_file.write("Binning", options["binning"])
    #     self.setting_file.save()

    def load_crystal_map(self, xmap_path: Optional[str] = None):
        if xmap_path is not None:
            self.xmap_path = xmap_path
            self.xmap_name = path.basename(self.xmap_path)
            self.xmap_dir = path.dirname(self.xmap_path)
            xmap = io.load(xmap_path)
            self.updateCrystalMapTable(xmap)
        elif self.fileBrowserOF.getFile():
            self.xmap_path = self.fileBrowserOF.getPaths()[0]
            self.xmap_name = path.basename(self.xmap_path)
            self.xmap_dir = path.dirname(self.xmap_path)
            xmap = io.load(self.xmap_path)
            self.updateCrystalMapTable(xmap)

    def load_master_pattern(self, mp_path: Optional[str] = None):
        if mp_path is not None:
            try:
                mp: LazyEBSDMasterPattern = kp.load(mp_path, lazy=True)
                if mp.phase.name == "":
                    mp.phase.name = path.dirname(mp_path).split("/").pop()
                self.phases.add(mp.phase)
                mp.phase.color = self.colors[len(self.phases.ids) - 1]
                self.mp_paths[mp.phase.name] = mp_path
            except Exception as e:
                print("Phase could not be loaded from master pattern", e)
            self.updatePhaseTable()
        elif self.fileBrowserOF.getFile():
            mp_paths = self.fileBrowserOF.getPaths()
            for mp_path in mp_paths:
                try:
                    mp: LazyEBSDMasterPattern = kp.load(mp_path, lazy=True)
                    if mp.phase.name == "":
                        mp.phase.name = path.dirname(mp_path).split("/").pop()
                    self.phases.add(mp.phase)
                    mp.phase.color = self.colors[len(self.phases.ids) - 1]
                    self.mp_paths[mp.phase.name] = mp_path
                except Exception as e:
                    print("Phase could not be loaded from master pattern", e)
            self.updatePhaseTable()

    def updatePhaseTable(self):
        """
        NAME_COL = 0
        NUMBER_COL = 1
        ISS_COL = 2
        CRYSTAL_COL = 3
        COLOR_COL = 4
        """
        phasesTable = self.ui.tableWidgetPhase
        phasesTable.setRowCount(len(self.phases.ids))
        row = 0
        for _, phase in self.phases:
            sg = phase.space_group
            entries = [
                phase.name,
                sg.number,
                sg.short_name,
                sg.crystal_system,
                phase.color,
            ]
            for col, entry in enumerate(entries):
                item = QTableWidgetItem(str(entry))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                phasesTable.setItem(row, col, item)
            row += 1
        self.setAvailableButtons()

    def updateCrystalMapTable(self, xmap: CrystalMap):
        self.ui.labelXmapPath.setText(self.xmap_path)
        xmapTable = self.ui.tableWidgetXmap
        xmapTable.setRowCount(len(xmap.phases.ids))
        xmapTable.setVerticalHeaderLabels(
            [f"P{i}" for i in range(len(xmap.phases.ids))]
        )
        row = 0
        for _, phase in xmap.phases:
            phase_amount = xmap[f"{phase.name}"].size / xmap.size
            entries = [phase.name, f"{xmap[f'{phase.name}'].size} ({phase_amount:.1%})"]
            for col, entry in enumerate(entries):
                item = QTableWidgetItem(str(entry))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                xmapTable.setItem(row, col, item)
            row += 1
        if path.exists(path.join(self.xmap_dir, "index_data.npy")):
            self.ui.labelIndexDataStatus.setStyleSheet("QLabel { color : green; }")
            self.ui.labelIndexDataStatus.setText("Index data available")
        else:
            self.ui.labelIndexDataStatus.setStyleSheet("QLabel { color : red; }")
            self.ui.labelIndexDataStatus.setText("No available index data")
        self.setAvailableButtons()

    def remove_master_pattern(self):
        phaseTable = self.ui.tableWidgetPhase
        indexes = phaseTable.selectionModel().selectedRows()
        countRow = len(indexes)
        for i in range(countRow, 0, -1):
            phase_key = phaseTable.item(indexes[i - 1].row(), 0).text()
            self.phases.__delitem__(phase_key)
            if phase_key in self.mp_paths.keys():
                self.mp_paths.pop(phase_key)
            phaseTable.removeRow(indexes[i - 1].row())
        self.setAvailableButtons()

    def setAvailableButtons(self):
        ok_flag = False
        phase_map_flag = False
        add_phase_flag = True
        xmap_flag = False
        n_phases = self.ui.tableWidgetPhase.rowCount()
        n_xmap = self.ui.tableWidgetXmap.rowCount()
        if n_phases:
            ok_flag = True
            if n_phases > 1:
                phase_map_flag = True
        if n_xmap:
            xmap_flag = True
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(ok_flag and xmap_flag)
        self.ui.checkBoxPhase.setEnabled(phase_map_flag)
        self.ui.checkBoxPhase.setChecked(phase_map_flag)
        self.ui.pushButtonLoadMP.setEnabled(add_phase_flag)

    def getBinningShapes(self, signal: LazyEBSD) -> dict:
        sig_shape = signal.axes_manager.signal_shape[::-1]
        binnings: dict = {"None": sig_shape}
        for num in range(2, 17):
            if sig_shape[0] % num == 0 and sig_shape[1] % num == 0:
                binnings[f"{num}"] = (int(sig_shape[0] / num), int(sig_shape[1] / num))
        return binnings

    def refine_orientations(
        self,
        s: EBSD,
        xmap: CrystalMap,
        data: np.ndarray,
        master_patterns: dict,
        options: dict,
    ):
        binning = eval(options["binning"])
        pc = options["pc"]
        convention = options["convention"]
        mask = options["mask"]
        method = options["method"]
        if len(options["ref_kwargs"]):
            ref_kwargs = eval(options["ref_kwargs"])
        else:
            ref_kwargs = {}
        energy: int = s.metadata.Acquisition_instrument.SEM.beam_energy
        nav_shape = s.axes_manager.navigation_shape[::-1]
        step_sizes = (s.axes_manager["x"].scale, s.axes_manager["y"].scale)
        scan_unit = s.axes_manager[
            "x"
        ].units  # Assumes scan unit is the same for y and x
        if binning is None:
            binning = 1
        else:
            s = s.rebin(
                new_shape=s.axes_manager.navigation_shape + self.binnings[str(binning)]
            )
        sig_shape = s.axes_manager.signal_shape[::-1]  # (Rows, columns)
        det = kp.detectors.EBSDDetector(
            shape=sig_shape,
            binning=binning,
            sample_tilt=s.detector.sample_tilt,
            tilt=s.detector.tilt,
            pc=pc,
            convention=convention,
        )
        if mask:
            signal_mask = ~kp.filters.Window("circular", det.shape).astype(bool)
        else:
            signal_mask = None
        print("------- Detector stats -------")
        print(f"Navigation shape: {nav_shape}")
        print(f"Steps: {step_sizes} {scan_unit}")
        print(f"Signal shape: {sig_shape}")
        print(f"Circular mask: {mask}")

        ref_xmaps = {}
        for mp_key, mp in master_patterns.items():
            phase_id = xmap.phases.id_from_name(mp_key)
            mp.phase.color = self.colors[phase_id]
            print(f"\nRefining with Master Pattern: {mp.phase.name}")
            if data is not None:
                xmap_phase: CrystalMap = kp.indexing.xmap_from_hough_indexing_data(
                    data=data,
                    phase_list=self.phases,
                    data_index=phase_id,
                    navigation_shape=nav_shape,
                    step_sizes=step_sizes,
                    scan_unit=scan_unit,
                )
                # Not needed as of Kikuchipy 0.8.4
                # --------------------------------
                # if not xmap_phase.all_indexed:
                #     nav_mask_phase = ~(
                #         xmap_phase.phase_id == xmap.phases.id_from_name(mp_key)
                #     )
                #     nav_mask_phase = nav_mask_phase.reshape(xmap.shape)
                # else:
                #     nav_mask_phase = None
                ref_xmaps[mp_key] = s.refine_orientation(
                    xmap=xmap_phase,
                    detector=det,
                    master_pattern=mp,
                    energy=energy,
                    navigation_mask=None,
                    signal_mask=signal_mask,
                    trust_region=[1, 1, 1],
                    method=method,
                    method_kwargs=ref_kwargs,
                    compute=True,
                )
            else:
                nav_mask_phase = ~np.logical_or(
                    xmap.phase_id == xmap.phases.id_from_name(mp_key),
                    xmap.phase_id == -1,
                )
                nav_mask_phase = nav_mask_phase.reshape(xmap.shape)
                ref_xmaps[mp_key] = s.refine_orientation(
                    xmap=xmap,
                    detector=det,
                    master_pattern=mp,
                    energy=energy,
                    navigation_mask=nav_mask_phase,
                    signal_mask=signal_mask,
                    trust_region=[1, 1, 1],
                    method=method,
                    method_kwargs=ref_kwargs,
                    compute=True,
                )
        ref_xmaps_list = list(ref_xmaps.values())
        if len(ref_xmaps_list) == 1:
            ref_xmap = ref_xmaps_list[0]
        else:
            print("Merging crystal maps")
            ref_xmap = merge_crystal_maps(ref_xmaps_list, scores_prop="scores")
        io.save(
            path.join(self.xmap_dir, f"refined_{path.splitext(self.xmap_name)[0]}.h5"),
            ref_xmap,
        )
        io.save(
            path.join(self.xmap_dir, f"refined_{path.splitext(self.xmap_name)[0]}.ang"),
            ref_xmap,
        )
        print("Result was saved as refined_xmap_hi.ang and refined_xmap_hi.h5")

        for key in ["phase", "orientation", "ncc"]:
            optionEnabled, optionExecute = options.get(key)
            if optionEnabled:
                try:
                    if key == "orientation":
                        optionExecute(ref_xmap, eval(f"[{options['ckey_direction']}]"))
                    else:
                        optionExecute(ref_xmap)
                except Exception as e:
                    print(f"Could not save {key}_map:\n{e}")
        print(f"Finished refining orientations for {self.xmap_name}")

    def run_refinement(self, override_phases: bool = False):
        options = self.getOptions()
        try:
            s: EBSD = kp.load(self.pattern_path, lazy=options["lazy"])
        except Exception as e:
            raise e
        try:
            xmap: CrystalMap = io.load(self.xmap_path)
        except Exception as e:
            raise e
        data_path = path.join(self.xmap_dir, "index_data.npy")
        if path.exists(data_path):
            index_data = np.load(data_path)
        else:
            index_data = None
        energy: int = s.metadata.Acquisition_instrument.SEM.beam_energy
        master_patterns = {}
        for mp_key, mp_path in self.mp_paths.items():
            mp = kp.load(
                mp_path,
                energy=energy,
                projection="lambert",
                hemisphere="upper",
                lazy=options["lazy"],
            )
            if (
                mp.phase.name == ""
            ):  # If the master pattern is missing the name of the phase
                mp.phase.name = path.dirname(mp_path).split("/").pop()
            master_patterns[mp_key] = mp
            if not override_phases:
                if mp_key in xmap.phases_in_data.names:
                    xmap_phase = xmap.phases_in_data[mp_key]
                    equal_phases, are_different = _equal_phase(mp.phase, xmap_phase)
                    if not equal_phases:
                        if self.promptOverridePhase(
                            f"Master pattern phase '{mp.phase.name}' and phase of points to refine "
                            f"in crystal map '{xmap_phase.name}' must be the same, but have "
                            f"different {are_different}."
                        ):
                            xmap_phase.name = mp.phase.name
                            xmap_phase.space_group = mp.phase.space_group
                            xmap_phase.color = mp.phase.color
                            xmap_phase.structure = mp.phase.structure
                            continue
                        else:
                            return
        sendToJobManager(
            job_title=f"Refine orientations {self.xmap_name}",
            output_path=self.xmap_dir,
            listview=self.parentWidget().ui.jobList,
            func=self.refine_orientations,
            allow_cleanup=False,
            allow_logging=False,
            s=s,
            xmap=xmap,
            data=index_data,
            master_patterns=master_patterns,
            options=options,
        )

    def promptOverridePhase(self, message) -> bool:
        reply = QMessageBox(self).information(
            self,
            "Warning Phase conflict",
            f"{message}\nOverride phase from crystal map with phase from master pattern'?",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
        )
        if reply == QMessageBox.Yes:
            return True
        else:
            return False

    def save_quality_metrics(self, xmap):
        """
        Save plots of quality metrics
        """
        print("Saving quality metric for combined map ...")
        aspect_ratio = xmap.shape[1] / xmap.shape[0]
        figsize = (8 * aspect_ratio, 4.5 * aspect_ratio)
        fig, ax = plt.subplots(nrows=2, ncols=2, figsize=figsize)
        for a, to_plot in zip(ax.ravel(), ["pq", "cm", "fit", "nmatch"]):
            arr = xmap.get_map_data(to_plot)
            im = a.imshow(arr)
            fig.colorbar(im, ax=a, label=to_plot)
            a.axis("off")
            plt.imsave(
                path.join(self.xmap_dir, f"quality_metrics_{to_plot}.png"),
                arr,
            )
        fig.subplots_adjust(wspace=0, hspace=0.05)
        fig.savefig(
            path.join(self.xmap_dir, "quality_metrics_all.png"), **self.savefig_kwds
        )

    def save_phase_map(self, xmap):
        """
        Plot phase map
        """
        print("Saving phase map ...")
        fig = xmap.plot(return_figure=True, remove_padding=True)
        fig.savefig(
            path.join(self.xmap_dir, "refined_phase_map.png"), **self.savefig_kwds
        )

    def save_ipf_map(
        self,
        xmap: CrystalMap,
        ckey_direction: Optional[Sequence] = [0, 0, 1],
        ckey_overlay: Optional[bool] = False,
    ):
        """
        Plot inverse pole figure map with orientation colour key

        Parameters
        ----------
        xmap : CrystalMap
            The crystal map which the orientations originates from
        ckey_direction: sequence
            3D vector used to determine the orientation color key
        ckey_overlay : bool
            Whether the colour orientation key is shown on top of the map or saved to seperate png, default is seperate
        """
        print("Saving inverse pole figure map ...")
        v_ipf = Vector3d(ckey_direction)
        sym = xmap.phases[0].point_group
        ckey = plot.IPFColorKeyTSL(sym, v_ipf)
        print(ckey)
        fig_ckey = ckey.plot(return_figure=True)
        rgb_direction = ckey.orientation2color(xmap.rotations)
        fig = xmap.plot(rgb_direction, remove_padding=True, return_figure=True)
        if ckey_overlay:
            ax_ckey = fig.add_axes(
                [0.77, 0.07, 0.2, 0.2], projection="ipf", symmetry=sym
            )
            ax_ckey.plot_ipf_color_key(show_title=False)
            ax_ckey.patch.set_facecolor("None")
        else:
            fig_ckey.savefig(
                path.join(self.xmap_dir, "orientation_colour_key.png"),
                **self.savefig_kwds,
            )
        fig.savefig(path.join(self.xmap_dir, "refined_IPF.png"), **self.savefig_kwds)

    def save_ncc_map(self, xmap: CrystalMap):
        if len(xmap.phases.ids) == 1:
            fig = xmap.plot(
                "scores",
                return_figure=True,
                colorbar=True,
                colorbar_label="NCC",
                cmap="gray",
                remove_padding=True,
            )
        else:
            fig = xmap.plot(
                value=xmap.merged_scores[:, 0],
                colorbar=True,
                colorbar_label="NCC",
                return_figure=True,
                cmap="gray",
                remove_padding=True,
            )
        fig.savefig(
            path.join(self.xmap_dir, "refined_NCC.png"),
            **self.savefig_kwds,
        )


# TODO Add more Hough related properties, better way to sort?
def log_hi_parameters(
    dir_out: str,
    signal: EBSD | LazyEBSD = None,
    xmap: CrystalMap = None,
    mp_paths: dict = None,
    pattern_center: np.ndarray = None,
    convention: str = "BRUKER",
    binning: int = 1,
):
    """
    Assumes convention is BRUKER for pattern center if none is given
    """

    log = SettingFile(path.join(dir_out, "hi_parameters.txt"))
    K = ["strs"]
    ### Time and date
    log.write("Date", f"{date.today()}\n")

    ### SEM parameters
    log.write("Microscope", signal.metadata.Acquisition_instrument.SEM.microscope)
    log.write(
        "Acceleration voltage",
        f"{signal.metadata.Acquisition_instrument.SEM.beam_energy} kV",
    )
    log.write("Sample tilt", f"{signal.detector.sample_tilt} degrees")
    log.write("Camera tilt", f"{signal.detector.tilt} degrees")
    log.write(
        "Working distance",
        signal.metadata.Acquisition_instrument.SEM.working_distance,
    )
    log.write("Magnification", signal.metadata.Acquisition_instrument.SEM.magnification)
    log.write(
        "Navigation shape (rows, columns)",
        signal.axes_manager.navigation_shape[::-1],
    )
    if binning == 1:
        log.write("Binning", None)
    else:
        log.write("Binning", binning)
    log.write("Signal shape (rows, columns)", signal.axes_manager.signal_shape[::-1])
    log.write("Step size", f"{signal.axes_manager[0].scale} um\n")

    ### HI parameteres

    log.write("kikuchipy version", kp.__version__)

    if mp_paths is not None:
        for i, mp_path in enumerate(mp_paths.values(), 1):
            log.write(f"Master pattern path {i}", mp_path)
    log.write("PC convention", f"{convention.upper()}")
    log.write("Pattern center (x*, y*, z*)", f"{pattern_center}")

    if len(xmap.phases.names) > 1:
        for i, ph in enumerate(xmap.phases.names, 1):
            phase_amount = xmap[f"{ph}"].size / xmap.size
            log.write(
                f"Phase {i}: {ph} [% ( # points)] ",
                f"{phase_amount:.1%}, ({xmap[f'{ph}'].size})",
            )

        not_indexed_percent = xmap["not_indexed"].size / xmap.size
        log.write(
            "Not indexed", f"{xmap['not_indexed'].size} ({not_indexed_percent:.1%})"
        )

    log.save()
