import pytest
from config_loader import ConfigLoader
import os
from yaml import safe_load as yaml_load, safe_dump as yaml_dump
from toml import load as toml_load, dump as toml_dump
from configparser import ConfigParser
from json import load as json_load, dump as json_dump

class TestConfigLoader:

    def test_load_configuration_yaml_invalid(self):
        with pytest.raises(Exception):
            ConfigLoader("demo.txt")

    def test_load_configuration_no_env_yaml(self):
        data = ConfigLoader("./tests/data/sample.yaml").get_config()
        assert data['system'] == 'testing'
        assert data['testing']['demo'] == 'default'
        assert data['plain'] == "value"
        assert data['boolean']
        assert data['integer'] == 1
        assert data['float'] == 1.0
        assert data['env_val'] is None

    def test_load_configuration_env_yaml(self):
        os.environ['SYSTEM'] = "env_value"
        os.environ['ENVIRONMENT_VARIABLE'] = "value"
        os.environ['INT_VALUE'] = "2"
        os.environ['FLOAT_VALUE'] = "2.0"
        os.environ['BOOLEAN_VALUE'] = "False"
        os.environ['ENV_VAL'] = "Value"
        data = ConfigLoader("./tests/data/sample.yaml").get_config()
        assert data['system'] == 'env_value'
        assert data['testing']['demo'] == 'value'
        assert data['plain'] == "value"
        assert not data['boolean']
        assert data['integer'] == 2
        assert data['float'] == 2.0
        assert data['env_val'] == "Value"
        del os.environ['SYSTEM']
        del os.environ['ENVIRONMENT_VARIABLE']
        del os.environ['INT_VALUE']
        del os.environ['BOOLEAN_VALUE']
        del os.environ['FLOAT_VALUE']
        del os.environ['ENV_VAL']

    def test_load_configuration_invalid_value_yaml(self):
        old_data = yaml_load(open('./tests/data/sample.yaml'))
        sample = {'system': "${SYSTEM:testing"}
        yaml_dump(sample, open('./tests/data/sample.yaml', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.yaml")
        yaml_dump(old_data, open('./tests/data/sample.yaml', mode='w+'))
        data = ConfigLoader("./tests/data/sample.yaml").get_config()
        assert data['system'] == 'testing'
        assert data['testing']['demo'] == 'default'
        assert data['plain'] == "value"
        assert data['boolean']
        assert data['integer'] == 1
        assert data['float'] == 1.0
        sample = {'system': "SYSTEM:testing}"}
        yaml_dump(sample, open('./tests/data/sample.yaml', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.yaml")
        sample = {'system': "${SYSTEM:testing:testing2}"}
        yaml_dump(sample, open('./tests/data/sample.yaml', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.yaml")
        yaml_dump(old_data, open('./tests/data/sample.yaml', mode='w+'))

    def test_load_configuration_no_env_toml(self):
        data = ConfigLoader("./tests/data/sample.toml").get_config()
        assert data['system'] == 'testing'
        assert data['testing']['demo'] == 'default'
        assert data['plain'] == "value"
        assert data['boolean']
        assert data['integer'] == 1
        assert data['float'] == 1.0

    def test_load_configuration_env_toml(self):
        os.environ['SYSTEM'] = "env_value"
        os.environ['ENVIRONMENT_VARIABLE'] = "value"
        os.environ['INT_VALUE'] = "2"
        os.environ['FLOAT_VALUE'] = "2.0"
        os.environ['BOOLEAN_VALUE'] = "False"
        data = ConfigLoader("./tests/data/sample.toml").get_config()
        assert data['system'] == 'env_value'
        assert data['testing']['demo'] == 'value'
        assert data['plain'] == "value"
        assert not data['boolean']
        assert data['integer'] == 2
        assert data['float'] == 2.0
        del os.environ['SYSTEM']
        del os.environ['ENVIRONMENT_VARIABLE']
        del os.environ['INT_VALUE']
        del os.environ['BOOLEAN_VALUE']
        del os.environ['FLOAT_VALUE']

    def test_load_configuration_invalid_value_toml(self):
        old_data = toml_load(open('./tests/data/sample.toml'))
        sample = {'system': "${SYSTEM:testing"}
        toml_dump(sample, open('./tests/data/sample.toml', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.toml")
        toml_dump(old_data, open('./tests/data/sample.toml', mode='w+'))
        data = ConfigLoader("./tests/data/sample.toml").get_config()
        assert data['system'] == 'testing'
        assert data['testing']['demo'] == 'default'
        assert data['plain'] == "value"
        assert data['integer'] == 1
        assert data['float'] == 1.0
        sample = {'system': "SYSTEM:testing}"}
        toml_dump(sample, open('./tests/data/sample.toml', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.toml")
        toml_dump(old_data, open('./tests/data/sample.toml', mode='w+'))

    def test_load_configuration_no_env_ini(self):
        data = ConfigLoader("./tests/data/sample.ini").get_config()
        assert data['default']['system'] == 'testing'
        assert data['testing']['demo'] == 'default'
        assert data['default']['plain'] == "value"
        assert data['default']['boolean']
        assert data['default']['integer'] == 1
        assert data['default']['float'] == 1.0

    def test_load_configuration_env_ini(self):
        os.environ['SYSTEM'] = "env_value"
        os.environ['ENVIRONMENT_VARIABLE'] = "value"
        os.environ['INT_VALUE'] = "2"
        os.environ['BOOLEAN_VALUE'] = "False"
        os.environ['FLOAT_VALUE'] = "2.0"
        data = ConfigLoader("./tests/data/sample.ini").get_config()
        assert data['default']['system'] == 'env_value'
        assert data['testing']['demo'] == 'value'
        assert data['default']['plain'] == "value"
        assert not data['default']['boolean']
        assert data['default']['integer'] == 2
        assert data['default']['float'] == 2.0
        del os.environ['SYSTEM']
        del os.environ['ENVIRONMENT_VARIABLE']
        del os.environ['INT_VALUE']
        del os.environ['BOOLEAN_VALUE']
        del os.environ['FLOAT_VALUE']

    def test_load_configuration_invalid_value_ini(self):
        config_parser = ConfigParser()
        config_parser.read_file((open('./tests/data/sample.ini')))
        config_parser.set('default', 'system', '${SYSTEM:testing')
        config_parser.write(open('./tests/data/sample.ini', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.ini")
        config_parser.set('default', 'system', '${SYSTEM:testing}')
        config_parser.write(open('./tests/data/sample.ini', mode='w+'))
        data = ConfigLoader("./tests/data/sample.ini").get_config()
        assert data['default']['system'] == 'testing'
        assert data['testing']['demo'] == 'default'
        assert data['default']['plain'] == "value"
        assert data['default']['integer'] == 1
        assert data['default']['float'] == 1.0
        config_parser.set('default', 'system', 'SYSTEM:testing}')
        config_parser.write(open('./tests/data/sample.ini', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.ini")
        config_parser.set('default', 'system', '${SYSTEM:testing}')
        config_parser.write(open('./tests/data/sample.ini', mode='w+'))

    def test_load_configuration_no_env_cfg(self):
        data = ConfigLoader("./tests/data/sample.cfg").get_config()
        assert data['default']['system'] == 'testing'
        assert data['testing']['demo'] == 'default'
        assert data['default']['plain'] == "value"
        assert data['default']['boolean']
        assert data['default']['integer'] == 1
        assert data['default']['float'] == 1.0

    def test_load_configuration_env_cfg(self):
        os.environ['SYSTEM'] = "env_value"
        os.environ['ENVIRONMENT_VARIABLE'] = "value"
        os.environ['INT_VALUE'] = "2"
        os.environ['BOOLEAN_VALUE'] = "False"
        os.environ['FLOAT_VALUE'] = "2.0"
        data = ConfigLoader("./tests/data/sample.cfg").get_config()
        assert data['default']['system'] == 'env_value'
        assert data['testing']['demo'] == 'value'
        assert data['default']['plain'] == "value"
        assert not data['default']['boolean']
        assert data['default']['integer'] == 2
        assert data['default']['float'] == 2.0
        del os.environ['SYSTEM']
        del os.environ['ENVIRONMENT_VARIABLE']
        del os.environ['INT_VALUE']
        del os.environ['BOOLEAN_VALUE']
        del os.environ['FLOAT_VALUE']

    def test_load_configuration_invalid_value_cfg(self):
        config_parser = ConfigParser()
        config_parser.read_file((open('./tests/data/sample.cfg')))
        config_parser.set('default', 'system', '${SYSTEM:testing')
        config_parser.write(open('./tests/data/sample.cfg', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.cfg")
        config_parser.set('default', 'system', '${SYSTEM:testing}')
        config_parser.write(open('./tests/data/sample.cfg', mode='w+'))
        data = ConfigLoader("./tests/data/sample.cfg").get_config()
        assert data['default']['system'] == 'testing'
        assert data['testing']['demo'] == 'default'
        assert data['default']['plain'] == "value"
        assert data['default']['integer'] == 1
        assert data['default']['float'] == 1.0
        config_parser.set('default', 'system', 'SYSTEM:testing}')
        config_parser.write(open('./tests/data/sample.cfg', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.cfg")
        config_parser.set('default', 'system', '${SYSTEM:testing}')
        config_parser.write(open('./tests/data/sample.cfg', mode='w+'))


    def test_load_configuration_no_env_json(self):
        data = ConfigLoader("./tests/data/sample.json").get_config()
        assert data['system'] == 'testing'
        assert data['testing']['demo'] == 'default'
        assert data['plain'] == "value"
        assert data['boolean']
        assert data['integer'] == 1
        assert data['float'] == 1.0
        assert data['env_val'] is None

    def test_load_configuration_env_json(self):
        os.environ['SYSTEM'] = "env_value"
        os.environ['ENVIRONMENT_VARIABLE'] = "value"
        os.environ['INT_VALUE'] = "2"
        os.environ['FLOAT_VALUE'] = "2.0"
        os.environ['BOOLEAN_VALUE'] = "False"
        os.environ['ENV_VAL'] = "Value"
        data = ConfigLoader("./tests/data/sample.json").get_config()
        assert data['system'] == 'env_value'
        assert data['testing']['demo'] == 'value'
        assert data['plain'] == "value"
        assert not data['boolean']
        assert data['integer'] == 2
        assert data['float'] == 2.0
        assert data['env_val'] == "Value"
        del os.environ['SYSTEM']
        del os.environ['ENVIRONMENT_VARIABLE']
        del os.environ['INT_VALUE']
        del os.environ['BOOLEAN_VALUE']
        del os.environ['FLOAT_VALUE']
        del os.environ['ENV_VAL']

    def test_load_configuration_invalid_value_json(self):
        old_data = json_load(open('./tests/data/sample.json'))
        sample = {'system': "${SYSTEM:testing"}
        json_dump(sample, open('./tests/data/sample.json', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.json")
        json_dump(old_data, open('./tests/data/sample.json', mode='w+'))
        data = ConfigLoader("./tests/data/sample.json").get_config()
        assert data['system'] == 'testing'
        assert data['testing']['demo'] == 'default'
        assert data['plain'] == "value"
        assert data['boolean']
        assert data['integer'] == 1
        assert data['float'] == 1.0
        sample = {'system': "SYSTEM:testing}"}
        json_dump(sample, open('./tests/data/sample.json', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.json")
        sample = {'system': "${SYSTEM:testing:testing2}"}
        json_dump(sample, open('./tests/data/sample.json', mode='w+'))
        with pytest.raises(Exception):
            ConfigLoader("./tests/data/sample.json")
        json_dump(old_data, open('./tests/data/sample.json', mode='w+'))