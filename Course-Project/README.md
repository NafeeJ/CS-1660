# Course Project - Big Data Toolbox

## Run this project
Below are the steps needed to run this project on your Docker Engine. It is assumed that you want to run on a Google Kubernetes Engine Cluster

1. Pull Docker image
```
docker pull nafeej/bigdata-toolbox
```

2. Run Docker image
```
docker run -dit nafeej/bigdata-toolbox
```
This will produce a container ID. Copy it as shown below (yours will be different):\
<img src="docker_run.jpg">

3. Enter container shell
```
docker exec -it (YOUR_CONTAINER_ID) bash
```

4. Create GCP project (skip if you have one already)
    * Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)
    * Click "Select a project"\
    <img src="select_project.jpg">
    * Click "New project"\
    <img src="new_project.jpg">
    * Set up project name and ID and click "Create"\
    <img src="create_project.jpg">

5. Authorize glcoud
```
gcloud auth login
```
Simply follow the instructions given by Google (make sure you choose the Google account you want the GKE cluster to run on)

6. Set Project ID
```
gcloud config set project (YOUR_PROJECT_ID)
```

7. Set up kubernetes cluster (skip if you have one already)
    * Search for Kubernetes Engine in GCP\
    <img src="kube_search.jpg">
    * Enable Kubernetes API\
    <img src="kube_enable.jpg">
    * Create cluster\
    <img src="kube_create.jpg">
    * Choose autopilot mode\
    <img src="kube_mode.jpg">
    * Name cluster and click create\
    <img src="kube_create2.jpg">

8. Connect cluster to container
    * Click on cluster\
    <img src="cluster_click.jpg">
    * Click on connect\
    <img src="cluster_connect.jpg">
    * Copy command\
    <img src="cluster_copy.jpg">
    * Paste command in shell\
    <img src="cluster_paste.jpg">

9. Run driver
```
python3 main.py
```