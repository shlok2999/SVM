import os

# Define the system requirements
system_requirements = {
    "cpu": "1",
    "gpu": "1",
    "ram": "2g",
    "python": "3.9.2",
    "packages": [
        "flask==2.0.1",
        "numpy==1.20.2",
        "pandas==1.2.3"
    ]
}

# Define the Dockerfile contents
dockerfile_contents = f"""
FROM nvidia/cuda:11.4.0-cudnn8-runtime-ubuntu20.04
RUN apt-get update && \\
    apt-get install -y python3-pip && \\
    pip3 install {' '.join(system_requirements['packages'])}
ENV CPU_COUNT {system_requirements['cpu']}
ENV GPU_COUNT {system_requirements['gpu']}
ENV RAM_COUNT {system_requirements['ram']}
WORKDIR /app
COPY . /app
CMD [ "python3", "app.py" ]
"""

try:
    # Write the Dockerfile to disk
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_contents)

    # Build the Docker image
    os.system("docker build -t myapp .")
    
    print("Docker image built successfully!")
    
except Exception as e:
    print(f"Error: {e}")