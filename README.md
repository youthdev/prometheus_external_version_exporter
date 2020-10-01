# QUICKSTART

```
docker run -v ./config.yaml:/app/config.yaml -p 8000:8000 youthdev/prometheus_external_version_exporter
```

Example config.yaml

```yaml
services:
  shopee:
    url: http://shopee.vn
    regex: '[0-9]+\.[0-9]+\.[0-9]'
  sendo:
    url: http://sendo.vn
    regex: '[0-9]+\.([0-9]+\.[0-9])'
```

The script will try to get the first matched group of regex if possible, if not, it will use the whole matched string.

Example of exposed metrics:

```
external_service_version{name="shopee",version="3.56.6"} 3.0005600006e+010
external_service_version{name="sendo",version="99.8"} 9.900008e+06
```