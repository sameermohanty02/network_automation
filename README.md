# network_automation
Making production grade Network Automation by templates using jinja and yaml.

## Directories
vars:
contains the standard data structure for network elements to be fed into jinja files to make config templates
I have created datastructure for standard vlans

Templates:
containes config templates for network devices. I have given an example to create vlans.

## host.yml
Inventory file for the network devices

## auto.py
python file to connect to devices using SSH

```
with open('host_list.yml',"r") as handle:
        hosts = yaml.full_load(handle)
```

using yaml.full_load to get host list

```
with open(f"vars/{host['name']}_ios.yml","r") as handle:
            interface_config = yaml.full_load(handle)
```
getting vlan datastructure

```
template = j2_env.get_template('templates/switches.j2')
        switches_config = template.render(data=interface_config)
```

using jinja2 to make config templates

```
device = socket.gethostbyname(host["name"])
        conn = Netmiko(host=device,device_type=platform,username="uname",password="pass")
        print(f"Logged into {conn.find_prompt()} successfully")
        for i in switches_config.split('\n'):
            result = conn.send_command(i)
            print (result)
        conn.disconnect()
```

making a SSH connection to the device and pushing the configs.



