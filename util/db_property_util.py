import configparser

class DBPropertyUtil:
    @staticmethod
    def get_property_string(filename: str) -> str:
        config = configparser.ConfigParser()
        config.read(filename)
        db_config = config['DATABASE']
        return f"mysql+mysqlconnector://{db_config['username']}:{db_config['password']}@{db_config['hostname']}:{db_config['port']}/{db_config['dbname']}"