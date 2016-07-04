import imp
import os

PluginFolder = "./plugins"
MainModule = "__init__"

def get_plugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for plugin in possibleplugins:
        location = os.path.join(PluginFolder, plugin)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins.append({"name": plugin, "info": info})
    return plugins

def load_plugin(plugin):
    return imp.load_module(MainModule, *plugin["info"])

def load_plugin_from_name(pluginname):
    location = os.path.join(PluginFolder, pluginname)
    if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
        return False
    info = imp.find_module(MainModule, [location])
    return load_plugin({"name": pluginname, "info": info})

