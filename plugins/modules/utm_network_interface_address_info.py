#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2018, Juergen Wiebe <wiebe@e-spirit.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
module: utm_network_interface_address_info

author:
  - Juergen Wiebe (@steamx)

short_description: Get info for a network/interface_address object

description:
  - Get info for a network/interface_address object in SOPHOS UTM.
attributes:
  check_mode:
    version_added: 3.3.0
    # This was backported to 2.5.4 and 1.3.11 as well, since this was a bugfix

options:
  name:
    type: str
    description:
      - The name of the object that identifies the entry.
    required: true

extends_documentation_fragment:
  - community.general.utm
  - community.general.attributes
  - community.general.attributes.info_module
"""

EXAMPLES = r"""
- name: Get network interface address info
  utm_proxy_interface_address_info:
    utm_host: sophos.host.name
    utm_token: abcdefghijklmno1234
    name: TestNetworkInterfaceAddress
"""

RETURN = r"""
result:
  description: The utm object that was created.
  returned: success
  type: complex
  contains:
    _ref:
      description: The reference name of the object.
      type: str
    _locked:
      description: Whether or not the object is currently locked.
      type: bool
    _type:
      description: The type of the object.
      type: str
    name:
      description: The name of the object.
      type: str
    address:
      description: The ip4 address of the network/interface_address object.
      type: str
    address6:
      description: The ip6 address of the network/interface_address object.
      type: str
    comment:
      description: The comment string.
      type: str
    resolved:
      description: Whether or not the object is resolved.
      type: bool
    resolved6:
      description: Whether or not the object is resolved.
      type: bool
"""

from ansible_collections.community.general.plugins.module_utils.utm_utils import UTM, UTMModule
from ansible.module_utils.common.text.converters import to_native


def main():
    endpoint = "network/interface_address"
    key_to_check_for_changes = []
    module = UTMModule(
        argument_spec=dict(
            name=dict(type='str', required=True)
        ),
        supports_check_mode=True,
    )
    try:
        UTM(module, endpoint, key_to_check_for_changes, info_only=True).execute()
    except Exception as e:
        module.fail_json(msg=to_native(e))


if __name__ == '__main__':
    main()
