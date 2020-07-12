import yaml

class GetInfo:

    @classmethod
    def configDataGet(cls):
        try:
            f = open(r"C:\Users\EZFARM\PycharmProjects\Saramin\config\information.yml", "r", encoding="utf-8")
        except FileNotFoundError as err:
            print(err)
            return
        else:

            infoYaml = f.readline()
            yaml.safe_load(infoYaml)
            return infoYaml