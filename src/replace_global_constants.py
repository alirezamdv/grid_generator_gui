from jinja2 import PackageLoader, Environment, FileSystemLoader
import configparser
import os


def replace_global_Constants(proj, out_path, LenLat, LenLon, lon, lat, topo, grad) -> None:
    env_p = str(os.path.dirname(os.path.realpath(__file__))) + "/template/"
    TemplateLoader = FileSystemLoader(env_p)
    env = Environment(loader=TemplateLoader)
    c_template = env.get_template("template.c")
    make_template = env.get_template("Makefile")

    with open(out_path + f"triangle_refine_{proj}_bin.c", "w+") as tri:
        tri.write(c_template.render(LenLat=LenLat, LenLon=LenLon, lon=f'"{lon}"',
                                    lat=f'"{lat}"',
                                    topo=f'"{topo}"',
                                    grad=f'"{grad}"'))
    with open(out_path + "Makefile", "w+") as m:
        m.write(make_template.render(name=proj))


if __name__ == '__main__':
    replace_global_Constants()
