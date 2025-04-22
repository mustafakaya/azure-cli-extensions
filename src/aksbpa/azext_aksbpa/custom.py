# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from azure.mgmt.containerservice import ContainerServiceClient
from azure.cli.core.azclierror import CLIError
from azure.cli.core.azclierror import ResourceNotFoundError
from azext_aksbpa.checker import run_all_recommendations
from tabulate import tabulate
from azure.cli.core.commands.client_factory import get_mgmt_service_client

def create_aksbpa(cmd, resource_group_name, aksbpa_name, location=None, tags=None):
    raise CLIError('TODO: Implement `aksbpa create`')


def list_aksbpa(cmd, resource_group_name=None):
    raise CLIError('TODO: Implement `aksbpa list`')


def update_aksbpa(cmd, instance, tags=None):
    with cmd.update_context(instance) as c:
        c.set_param('tags', tags)
    return instance

def aks_bpa_scan(cmd, name, resource_group):
    print(f"Scanning AKS cluster '{name}' in resource group '{resource_group}'...\n")

    cluster_info = get_cluster_info(cmd, name, resource_group)
    recommendations = run_all_recommendations(cmd, cluster_info)    

    # print_cluster_info(cluster_info)
    print("")
    print_recommendation_table(recommendations, name)
    print("\n")
    return "completed."


def get_cluster_info(cmd, name, resource_group):
    try:
        client = get_mgmt_service_client(cmd.cli_ctx, ContainerServiceClient)
        cluster = client.managed_clusters.get(resource_group, name)
        return cluster
        """
        return {
           "clusterName": cluster.name,
          "location": cluster.location,
            "kubernetesVersion": cluster.kubernetes_version,
            "provisioningState": cluster.provisioning_state,
            "nodeResourceGroup": cluster.node_resource_group,
            "dnsPrefix": cluster.dns_prefix,
            "fqdn": cluster.fqdn
        }"""    ""
    except Exception as ex:
        raise CLIError(f"Failed to fetch AKS cluster info: {str(ex)}")


def print_cluster_info(cluster_info):
     print("Cluster Info:")
   #  for key, value in cluster_info.items():
     #    print(f"  {key}: {value}")


def print_recommendation_table(results, cluster_name):
    table = []
    for r in results:
        status = r.get("status")
        if status == "Passed":
            status_emoji = "✅"
        elif status == "Failed":
            status_emoji = "❌"
        elif status == "CouldNotValidated":
            status_emoji = "⚠️"  
        else:
            status_emoji = "❓"  

        table.append([
            r.get("category"),
            r.get("recommendation_name"),
            cluster_name,
            status_emoji
        ])
    print("\nBest Practice Assessment Results:\n")
    print(tabulate(table, headers=["Category","Recommendation name", "Cluster name", "Status"]))

