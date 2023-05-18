# SVM
### Project Category : AI Model Training/ Execution
### Project Name : Data Foundation Cloud (DCloud) Envronment 
### Team Members:
### Shlok Bansal : 2021201046
### Vishal Pandey : 2021201070
### Mayank Mukundam : 2021201057
### Project Overview:
1. Docker nodes with defined dataset and constrained resource access (GPU/CPU, storage and memory)
2.  Python and NVIDIA based AI/ ML setup for TensorFlow and PyTorch
# Software Requirements
## 1. Introduction

The system provides an efficient solution for building a containerised ecosystem. Users can easily configure these ecosystems according to their requirements but within constraints of limited CPUs, GPUs, memory. User will be provided with a friendly interface to manage all sorts of configurations. This streamlined process reduces the time and effort required to manage the ecosystem.

## 2. System Features

- Configurations management eg no of gpus, ram, automatic software installation support 

- Docker container management according to requirements

- Container monitoring

- Real Time Status Updates

- handle concurrent requests

- Support for configuration templates

## 3. Non Functional Requirements

- Performance: The system should be able to handle high and perform efficiently, with quick response time.

- High Scalability

- High Availability

- Interoperability: The system should be able to integrate with DFS platform

- User-friendly: The system should be easy to use, with a user-friendly interface and intuitive functionality.

- Reliability: The system should be reliable, with minimal downtime and a high degree of stability.

- Compatibility: The system should be compatible with various data formats, allowing users to upload their own ecosystem config files.

- Maintainability: The system should be easy to maintain and upgrade, with clear documentation and a robust architecture.

## 4. Project Deliverable
The project will be delivered in phases:
- Prototype phase: Building a simple and efficient prototype to demonstrate the workflow for container ecosystem deployment
- Concurrency support: This phase will mostly focus on making the abover prototype more rustic and handle traffic efficiently

    
    
    ![dfs](https://github.com/shlok2999/SVM/blob/main/dfs_new.png)

    As shown in the above diagram, the UI will appear in the as a form wherein user will get to choose the language version user will work on, library user wants to get support of in their Ecosystem, Computing Requirements for the Ecosystem. All the libraries & langiages resource requirements will be a dropdwon which shows the list of resources that are avialbale to create an ecosystem.
      
- Logging and Fault Tolerance
- Final Backend: This phase will contain all above deliverables plus support for templates.
- UI Integration phase
    This phase deals with the Integration of whole backend with a UI Interface so that, it can be easily used by the end user.

## Architecture Overview
![dfs](https://github.com/shlok2999/SVM/blob/shlok/dfs_arch_v2.png)

## Configuration Contract
### Env Config
![dfs](https://github.com/shlok2999/SVM/blob/shlok/contracts/dfs_config.png)

### Services Self Regsiter Contract
![dfs](https://github.com/shlok2999/SVM/blob/shlok/contracts/dfs_service.png)

### Library Contract
![dfs](https://github.com/shlok2999/SVM/blob/shlok/contracts/dfs_library.png)

### Deployment Config
![dfs](https://github.com/shlok2999/SVM/blob/shlok/contracts/dfs_deployment.png)

### Templates Config
![dfs](https://github.com/shlok2999/SVM/blob/shlok/contracts/dfs_template.png)

## 4. How to Run
Project can be run by following below given steps:
- Have a mongo db instance running either in local or mongo atlas and replace the mongo connection url in the code
- Run the following services one by one:
    -   Run the main API server: python3 dfs_server/app.py (apis to be accessed by frontend)
    -   Run node agents, one for each deployable node: python3 dfs_node/app.py
    -   Run kafka consumer service, one for each deployable node: python3 dfs_node/kiafka_consumer.py
    -   Run the node manager serrvice: python3 node_manager/app.py
    -   Run the node monitor serrvice: python3 dfs_monitor/app.py

