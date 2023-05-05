import yaml

def create_compose_file(env_name, ram, cpu, gpu, port_mapping_content, temp_filesystems):
    compose_file_content = {}
    compose_file_content['version'] = "3.9"

    services_dict = {}
    services_dict[env_name] ={}
    services_dict[env_name]['container_name'] = f"""{env_name}""" 
    services_dict[env_name]['build'] = {}
    services_dict[env_name]['build']['context'] = '.'
    services_dict[env_name]['ports'] = port_mapping_content
    services_dict[env_name]['tty'] = True

    temp_volumes_list = []
    for filesys in temp_filesystems:
        temp_object = {}
        temp_object['type'] = "tmpfs"
        temp_object['target'] = filesys['target']
        temp_object['tmpfs'] = {}
        temp_object['tmpfs']['size'] = filesys['size']
        temp_volumes_list.append(temp_object)

    permanent_obj = {}
    permanent_obj['type'] = "volume"
    permanent_obj['source'] = env_name
    permanent_obj['target'] = '/'+env_name
    temp_volumes_list.append(permanent_obj)
    services_dict[env_name]['volumes'] = temp_volumes_list

    deploy_config_dict = {}
    deploy_config_dict['resources'] = {}
    deploy_config_dict['resources']['limits'] = {}
    deploy_config_dict['resources']['reservations'] = {}
    
    deploy_resource_limits = {}
    if cpu is not None and len(cpu) > 0:
        deploy_resource_limits['cpus'] = cpu
    
    if cpu is not None and len(cpu) > 0:
        deploy_resource_limits['memory'] = ram

    deploy_resource_reservations = {}
    if gpu is not None and len(gpu) > 0:
        deploy_resource_reservations['devices'] = [{'driver': 'nvidia', 'count': int(gpu), "capabilities": ["gpu"]}]

    if len(deploy_resource_reservations.keys()) > 0:
        deploy_config_dict['resources']['reservations'] = deploy_resource_reservations
    
    if len(deploy_resource_limits.keys()) > 0:
        deploy_config_dict['resources']['limits'] = deploy_resource_limits

    if len(deploy_config_dict.keys()) > 0:
        services_dict[env_name]['deploy'] = deploy_config_dict

    compose_file_content['services'] = services_dict
    compose_file_content['volumes'] = {env_name:{}}

    file=open("compose.yaml","w")
    yaml.dump(compose_file_content, file, sort_keys=False,  default_flow_style=False)
    file.close()