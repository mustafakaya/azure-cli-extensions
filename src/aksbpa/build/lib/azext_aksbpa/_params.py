# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long

from knack.arguments import CLIArgumentType


def load_arguments(self, _):

    from azure.cli.core.commands.parameters import tags_type
    from azure.cli.core.commands.validators import get_default_location_from_resource_group

    aksbpa_name_type = CLIArgumentType(options_list='--aksbpa-name-name', help='Name of the Aksbpa.', id_part='name')

    with self.argument_context('aksbpa') as c:
        c.argument('tags', tags_type)
        c.argument('location', validator=get_default_location_from_resource_group)
        #c.argument('aksbpa_name', aksbpa_name_type, options_list=['--name', '-n'])
        c.argument('name', options_list=['-n', '--name'], help='AKS Cluster Name')
        c.argument('resource_group', options_list=['-r', '--resource-group'], help='Resource Group Name')
        c.argument('subscription', aksbpa_name_type, options_list=['--subscription', '-s'], help='Subscription Id')

    with self.argument_context('aksbpa list') as c:
        c.argument('aksbpa_name', aksbpa_name_type, id_part=None)
