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

The system provides an efficient solution for building a container ecosystem. Users can easily configure deployement options for their respective machine learning models. User will be provided with a friendly interface to manage their container needs. This streamlined process reduces the time and effort required to manage deployement.

## 2. System Features

- Configurations management eg no of gpus, ram, automatic software installation support 

- Docker container management preferably using kubernetes

- Providing users with option to manage their deployement 

## 3. Non Functional Requirements

- Performance: The system should be able to handle high and perform efficiently, with quick response time.

- High Scalability

- Security: The system should implement appropriate security measures, such as encryption and secure access controls.

- High Availability

- Interoperability: The system should be able to integrate with other software solutions

- User-friendly: The system should be easy to use, with a user-friendly interface and intuitive functionality.

- Reliability: The system should be reliable, with minimal downtime and a high degree of stability.

- Compatibility: The system should be compatible with various data formats, allowing users to upload their own deployment config file.

- Maintainability: The system should be easy to maintain and upgrade, with clear documentation and a robust architecture.

# Design Specification
On a high level:
- Authenticate user
- Take config inputs from users reagrding the deployment requirements. eg - no of GPUs, CPUs, libraries reqd etc 
- Create a dynamic dockerfile or kubernetes deployment scripts according to user specifications
- Setup the deployment ecosystem
- Provide access to the deployment container.
