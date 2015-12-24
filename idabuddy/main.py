import idaapi
idaapi.require('installer')

from installer import Installer

installer = Installer()
installer.start()