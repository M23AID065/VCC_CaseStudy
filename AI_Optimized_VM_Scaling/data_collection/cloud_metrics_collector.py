import boto3
import googleapiclient.discovery
import requests
import psutil
import time
import json

# AWS CloudWatch Metrics Collection
def get_aws_metrics(instance_id, region="us-east-1"):
    cloudwatch = boto3.client("cloudwatch", region_name=region)
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=time.time() - 300,
        EndTime=time.time(),
        Period=60,
        Statistics=["Average"],
    )
    cpu_utilization = response["Datapoints"][0]["Average"] if response["Datapoints"] else 0
    return {"cpu_usage": cpu_utilization}

# GCP Stackdriver Metrics Collection
def get_gcp_metrics(project_id, instance_id, zone):
    compute = googleapiclient.discovery.build("compute", "v1")
    request = compute.instances().get(project=project_id, zone=zone, instance=instance_id)
    response = request.execute()
    cpu_usage = response.get("cpuPlatform", "Unknown")
    return {"cpu_usage": cpu_usage}

# Azure Monitor Metrics Collection
def get_azure_metrics(subscription_id, resource_group, vm_name):
    token = "YOUR_AZURE_ACCESS_TOKEN"
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{vm_name}/instanceView?api-version=2022-08-01"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.get(url, headers=headers).json()
    cpu_usage = response.get("statuses", [{}])[0].get("code", "Unknown")
    return {"cpu_usage": cpu_usage}

# Local System Metrics Collection
def get_local_metrics():
    return {
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "network_usage": psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv,
    }

# Main Data Collection Loop
if __name__ == "__main__":
    while True:
        aws_metrics = get_aws_metrics("i-0abcdef1234567890")
        gcp_metrics = get_gcp_metrics("my-project-id", "my-instance-id", "us-central1-a")
        azure_metrics = get_azure_metrics("my-subscription-id", "my-resource-group", "my-vm-name")
        local_metrics = get_local_metrics()

        all_metrics = {
            "AWS": aws_metrics,
            "GCP": gcp_metrics,
            "Azure": azure_metrics,
            "Local": local_metrics,
        }

        print(json.dumps(all_metrics, indent=4))
        time.sleep(10)  # Collect data every 10 seconds
