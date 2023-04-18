import yaml
from jinja2 import Template
with open('data.yml') as f:
    entries = yaml.safe_load(f)


for backend in entries['backends']:

    with open('templates/backend.jinja') as file:
        template = Template(file.read())

    output = template.render(backend=backend)

    with open(f'backends/{backend["name"]}.conf', 'w') as outfile:
        outfile.write(output)

with open('templates/vhost.jinja') as file:
    template = Template(file.read())
    for host in entries['hosts']:
        if 'custom_error' in host:
            print(host["name"])

            for index, page in enumerate(host["custom_error"]):
                for file in entries['error-files']:
                    if file['name'] == page:
                        host['custom_error'][index] = file
                        continue

        if 'backend' in host:
            for backend in entries['backends']:
                if backend['name'] == host['backend']:
                    host['backend'] = backend
                    continue
        if 'use' in host:
            if 'www' not in host['use']:
                host['use'].append('is_www')

        with open('templates/vhost.jinja') as file:
            template = Template(file.read())

        output = template.render(host=host)

        with open(f'sites-available/{host["domain"]}.conf', 'w') as outfile:
            outfile.write(output)
        if 'use' in host:
            if 'www' in host['use']:

                host['domain'] = 'www.'+host['domain']
                host['name'] = 'WWW ' + host['name']
                host['use'].append('is_www')
                output = template.render(host=host)
                with open(f'sites-available/{host["domain"]}.conf', 'w') as outfile:
                    outfile.write(output)
