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

from os_vif import plugin
from os_vif import objects

from vif_plug_ovs import processutils
from vif_plug_ovs import linux_net

PLUGIN_NAME = 'hw_veb'


class HardwareVebPlugin(base.PluginBase):
    """
    A VIF type that plugs a virtual machine nework interface into a SR-IOV
    virtual function (VF) using a macvtap VNIC type.
    """

    def __init__(self, **config):
        processutils.configure(**config)

    def get_supported_vifs(self):
        return set([objects.PluginVIFSupport(PLUGIN_NAME, '1.0', '1.0')])

    def plug(self, instance, vif):
        if vif.vnic_type == vnic_types.MACVTAP:
            linux_net.set_vf_interface_vlan(vif.profile['pci_slot'],
                                            mac_addr=vif.address,
                                            vlan=vif.vlan)

    def unplug(self, vif):
        if vif.vnic_type == vnic_types.MACVTAP:
            # The ip utility doesn't accept the MAC 00:00:00:00:00:00.
            # Therefore, keep the MAC unchanged.  Later operations on
            # the same VF will not be affected by the existing MAC.
            linux_net.set_vf_interface_vlan(vif.profile['pci_slot'],
                                            mac_addr=vif.address)
