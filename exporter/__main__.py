from prometheus_client import start_http_server, Gauge, Info
import yaml
import urllib.request
import re
import os
import time

# Create a metric to track versions.
VERSION_VALUE = Gauge('external_service_version_value', 'Current version value of an external service', ['name'])
VERSION_INFO = Info('external_service_version_info', 'Current version info of an external service', ['name'])

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
                        # Try to part the version to int, if not, treat it as zero
                        part_int = 0
                        try:
                            part_int = int(part)
                        except ValueError:
                            print('Can not parse part %d of version of %s because it is not a number, '
                                  'which currently is: %s' % (idx + 1, service_name, version))
                        version_value += part_int % exponential_factor * pow(exponential_factor, idx)

                    # print(
                    #     'Scraped %s with version %s and version value is %.2f' % (service_name, version, version_value))
                    VERSION_VALUE.labels(service_name).set(version_value)
                    VERSION_INFO.labels(service_name).info({'version': version})
            except yaml.YAMLError as exc:
                print("Error, can not parse config.yml file: %s" % exc)

            time.sleep(scrap_delay)
