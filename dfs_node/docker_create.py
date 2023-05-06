import json
import subprocess
from python_on_whales import docker, DockerClient
from utils import *
import os

def install_os(os_name, installation_steps):
	os_tags = "latest"

	dockerfile_content = []
	dockerfile_content.append(f"""FROM {os_name}:{os_tags}\n""")

	if "init-steps" in installation_steps:
		for step in installation_steps['init-steps']:
			dockerfile_content.append(f"""RUN {step}\n""")
			# dockerfile_content.append(step)
	
	return dockerfile_content

def install_language_steps(installation_steps, dockerfile_content):
	for step in installation_steps:
		dockerfile_content.append(f"""RUN {step}\n""")
		# dockerfile_content.append(step)

	return dockerfile_content

def install_libraries_steps(installation_steps, libraries_list, dockerfile_content):
	for library in libraries_list:
		if library in installation_steps:
			for library_install_step in installation_steps[library]:
				dockerfile_content.append(f"""RUN {library_install_step}\n""")
				# dockerfile_content.append(library_install_step)

	return dockerfile_content

def install_language_and_library(languages, installation_steps):
	dockerfile_content = []
	for language in languages:
		lang_name = language['language-name']
		libraries_list = language['libraries']
		dockerfile_content = install_language_steps(installation_steps[lang_name]['installation-steps'], dockerfile_content)
		dockerfile_content = install_libraries_steps(installation_steps[lang_name]['libraries'], libraries_list, dockerfile_content)

	return dockerfile_content

def extract_resource_requirements(resources):
	dockerfile_content = []
	if resources is not None:
		ram = resources['ram']
		cpu = resources['cpu']
		gpu = resources['gpu']

	# if ram is not None:
	# 	dockerfile_content.append(f"""--memory="{ram}" """)
	# if cpu is not None:
	# 	dockerfile_content.append(f"""--cpus="{cpu}" """)
	# if gpu is not None:
	# 	dockerfile_content.append(f"""--gpus all="{gpu}" """)

	# return dockerfile_content

	return ram, cpu, gpu

def extract_port_mapping(port_mappings):
	port_mappings_list = []
	for mapping in port_mappings:
		internal_port_obj = mapping['internal']
		internal_port_mapping = internal_port_obj['ports']
		if 'protocol' in internal_port_obj and len(internal_port_obj['protocol']) > 0:
			internal_port_mapping += "/" + internal_port_obj['protocol']
		
		external_port_obj = mapping['external']
		external_port_mapping = external_port_obj['ports']
		if 'protocol' in external_port_obj and len(external_port_obj['protocol']) > 0:
			external_port_mapping += "/" + external_port_obj['protocol']

		# port_mappings_list.append("-p " + external_port_mapping + ":" + internal_port_mapping)
		port_mappings_list.append(f"""{external_port_mapping}:{internal_port_mapping}""")
	return port_mappings_list


def write_to_dockerfile(file_desc, installation_steps):
	for step in installation_steps:
		file_desc.write(step)

# file_desc = open('dfs_contract.json')
# data = json.load(file_desc)
# file_desc.close()

def extract_temp_filesystem(storage_req):
	req_list = []
	for req in storage_req:
		req_list.append(req)
	return req_list

def init_env_setup_steps(installation_steps, data):
	env_name = None
	if 'env-name' in data:
		env_name = data['env-name']

	version = None
	if 'version' in data:
		version = data['version']

	os = None
	if 'os' in data:
		os = data['os']
		

	languages = None
	if 'languages' in data:
		languages = data['languages']

	resources = None
	if 'resources' in data:
		resources = data['resources']

	datasets = None
	if 'dataset' in data:
		dataset = data['dataset']

	port_mappings = None
	if 'port-publish' in data:
		port_mappings = data['port-publish']
	
	storage_req = None
	if 'storage' in data:
		storage_req = data['storage']

	docker_file_desc = open("Dockerfile",'w')

	os_dockerfile_content = install_os(os, installation_steps)
	languages_dockerfile_content = install_language_and_library(languages, installation_steps["specifications"])
	# resources_dockerfile_content = extract_resource_requirements(resources)
	ram, cpu, gpu = extract_resource_requirements(resources)
	port_mapping_content = extract_port_mapping(port_mappings)
	temp_filesystem = extract_temp_filesystem(storage_req)

	write_to_dockerfile(docker_file_desc, os_dockerfile_content)
	write_to_dockerfile(docker_file_desc, languages_dockerfile_content)
	write_to_dockerfile(docker_file_desc, ["USER root"])
	docker_file_desc.close()

	create_compose_file(env_name + "_"+ data['_id'], ram, cpu, gpu, port_mapping_content, temp_filesystem)

	# with open("output.log", "w") as output:
	# 	subprocess.call("sudo docker compose --compatibility up -d", shell=True, stdout=output, stderr=output)

	# docker = DockerClient(compose_files=["./compose.yaml"])
	# docker.compose.build()
	# docker.compose.up()
	proc = subprocess.Popen(['docker','compose','--compatibility','up','-d'], stdout=subprocess.PIPE)
	output = proc.stdout.read().decode()
	print(output)
	print(type(output))
	print("Done")
	message_list = output.split('\n')
	print(message_list)

	if message_list[-2].find("DONE") != -1:
		print("Success")
	else:
		print("Failiure")

# docker_run_command_list = ["docker run -d"]
# docker_run_command_list.extend(port_mapping_content)
# docker_run_command_list.extend(resources_dockerfile_content)
# docker_run_command_list.append("demo-svm")

# docker_run_command = ' '.join(docker_run_command_list)

# with open("output.log", "w") as output:
# 	subprocess.call("docker build . -t demo_svm", shell=True, stdout=output, stderr=output)
# 	subprocess.call(docker_run_command, shell=True, stdout=output, stderr=output)


# os_dockerfile_content = install_os(os, installation_steps)
# languages_dockerfile_content = install_language_and_library(languages, installation_steps)
# ram, gpu, cpu = extract_resource_requirements(resources)
# base_image = os['image-name'] + ":" + os['tags']
# docker_run_command = []
# docker_run_command.extend(os_dockerfile_content)
# docker_run_command.extend(languages_dockerfile_content)

# base_image_obj = docker.pull(base_image)
# docker.container.run(image=base_image_obj, command=docker_run_command, cpus=cpu, detach=True, memory=ram, gpus=gpu)