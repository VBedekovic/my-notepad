from importlib import import_module, invalidate_caches
from IPlugin import *
import os

def myfactory(moduleName):
    invalidate_caches()
    pluginModule = import_module("plugins." + moduleName)
    return getattr(pluginModule, "construct")

def loadPlugins():
    plugins: list[Plugin] = []
    for mymodule in os.listdir('plugins'):
        moduleName, moduleExt = os.path.splitext(mymodule)
        if moduleExt=='.py':
            plugin=myfactory(moduleName)()
            plugins.append(plugin)     
    return plugins
