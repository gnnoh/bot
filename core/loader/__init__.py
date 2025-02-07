import importlib
import os
import re
import traceback

from core.elements import Command, Option, Schedule
from core.logger import Logger

err_prompt = []

load_dir_path = os.path.abspath('./modules/')


def load_modules():
    fun_file = None
    dir_list = os.listdir(load_dir_path)
    for file_name in dir_list:
        try:
            file_path = f'{load_dir_path}/{file_name}'
            fun_file = None
            if os.path.isdir(file_path):
                if file_name != '__pycache__':
                    fun_file = file_name
            if fun_file is not None:
                Logger.info(f'Loading modules.{fun_file}...')
                modules = 'modules.' + fun_file
                importlib.import_module(modules)
                Logger.info(f'Succeeded loaded modules.{fun_file}!')
        except:
            tb = traceback.format_exc()
            Logger.info(f'Failed to load modules.{fun_file}: \n{tb}')
            err_prompt.append(str(tb))


class ModulesManager:
    _modules_list = set()

    @staticmethod
    def add_module(module: [Command, Option, Schedule]):
        ModulesManager._modules_list.add(module)

    @staticmethod
    def return_modules_list():
        return ModulesManager._modules_list

    @staticmethod
    def return_modules_list_as_dict():
        d = {}
        modules = []
        recommend_modules = []
        for alias in ModulesManager.return_modules_alias_map():
            modules.append(alias)
        for x in ModulesManager._modules_list:
            prefix = x.bind_prefix
            if prefix in d:
                raise ValueError(f'Duplicate bind prefix "{prefix}"')
            d.update({prefix: x})
            modules.append(prefix)
            recommend = x.recommend_modules
            if isinstance(recommend, str):
                recommend_modules.append(recommend)
            if isinstance(recommend, (list, tuple)):
                for y in recommend:
                    recommend_modules.append(y)
        for rm in recommend_modules:
            if rm not in modules:
                raise ValueError(f'Invalid recommend module "{rm}"')
        return d

    @staticmethod
    def return_modules_alias_map():
        alias_map = {}
        for x in ModulesManager._modules_list:
            if isinstance(x.alias, str):
                alias_map.update({x.alias: x.bind_prefix})
            if isinstance(x.alias, (tuple, list)):
                for y in x.alias:
                    alias_map.update({y: x.bind_prefix})
            if isinstance(x.alias, dict):
                alias_map.update(x.alias)
        return alias_map

    @staticmethod
    def return_modules_developers_map():
        d = {}
        for x in ModulesManager._modules_list:
            if x.developers is not None:
                d.update({x.bind_prefix: x.developers})
        return d

    @staticmethod
    def return_regex_modules():
        d = {}
        for x in ModulesManager._modules_list:
            if isinstance(x, Command) and x.is_regex_function:
                d.update({x.bind_prefix: x})
        return d

    @staticmethod
    def return_modules_help():
        d = {}
        for x in ModulesManager._modules_list:
            if x.help_doc is not None:
                d.update({x.bind_prefix: x.help_doc})
        return d

    @staticmethod
    def return_schedule_function_list():
        l = []
        for x in ModulesManager._modules_list:
            if isinstance(x, Schedule):
                l.append(x)
        return l


load_modules()
Modules = ModulesManager.return_modules_list_as_dict()
ModulesAliases = ModulesManager.return_modules_alias_map()
ModulesRegex = ModulesManager.return_regex_modules()
ModulesHelp = ModulesManager.return_modules_help()

loadercache = os.path.abspath('.cache_loader')
openloadercache = open(loadercache, 'w')
if err_prompt:
    err_prompt = re.sub('  File "<frozen importlib.*?>", .*?\n', '', '\n'.join(err_prompt))
    openloadercache.write('加载模块中发生了以下错误，对应模块未加载：\n' + err_prompt)
else:
    openloadercache.write('所有模块已正确加载。')
openloadercache.close()
