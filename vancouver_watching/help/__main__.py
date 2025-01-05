from blueness import module
from blue_options.help.functions import help_main

from vancouver_watching import NAME
from vancouver_watching.help.functions import help_functions

NAME = module.name(__file__, NAME)


help_main(NAME, help_functions)
