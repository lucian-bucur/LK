import ConfigParser
import StringIO


class ConfigLoader:
    list_configs = {
        "exim": ["local_domains", "mysql_logging_server", "managed_ips"],
        "caught": ["imap_host"]
    }

    def __init__(self, raw_configs):
        self.raw_configs = raw_configs
        self.parser = ConfigParser.ConfigParser()

    def parse(self):
        config = self.raw_configs.json()['configuration']
        string_buffer = StringIO.StringIO(config)
        self.parser.readfp(string_buffer)
        return self.format()

    def format(self):
        for section in self.parser.sections():
            for option in self.parser.options(section):
                if self.in_list_configs(section, option):
                    value = self.parser.get(section, option)
                    self.parser.set(section, option, value.split(","))

    def in_list_configs(self, section, option):
        if section in self.list_configs:
            if option in self.list_configs[section]:
                return True
        return False
