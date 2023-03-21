import yaml

def create_compose_file(env_name, ram, cpu, gpu, port_mapping_content):
    compose_file_content = {}
    compose_file_content['version'] = "3.9"

    services_dict = {}
    services_dict[env_name] ={}
    services_dict[env_name]['container_name'] = f"""{env_name}""" 
    services_dict[env_name]['build'] = {}
    services_dict[env_name]['build']['context'] = '.'
    services_dict[env_name]['ports'] = port_mapping_content
    services_dict[env_name]['tty'] = True

    deploy_config_dict = {}
    deploy_config_dict['resources'] = {}
    deploy_config_dict['resources']['limits'] = {}
    
    deploy_resource_limits = {}
    if cpu is not None and len(cpu) > 0:
        deploy_resource_limits['cpus'] = cpu
    
    if cpu is not None and len(cpu) > 0:
        deploy_resource_limits['memory'] = ram

    # deploy_resource_reservations = {}
    # if gpu is not None and len(gpu) > 0:
    #     deploy_resource_reservations['devices'] = [{'driver': 'nvidia', 'count': int(gpu), "capabilities": ["gpu"]}]

    # if len(deploy_resource_reservations.keys()) > 0:
    #     deploy_resource_limits['reservation'] = deploy_resource_reservations
    
    if len(deploy_resource_limits.keys()) > 0:
        deploy_config_dict['resources']['limits'] = deploy_resource_limits

    if len(deploy_config_dict.keys()) > 0:
        services_dict[env_name]['deploy'] = deploy_config_dict

    compose_file_content['services'] = services_dict

    file=open("compose.yaml","w")
    yaml.dump(compose_file_content, file, sort_keys=False,  default_flow_style=True)
    file.close()