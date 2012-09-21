from bount.precompilers import LessPrecompiler, CoffeePrecompiler
from bount.stacks import *
from bount.stacks.goethe import GoetheStack
from path import path

__author__ = 'mturilin'

PROJECT_ROOT = path(__file__).dirname()

precompilers = [
    LessPrecompiler('less', 'compiled/css'),
    CoffeePrecompiler('less', 'compiled/js'),
    ]

stack = GoetheStack.build_stack(
    settings_module='settings',
    dependencies_path=PROJECT_ROOT.joinpath('requirements.txt'),
    project_name='neji',
    source_root=PROJECT_ROOT.joinpath('src'),
    precompilers=precompilers)




