import configparser


def read_ini(file_path):
    dictionnaire = dict()
    config = configparser.ConfigParser()
    config.read(file_path)
    for section in config.sections():
        for key in config[section]:
            dictionnaire[key] = config[section][key]
    return dictionnaire



if __name__ == "__main__":
    print(read_ini("config_mysql.ini"))