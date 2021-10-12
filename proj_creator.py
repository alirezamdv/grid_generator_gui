import os
import configparser
import json


class ProjectInitiator:
    def __init__(self, name, proj_names, mode=""):
        self.parser = configparser.ConfigParser()
        # self.read_env()
        # self.dirs = next(os.walk("."))[1]
        self.projects = self.check_projects()
        print(self.projects)
        # if not name and len(self.projects) < 1:
        #     self.name = "untitled"
        #     self.create_project()
        if
        if mode == "new":
            c = len([un for un in self.projects if "untitled" in un.split("_")]) + 1
            print(c)
            self.name = "untitled_" + str(c)
            self.create_project()
        self.save_env()

    def create_project(self):
        os.makedirs("./" + self.name, exist_ok=True)
        with open("./" + self.name + "/config.ini", "w") as f:
            f.write(f"project_name={self.name}")
        self.projects.append(self.name)

    def save_env(self):
        with open("config.ini", "w") as f:
            self.parser.write(f)
            # f.write(f"projects={','.join(self.projects)}")

    def read_config(self, path="."):
        self.parser.read(path + "/config.ini")
        return self.parser

    def check_projects(self):
        projects = []
        PROJECTS = self.read_config()
        PROJECTS = PROJECTS.get("global_configs", "projects").split(",")
        # print(PROJECTS.get("global_configs", "projects").split(","))
        for p in PROJECTS:
            if os.path.exists("./" + p):
                projects.append(p)
        return projects


def project_init(name="untitled"):
    base = "."
    os.makedirs(base + "/" + name, exist_ok=True)


def newest(path):
    files = next(os.walk(path))[1]
    paths = [os.path.join(path, basename) for basename in files]
    PROJECTS.append(max(paths, key=os.path.getctime))
    with open("config.ini", "w") as f:
        f.write(f"projects={','.join(PROJECTS)}")
    print(PROJECTS)
    print(max(paths, key=os.path.getctime))
    print(files, "untitled" in files)


# project_init("rrrdasdsdrrr")
# newest(".")
a = ProjectInitiator(mode="new")
