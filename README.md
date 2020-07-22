# ConfigLoader | ![Build](https://github.com/sfahad1414/conf_loader/workflows/Build/badge.svg) ![Latest Version](https://pypip.in/version/conf_loader/badge.svg) ![Versions](https://img.shields.io/pypi/pyversions/conf_loader.svg) ![License](https://img.shields.io/pypi/l/conf_loader.svg)
Simple configuration file loader

### Why
Modern configuration file is more and more complex, flexible and readable, but **had no option to pass environment variables**. This project aim to simplify usage of the configuration file and environment variables for production and development, with easy dictionary like access

**Supported files**: ini, yaml, json & cfg
### Install
```bash
pip install conf_loader
```

### Basic usage
Let's assume we had a project with this config file `system.yaml`

```yaml
# system.yaml
database:
    host: ${DATABASE_HOST:localhost}
    port: ${DATABASE_PORT:27017}
    username: ${DATABASE_USER:user}
    password: ${DATABASE_PASSWORD:password}
    database: ${DATABASE}
```

and environment variables set to
```
DATABASE_HOST=mongodb://xxx.xxx.xxx.xxx
DATABASE_USER=mongo
DATABASE_PASSWORD=changeit
DATABASE=Demo
```

parse file with `ConfigLoader`

```python
from conf_loader import ConfigLoader

# read file system.yaml and parse config
env = ConfigLoader('system.yaml').get_config()

# access whole database section
print(env['database'])

# {
# 'database': 'test',
# 'host': 'mongodb://xxx.xxx.xxx.xxx',
# 'user': 'mongo'
# 'password': 'changeit',
# 'port': 27017,
# 'database': 'demo'
# }

# access database host value
print(env['database']['host'])

# >> mongodb://xxx.xxx.xxx.xxx

# access database port value returns default value as DEFAULT_PORT is not set in environment
print(env['database']['port'])

# >> 27017
```

### License
MIT licensed. See the [LICENSE](LICENSE) file for more details.
