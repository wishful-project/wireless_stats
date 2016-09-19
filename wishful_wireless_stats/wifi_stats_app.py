import logging
import wishful_upis as upis
from wishful_agent.core import wishful_module

__author__ = "Anatolij Zubow"
__copyright__ = "Copyright (c) 2015, Technische Universitat Berlin"
__version__ = "0.1.0"
__email__ = "zubow@tkn.tu-berlin.de"


'''
    Wireless stats app for IEEE 802.11:
    - estimates the AP which serves the given STA
    - ...
'''
@wishful_module.build_module
class WifiStatsApp(wishful_module.ControllerModule):
    def __init__(self):
        super().__init__()
        self.log = logging.getLogger('WirelessStatsApp')
        self.nodes = {}

    @wishful_module.on_start()
    def start_wifi_stats_module(self):
        self.log.debug("Start HO module".format())
        self.running = True

    @wishful_module.on_exit()
    def stop_wifi_stats_module(self):
        self.log.debug("Stop HO module".format())
        self.running = False


    @wishful_module.on_event(upis.mgmt.NewNodeEvent)
    def add_node(self, event):
        node = event.node

        if self.mode == "GLOBAL" and node.local:
            return

        self.log.info("Added new node: {}, Local: {}"
                      .format(node.uuid, node.local))
        self.nodes[node.uuid] = node


    @wishful_module.on_event(upis.mgmt.NodeExitEvent)
    @wishful_module.on_event(upis.mgmt.NodeLostEvent)
    def remove_node(self, event):
        self.log.info("Node lost".format())
        node = event.node
        reason = event.reason
        if node.uuid in self.nodes:
            del self.nodes[node.uuid]
            self.log.info("Node: {}, Local: {} removed reason: {}"
                          .format(node.uuid, node.local, reason))


    @wishful_module.on_event(upis.wifi.WiFiGetServingAPRequestEvent)
    def get_AP_the_client_is_associated_with(self, event):
        """
        Estimates the AP which serves the given STA. Note: if an STA is associated with multiple APs the one with the
        smallest inactivity time is returned.
        """
        sta_mac_addr = event.sta_mac_addr
        wifi_intf = event.wifi_intf

        self.log.debug('Function: is_associated_with')

        try:
            nodes_with_sta = {}

            for node_uuid, node in self.nodes.items():
                res = node.iface(wifi_intf).blocking(
                    True).radio.get_inactivity_time_of_connected_devices()

                if sta_mac_addr in res:
                    self.log.debug(res[sta_mac_addr])
                    nodes_with_sta[node_uuid] = int(res[sta_mac_addr][0])

                    # dictionary of aps where station is associated
                    self.log.debug("STA found on the following APs with the following idle times:")
                    self.log.debug(str(nodes_with_sta))

            if not bool(nodes_with_sta):
                # If no serving AP was found; send None in reply event
                reply_event = upis.net_func.WiFiGetServingAPReplyEvent(sta_mac_addr, wifi_intf, None)
                self.send_event(reply_event)
                return

            # serving AP is the one with minimal STA idle value
            servingAP = min(nodes_with_sta, key=nodes_with_sta.get)
            self.log.info("STA %s is served by AP %s " % (sta_mac_addr, servingAP))

            reply_event = upis.net_func.WiFiGetServingAPReplyEvent(sta_mac_addr, wifi_intf, servingAP)
            self.send_event(reply_event)
            return

        except Exception as e:
            self.log.fatal("An error occurred in get_servingAP: %s" % e)
            raise e


