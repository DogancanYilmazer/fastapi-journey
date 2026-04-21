### 1. What components do you see running in kube-system? Can you identify any components from the lecture (scheduler, etcd, api-server)?

- CoreDNS: Provides DNS service discovery for pods and services inside the cluster.
- etcd: Stores the cluster's state and configuration data.
- kube-apiserver: Handles API requests and is the main control plane entry point.
- kube-controller-manager: Runs controllers that keep the desired and actual state aligned.
- kube-proxy: Manages Service networking and routes traffic to the correct pods.
- kube-scheduler: Assigns newly created pods to suitable nodes.
- storage-provisioner: Dynamically provisions storage volumes when requested.

### 2. In the Events section of kubectl describe, what sequence of events happened before the pod started running? Which component scheduled the pod?

Assigned my-pod to minikube, Pulling image "python:3.9-slim", Created container, Started container. The scheduler component scheduled the pod.

### 3. Why does platform.node() return the pod name? What does this tell you about container networking isolation?

Because Kubernetes assigns a unique hostname to each pod, which is the same as the pod name. This indicates that each pod has its own network namespace, providing isolation between pods.

### 4. After deleting the pod manually, did Kubernetes bring it back? Why or why not?

No. It was a standalone Pod, and without a controller (like a Deployment), Kubernetes does not recreate deleted Pods.


### 5. What would need to be different (hint: think about what you'll learn in Lecture 4) for Kubernetes to automatically restart a deleted pod?
This question has a deliberate answer: a standalone pod has no controller watching over it. You need a Deployment for self-healing. You'll build one in Lecture 4.



### 1. What is the difference between running a container with `docker run` and deploying a pod with `kubectl run`? Both used the same image — what changed?

`docker run` starts one container you manage directly on your local machine. `kubectl run` creates a Pod in Kubernetes, which is scheduled on a cluster node and managed by Kubernetes as part of a larger, scalable system.


### 2. In `kubectl describe pod`, what is the role of the **Scheduler** event? Which control plane component does that correspond to?

It means the pod was assigned to a node by the Kubernetes scheduler, which is the kube-scheduler control plane component.

### 3. In `kubectl get pods -n kube-system`, name two components you recognised from the lecture and describe what they do.

`kube-apiserver` handles all API requests and is the main entry point to the cluster, while `etcd` stores the cluster state and configuration data.

### 4. **Image-specific observation** (answer only the one relevant to your image):
   - 🐍 Python: Why does `platform.node()` return the pod name? What does this tell you about how Kubernetes assigns identities to pods?

It returns the pod name because Kubernetes sets each pod's hostname to a unique pod name.

### 5. Task 6 reflection: After deleting the pod, Kubernetes did **not** restart it. In one paragraph, explain why, and what Kubernetes object would change this behaviour.

It did not restart because a standalone Pod has no controller; a Deployment would recreate it automatically.