import os
import json
from azure.cli.core._profile import Profile
from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest

def load_kql_query(name):
    base_path = os.path.dirname(__file__)
    kql_path = os.path.join(base_path, "kql", name)
    with open(kql_path, "r") as f:
        return f.read()

def load_recommendations():
    try:
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "recommendations.json")
        with open(file_path, "r") as f:
            return json.load(f)
    except Exception as e:
        print("❌ Failed to load recommendations file:", e)
        return []

def run_azure_resource_graph(cmd, query):
    try:
        profile = Profile(cli_ctx=cmd.cli_ctx)
        credential, subscription_id, _ = profile.get_login_credentials()

        client = ResourceGraphClient(credential)
        request = QueryRequest(
            query=query,
            subscriptions=[subscription_id]
        )

        result = client.resources(request)
        return result.data
    except Exception as e:
        print("❌ Failed to run ARG query:", e)
        return []

def evaluate_object_key(cluster_info, recommendation: dict):
    try:
        if "object_key" not in recommendation:
            return None
        if recommendation["object_key"] == "CouldNotValidated":
            return "CouldNotValidated"

        keys = recommendation["object_key"].replace("[", ".[").split(".")
        value = cluster_info

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, {})
            elif isinstance(value, list) and key.startswith("[") and key.endswith("]"):
                idx = int(key[1:-1])
                value = value[idx]
            else:
                value = getattr(value, key, {})

        expected_value = recommendation["object.value"]

        
        if isinstance(expected_value, str) and "|" in expected_value:
            allowed_values = [v.strip() for v in expected_value.split("|")]
            return str(value) in allowed_values

        
        if isinstance(expected_value, list):
            return all(item in value for item in expected_value)

        return str(value) == str(expected_value)

    except Exception as e:
        print(f"❌ Error evaluating recommendation '{recommendation.get('recommendation_name')}': {e}")
        return False


def run_all_recommendations(cmd, cluster_info):
    results = []
    cluster_info_dict = cluster_info.as_dict()
    recommendations = load_recommendations()

    seen = set()

    for check in recommendations:
        name = check.get("recommendation_name")
        if name in seen:
            continue  # Skip duplicates
        seen.add(name)

        status = "CouldNotValidated"

        if "query_file" in check:
            try:
                query = load_kql_query(check["query_file"])
                query_results = run_azure_resource_graph(cmd, query)

                filtered_results = []
                if isinstance(query_results, list):
                    for item in query_results:
                        if item.get("name") == cluster_info.name:
                            filtered_results.append(item)
                else:
                    print("❌ Unexpected ARG query result format")

                status = "Passed" if len(filtered_results) == 0 else "Failed"
            except Exception as e:
                print(f"❌ Error running ARG query for {check['recommendation_name']}: {e}")
                status = "CouldNotValidated"

        elif "object_key" in check:
            result = evaluate_object_key(cluster_info_dict, check)
            if result == "CouldNotValidated":
                status = "CouldNotValidated"
            elif result:
                status = "Passed"
            else:
                status = "Failed"

        results.append({
            "recommendation_name": name,
            "category": check.get("category"),
            "cluster": cluster_info.name,
            "status": status
        })

    return results

