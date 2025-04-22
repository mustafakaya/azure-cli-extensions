# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType
from azext_aksbpa._client_factory import cf_aksbpa
from tabulate import tabulate

def load_command_table(self, _):
    from .custom import aks_bpa_scan
    aks_bpa_command = CliCommandType(
        operations_tmpl='{}#{}'.format(__name__.replace('.commands', '.custom'), 'aks_bpa_scan')
    )
    with self.command_group('aks-bpa', aks_bpa_command) as g:
        g.command('scan', 'aks_bpa_scan')


    with self.command_group('aksbpa', is_preview=True):
        pass


