from yaml import safe_load
import yaml
from netmiko import Netmiko
from jinja2 import Environment, FileSystemLoader
import socket


def main():
    with open('host_list.yml',"r") as handle:
        hosts = yaml.full_load(handle)

    platform_map = {'ios':'cisco_ios'}

    for host in hosts["host_list"]:
        platform = platform_map[host["platform"]]
        with open(f"vars/{host['name']}_ios.yml","r") as handle:
            interface_config = yaml.full_load(handle)
        j2_env = Environment(
                loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
            )

        template = j2_env.get_template('templates/switches.j2')
        switches_config = template.render(data=interface_config)
        device = socket.gethostbyname(host["name"])
        conn = Netmiko(host=device,device_type=platform,username="uname",password="pass")
        print(f"Logged into {conn.find_prompt()} successfully")
        for i in switches_config.split('\n'):
            result = conn.send_command(i)
            print (result)
        conn.disconnect()

if __name__ == "__main__":
    main()
