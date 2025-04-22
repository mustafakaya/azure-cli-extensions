# Azure CLI AKS Best Practice Assessment Extension (Preview)

This is an Azure CLI extension that performs **Best Practice Assessments (BPA)** on Azure Kubernetes Service (AKS) clusters.  
It evaluates your clusters against a set of recommendations based on the **[Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/architecture/framework/)** across five key pillars:

- ✅ **Reliability**  
- 🔐 **Security**  
- 💰 **Cost Optimization**  
- ⚙️ **Operational Excellence**  
- 🚀 **Performance Efficiency** *(planned)*

The goal is to help you identify gaps, improve configurations, and align your AKS environment with Microsoft-recommended architecture best practices.

---

## 🚀 Features

- 🔍 JSON-driven recommendation engine  
- 💡 Support for deep `cluster_info` attribute checks  
- 📊 Azure Resource Graph (ARG) support for advanced queries  
- 🟢 ✅ Passed / ❌ Failed / ⚠️ CouldNotValidated status mapping  
- 🧪 CLI-friendly results view for easy scanning  

---

## 📦 How to Install

Install the extension using Azure CLI:

```bash
az extension add --source aksbpa
```

## 🛠️ How to Use

Run the assessment against your AKS cluster:

```bash
az aks-bpa scan --resource-group <resource-group-name> --name <aks-cluster-name>
```

The extension evaluates all configured best practices and returns a detailed table of results.

---

## 📄 Recommendation Format (`recommendations.json`)

Each rule in the assessment is defined in JSON like this:

```json
{
  "recommendation_name": "Update AKS tier to Standard or Premium",
  "object_key": "sku.tier",
  "object.value": "Standard | Premium",
  "category": "Reliability"
}
```

object_key: Dot-notated path to the property in the AKS cluster object

object.value: Expected value(s). Use | to specify multiple valid values

query_file: Optional KQL file for ARG-based checks

## 📊 Sample Output

```text
Category           Recommendation                                          Cluster                 Status
-----------------  ------------------------------------------------------  ----------------------  -------
Security           Use Microsoft Entra Workload ID                        aks-prod-cluster        ❌
Reliability        Deploy AKS cluster across availability zones           aks-prod-cluster        ✅
Cost Optimization  Choose the right VM size                               aks-prod-cluster        ⚠️
```


![image](https://github.com/user-attachments/assets/1d213ead-95b1-4f69-8562-f179997b5f65)

##  📚 References
This extension is built with guidance and recommendations inspired by:

[Azure Well-Architected Framework](https://learn.microsoft.com/en-us/azure/well-architected/) 

[Azure Proactive Resiliency Library (APRL)](https://azure.github.io/Azure-Proactive-Resiliency-Library-v2/welcome/)

These resources serve as the foundation for many of the best practice checks implemented in the AKS BPA CLI extension.

## 🐞 Known Issues

- JSON parsing errors can occur if `recommendations.json` is not formatted properly.
- ARG-based recommendations require appropriate subscription-level permissions.
- Clusters with limited RBAC may not return full `cluster_info`.

## 🤝 Contributing

This tool is perfect for platform engineers, DevOps, and SREs looking to validate AKS clusters against real-world best practices.

**Contributions are welcome!** PRs, issues, and ideas are always appreciated. 🙏  
Let’s build better clusters. 🚀

