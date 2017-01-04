import os
import time

from PyQt4.QtCore import QString
from PyQt4.QtGui import QFileDialog
from copy import deepcopy

from golem.task.taskstate import TaskStatus

from apps.core.task.gnrtaskstate import TaskDesc
from apps.core.gui.controller.newtaskdialogcustomizer import NewTaskDialogCustomizer
from apps.rendering.task.renderingtaskstate import RenderingTaskDefinition

from gui.controller.timehelper import set_time_spin_boxes
from apps.core.gui.verificationparamshelper import read_advance_verification_params, \
    load_verification_params

import logging

logger = logging.getLogger("apps.rendering")


class RenderingNewTaskDialogCustomizer(NewTaskDialogCustomizer)


    def load_task_definition(self, task_definition):


        self._load_payment_params(definition)

    def _load_options(self, definition):
        pass

    def _load_task_type(self, definition):
        renderer_item = self.gui.ui.taskTypeComboBox.findText(definition.task_type)
        if renderer_item >= 0:
            self.gui.ui.taskTypeComboBox.setCurrentIndex(renderer_item)
        else:
            logger.error("Cannot load task, wrong renderer")
            return

    def __test_task_button_clicked(self):
        self.task_state = TaskDesc()
        self.task_state.status = TaskStatus.notStarted
        self.task_state.definition = self._query_task_definition()

        if not self.logic.run_test_task(self.task_state):
            logger.error("Task not tested properly")

    def test_task_computation_finished(self, success, est_mem):
        if success:
            self.task_state.definition.estimated_memory = est_mem
            self._change_finish_state(True)

    def _finish_button_clicked(self):
        self._add_current_task()
        self.load_task_definition(self.task_state.definition)

    def _cancel_button_clicked(self):
        self.__reset_to_defaults()
        NewTaskDialogCustomizer._cancel_button_clicked(self)


    def _query_task_definition(self):
        definition = RenderingTaskDefinition()
        self._read_basic_task_params(definition)
        self._read_renderer_params(definition)
        self._read_task_name(definition)
        self._read_advance_verification_params(definition)
        self._read_price_params(definition)

        return definition

    def _read_task_type(self):
        pass

    def _read_renderer_params(self, definition):
        definition.task_type = self.__get_current_task_type().name
        definition.render = self.__get_current_task_type().name
        definition.options = deepcopy(self.logic.options)
        self.get_task_specific_options(definition)
        self.logic.options = definition.options

        if self.add_task_resource_dialog_customizer:
            definition.resources = self.logic.options.add_to_resources(definition.resources)
            definition.resources.add(os.path.normpath(definition.main_scene_file))
            self.logic.customizer.gui.ui.resourceFilesLabel.setText(u"{}".format(len(definition.resources)))

    def _read_advance_verification_params(self, definition):
        read_advance_verification_params(self.gui, definition)

    def _optimize_total_check_box_changed(self):
        NewTaskDialogCustomizer._optimize_total_check_box_changed(self)
        self.task_settings_changed()

    def _open_options(self):
        renderer_name = self.gui.ui.taskTypeComboBox.itemText(self.gui.ui.taskTypeComboBox.currentIndex())
        renderer = self.logic.get_task_type(u"{}".format(renderer_name))
        dialog = renderer.dialog
        dialog_customizer = renderer.dialog_customizer
        renderer_dialog = dialog(self.gui.window)
        dialog_customizer(renderer_dialog, self.logic, self)
        renderer_dialog.show()

    def get_task_specific_options(self, definition):
        self.task_customizer.get_task_specific_options(definition)

    def set_options(self, options):
        self.logic.options = options
        self.task_settings_changed()

    def get_options(self):
        return self.logic.options




