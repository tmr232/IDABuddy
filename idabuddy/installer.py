import idaapi

idaapi.require('idabuddy')
idaapi.require('sequences')
import sequences
from sark.qt import QtCore, form_to_widget, get_widget, QtWidgets, connect_method_to_signal

from idabuddy import AutoPopup


def get_idaview(title=None, form=None, widget=None):
    if form is not None:
        ida_widget = form_to_widget(form)
    elif widget is not None:
        ida_widget = widget
    else:
        ida_widget = get_widget(title)
    ida_holder = ida_widget.children()[0]
    idaview = ida_holder.children()[0]
    return idaview


# Get all ida views in <6.7
#
def iter_all_idaviews():
    '''Does return duplicates!'''
    for widget in QtWidgets.qApp.allWidgets():
        window_title = widget.windowTitle()
        if not window_title.startswith(u'IDA View-'):
            continue
        idaview = get_idaview(title=str(window_title))
        yield idaview


class Installer(object):
    INSTALL_INTERVAL = 1000

    def __init__(self):
        self._installed_views = set()
        if idaapi.IDA_SDK_VERSION >= 670:
            self._hooks = self._create_hooks(self._install_idabuddy)
            self._install_timer = None
        else:
            self._install_timer = QtCore.QTimer()
            connect_method_to_signal(self._install_timer, 'timeout()', self._on_install_timer)
            self._hooks = None

    def _iter_vacant_idaviews(self):
        return (idaview for idaview in iter_all_idaviews() if idaview not in self._installed_views)

    def _install_idabuddy(self, idaview):
        if idaview in self._installed_views:
            return
        self._installed_views.add(idaview)
        layout = QtWidgets.QHBoxLayout(idaview)
        popup = AutoPopup(idaview)
        layout.addWidget(popup)
        layout.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        layout.setContentsMargins(0, 0, 0, 0)
        popup.automate(sequences.say_address, *[sequences.say_random_saying]*10)
        popup.start()

        return popup

    def _create_hooks(self, install_idabuddy):
        class InstallerUiHooks(idaapi.UI_Hooks):
            def updating_actions(self, ctx):
                if ctx.form_type == idaapi.BWN_DISASM:
                    ida_widget = form_to_widget(ctx.form)
                    idaview = ida_widget.children()[0]
                    install_idabuddy(idaview)
                return super(InstallerUiHooks, self).updating_actions(ctx)

        return InstallerUiHooks()

    def _on_install_timer(self):
        for idaview in self._iter_vacant_idaviews():
            self._install_idabuddy(idaview)

    def start(self):
        if self._hooks:
            self._hooks.hook()
        else:
            self._install_timer.start(self.INSTALL_INTERVAL)

    def stop(self):
        if self._hooks:
            self._hooks.unhook()
        else:
            self._install_timer.stop()
