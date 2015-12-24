import idaapi

idaapi.require('installer')
from installer import Installer

class IDABuddy(idaapi.plugin_t):
    flags = 0
    comment = 'IDABuddy'
    help = 'IDABuddy'
    wanted_name = 'IDABuddy'
    wanted_hotkey = ''

    def init(self):
        self._installer = Installer()
        self._installer.start()
        return idaapi.PLUGIN_KEEP

    def term(self):
        self._installer.stop()

    def run(self, arg):
        pass


def PLUGIN_ENTRY():
    return IDABuddy()