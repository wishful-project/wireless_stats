import logging
import wishful_upis as upis
from wishful_agent.core import wishful_module

__author__ = "Piotr Gawlowicz"
__copyright__ = "Copyright (c) 2015, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{gawlowicz}@tkn.tu-berlin.de"


@wishful_module.build_module
class WirelessStatsApp(wishful_module.AgentModule):
    def __init__(self):
        super().__init__()
        self.log = logging.getLogger('WirelessStatsApp')

    @wishful_module.on_start()
    def myFunc_1(self):
        self.log.info("This function is executed on agent start".format())

    @wishful_module.on_exit()
    def myFunc_2(self):
        self.log.info("This function is executed on agent exit".format())
