from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
import time

config.load_kube_config()
kube_core = client.CoreV1Api()
kube_client = client.ApiClient()

ports = {
    "jupyter-service": 8888,
    "spark-service": 8080
}

pods = [
    "jupyter-deployment",
    "spark-deployment"
]

services = [
    "jupyter-service",
    "spark-service"
]

deployments = [
    "jupyter-deployment",
    "spark-deployment",
    "sparkworker-deployment"
]

def create(path, name):
    print(f"creating: '{name}'...")
    # utils.create_from_yaml(kube_client, path)
    try:
        utils.create_from_yaml(kube_client, path)
        print(f"'{name}' created")
    except:
        print(f"'{name}' already exists or an error occurred")

create("yaml/jupyter.yaml", "Jupyter Notebook")
create("yaml/spark.yaml", "Apache Spark")

# Wait for pods to be created
created = False
while not created:
    pods_response = kube_core.list_pod_for_all_namespaces()
    created = True
    cur_pods = []
    for pod in pods_response.items:
        cur_pods.append("-".join(pod.metadata.name.split("-", 2)[:2])) # cut off the random characters added to pod name by kubernetes
    not_created = []
    for pod in pods:
        # print(pod)
        # print(cur_pods)
        if pod not in cur_pods:
            not_created.append(pod)
            created = False
            break
    for pod in not_created:
        print(f"Waiting on {pod} pod creation...")
    # print(created)
    time.sleep(1)
print("All pods created.")

# Wait for all pods to be ready
ready = False
while not ready:
    pods_response = kube_core.list_pod_for_all_namespaces()
    not_running = True
    for pod in pods_response.items:
        status = pod.status.phase
        if status != "Running":
            # print(pod.status)
            print(f"Waiting on pod '{pod.metadata.name}' ...")
            not_running = False
    ready = not_running
    if ready == False:
        time.sleep(5)
print("All pods ready.")

urls = {}

services_response = kube_core.list_service_for_all_namespaces()
for service in services_response.items:
    # print(f"STATUS: {service.status}")
    ingress = service.status.load_balancer.ingress
    external_ip = None
    if ingress:
        while ingress[0].ip == None or ingress[0].ip == "None":
            print(f"External IP pending for {service.metadata.name}")
            time.sleep(1)
        if ingress[0].ip:
            # print(ingress)
            external_ip = ingress[0].ip
        else:
            external_ip = "localhost"
    if service.metadata.name in ports:
        # print(f"URL: {external_ip}:{ports[service.metadata.name]}")
        urls[service.metadata.name] = f"{external_ip}:{ports[service.metadata.name]}"


print("----------")

print("Welcome to Big Data Processing Application")
print("Please type the number that corresponds to the application you want to run:")

def print_options():
    print("-----")
    print("1. Apache Hadoop")
    print("2. Apache Spark")
    print("3. Jupyter Notebook")
    print("4. SonarQube and SonarScanner")
    print("5. Quit")
    print("-----")

while True:
    print_options()
    try:
        app = int(input("Type the number here > "))
        if app == 1:
            print("Launching Apache Hadoop")
        elif app == 2:
            pods_response = kube_core.list_pod_for_all_namespaces()
            worker = ""
            for pod in pods_response.items:
                if "sparkworker" in pod.metadata.name:
                    worker = pod.metadata.name
            cmd = ['bash']
            print(f"WORKER {worker}")
            stream(kube_core.connect_get_namespaced_pod_exec,
                  worker,
                  'default',
                  command=cmd,
                  stderr=True, stdin=True,
                  stdout=True, tty=True,
                  _preload_content=False)
            print(f"Follow the URL: http://{urls['spark-service']}")
        elif app == 3:
            print(f"Follow the URL: http://{urls['jupyter-service']}")

        elif app == 4:
            print("Launching SonarQube and SonarScanner")
        elif app == 5:
            for deployment in deployments:
                print(f"Deleting '{deployment}'...")
                kube_apps = client.AppsV1Api(kube_client)
                kube_apps.delete_namespaced_deployment(name=deployment, namespace='default', async_req=True)
            for service in services:
                print(f"Deleting '{service}'...")
                kube_core.delete_namespaced_service(name=service, namespace='default', async_req=True)
            break
        else:
            print("Not an option")
    except:
        print("Give a number")