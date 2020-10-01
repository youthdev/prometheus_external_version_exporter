from prometheus_client import start_http_server, Gauge
import yaml
import urllib.request
import re
import os
import time

# Create a metric to track versions.
VERSION = Gauge('external_service_version', 'Current version of an external service', ['name', 'version'])

if __name__ == '__main__':
    exponential_factor = os.getenv('EXPONENTIAL_FACTOR', 100000)
    scrap_delay = os.getenv('SCRAP_DELAY_SECONDS', 3600)
    # Start up the server to expose the metrics.
    start_http_server(8000)
    # Generate some requests.
    while True:
        with open("config.yaml", 'r') as stream:
            try:
                config = yaml.safe_load(stream)

                for service_name, service in config['services'].items():
                    content = str(urllib.request.urlopen(service['url']).read())
                    tmp = re.search(service['regex'], content)
                    version = '0.0.0'
                    if tmp:
                        if len(tmp.groups()) > 0:
                            version = tmp.group(1)
                        else:
                            version = tmp.group(0)

                    version_value = 0
                    for idx, part in enumerate(reversed(version.split('.'))):
                        version_value += int(part) % exponential_factor * pow(exponential_factor, idx)

                    # print(
                    #     'Scraped %s with version %s and version value is %.2f' % (service_name, version, version_value))
                    VERSION.labels(service_name, version).set(version_value)
            except yaml.YAMLError as exc:
                print("Error, can not parse config.yml file: %s" % exc)

            time.sleep(scrap_delay)
