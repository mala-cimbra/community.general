#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018, Yanis Guenane <yanis+ansible@guenane.org>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r"""
module: scaleway_volume_info
short_description: Gather information about the Scaleway volumes available
description:
  - Gather information about the Scaleway volumes available.
author:
  - "Yanis Guenane (@Spredzy)"
  - "Remy Leone (@remyleone)"
extends_documentation_fragment:
  - community.general.scaleway
  - community.general.attributes
  - community.general.attributes.info_module

options:
  region:
    type: str
    description:
      - Scaleway region to use (for example C(par1)).
    required: true
    choices:
      - ams1
      - EMEA-NL-EVS
      - par1
      - EMEA-FR-PAR1
      - par2
      - EMEA-FR-PAR2
      - waw1
      - EMEA-PL-WAW1
"""

EXAMPLES = r"""
- name: Gather Scaleway volumes information
  community.general.scaleway_volume_info:
    region: par1
  register: result

- ansible.builtin.debug:
    msg: "{{ result.scaleway_volume_info }}"
"""

RETURN = r"""
scaleway_volume_info:
  description:
    - Response from Scaleway API.
    - 'For more details please refer to: U(https://developers.scaleway.com/en/products/instance/api/).'
  returned: success
  type: list
  elements: dict
  sample:
    [
      {
        "creation_date": "2018-08-14T20:56:24.949660+00:00",
        "export_uri": null,
        "id": "b8d51a06-daeb-4fef-9539-a8aea016c1ba",
        "modification_date": "2018-08-14T20:56:24.949660+00:00",
        "name": "test-volume",
        "organization": "3f709602-5e6c-4619-b80c-e841c89734af",
        "server": null,
        "size": 50000000000,
        "state": "available",
        "volume_type": "l_ssd"
      }
    ]
"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.general.plugins.module_utils.scaleway import (
    Scaleway, ScalewayException, scaleway_argument_spec,
    SCALEWAY_LOCATION)


class ScalewayVolumeInfo(Scaleway):

    def __init__(self, module):
        super(ScalewayVolumeInfo, self).__init__(module)
        self.name = 'volumes'

        region = module.params["region"]
        self.module.params['api_url'] = SCALEWAY_LOCATION[region]["api_endpoint"]


def main():
    argument_spec = scaleway_argument_spec()
    argument_spec.update(dict(
        region=dict(required=True, choices=list(SCALEWAY_LOCATION.keys())),
    ))

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    try:
        module.exit_json(
            scaleway_volume_info=ScalewayVolumeInfo(module).get_resources()
        )
    except ScalewayException as exc:
        module.fail_json(msg=exc.message)


if __name__ == '__main__':
    main()
