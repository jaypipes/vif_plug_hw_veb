#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Implements vlans, bridges, and iptables rules using linux utilities."""

import os

from oslo_log import log as logging
from oslo_utils import excutils
from os_vif import pci

from vif_plug_hw_veb.i18n import _LE
from vif_plug_hw_veb import processutils

LOG = logging.getLogger(__name__)


def set_vf_interface_vlan(pci_addr, mac_addr, vlan=0):
    pf_ifname = pci.get_ifname_by_pci_address(pci_addr, pf_interface=True)
    vf_ifname = pci.get_ifname_by_pci_address(pci_addr)
    vf_num = pci.get_vf_num_by_pci_address(pci_addr)

    # Set the VF's mac address and vlan
    exit_code = [0, 2, 254]
    port_state = 'up' if vlan > 0 else 'down'
    processutils.execute('ip', 'link', 'set', pf_ifname,
                         'vf', vf_num,
                         'mac', mac_addr,
                         'vlan', vlan,
                         check_exit_code=exit_code,
                         run_as_root=True)
    # Bring up/down the VF's interface
    processutils.execute('ip', 'link', 'set', vf_ifname,
                         port_state,
                         check_exit_code=exit_code,
                         run_as_root=True)
