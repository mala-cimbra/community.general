# -*- coding: utf-8 -*-
# Copyright (c) 2025, Dexter Le <dextersydney2001@gmail.com>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.community.general.plugins.module_utils.cmd_runner import CmdRunner, cmd_runner_fmt


_state_map = {
    "present": "create",
    "absent": "remove",
    "status": "status",
    "enabled": "enable",
    "disabled": "disable",
    "online": "start",
    "offline": "stop",
    "maintenance": "set",
    "config": "config",
    "cleanup": "cleanup",
}


def fmt_resource_type(value):
    return [value[k] for k in ['resource_standard', 'resource_provider', 'resource_name'] if value.get(k) is not None]


def fmt_resource_operation(value):
    cmd = []
    for op in value:
        cmd.append("op")
        cmd.append(op.get('operation_action'))
        for operation_option in op.get('operation_option'):
            cmd.append(operation_option)

    return cmd


def fmt_resource_argument(value):
    return ['--group' if value['argument_action'] == 'group' else value['argument_action']] + value['argument_option']


def get_pacemaker_maintenance_mode(runner):
    with runner("cli_action config") as ctx:
        rc, out, err = ctx.run(cli_action="property")
        maintenance_mode_output = list(filter(lambda string: "maintenance-mode=true" in string.lower(), out.splitlines()))
        return bool(maintenance_mode_output)


def pacemaker_runner(module, **kwargs):
    runner_command = ['pcs']
    runner = CmdRunner(
        module,
        command=runner_command,
        arg_formats=dict(
            cli_action=cmd_runner_fmt.as_list(),
            state=cmd_runner_fmt.as_map(_state_map),
            name=cmd_runner_fmt.as_list(),
            resource_type=cmd_runner_fmt.as_func(fmt_resource_type),
            resource_option=cmd_runner_fmt.as_list(),
            resource_operation=cmd_runner_fmt.as_func(fmt_resource_operation),
            resource_meta=cmd_runner_fmt.stack(cmd_runner_fmt.as_opt_val)("meta"),
            resource_argument=cmd_runner_fmt.as_func(fmt_resource_argument),
            apply_all=cmd_runner_fmt.as_bool("--all"),
            wait=cmd_runner_fmt.as_opt_eq_val("--wait"),
            config=cmd_runner_fmt.as_fixed("config"),
            force=cmd_runner_fmt.as_bool("--force"),
        ),
        **kwargs
    )
    return runner
