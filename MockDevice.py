#!/bin/python3

from argparse import ArgumentParser
import shutil
import sys
import os


def generate_resources(manufacture: str, brand: str, model: str) -> None:
    res_dir = os.path.join("/tmp", "-".join((manufacture, brand, model)))
    if not os.path.exists(res_dir):
        os.makedirs(res_dir)

    with open(os.path.join(res_dir, "system.prop"), "w+") as f:
        f.write(f"ro.product.manufacturer={manufacture}\n")
        f.write(f"ro.product.brand={brand}\n")
        f.write(f"ro.product.model={model}\n")
        f.flush()

    with open(os.path.join(res_dir, "module.prop"), "w+") as f:
        f.write(f"id=MockDevice{model}\n")
        f.write(f"name=MockDevice{model}\n")
        f.write(f"version=1.0\n")
        f.write(f"versionCode=1\n")
        f.write(f"author={os.getlogin()}\n")
        f.write(f"description=Mock device to {manufacture}-{model}\n")
        f.flush()

    script_dir = os.path.join(res_dir, "META-INF", "com", "google", "android")
    if not os.path.exists(script_dir):
        os.makedirs(script_dir)
    src_file = os.path.join(os.path.dirname(__file__), "module_installer.sh")
    if not os.path.exists(src_file):
        print(f"{src_file} not exists!")
        exit(-1)
    shutil.copyfile(src_file, os.path.join(script_dir, "update-binary"))

    with open(os.path.join(script_dir, "updater-script"), "w+") as f:
        f.write("#MAGISK\n")
        f.flush()

    zip_file = os.path.join("/tmp", f"mock-{manufacture}-{model}")
    zip_res = shutil.make_archive(
        base_name=zip_file,
        format="zip",
        root_dir=res_dir,
        verbose=True
    )

    dest = shutil.move(zip_res, os.path.dirname(__file__))
    print(dest)


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument(
        "-m", "--manufacture",
        type=str,
        required=True,
        help="Product manufacture"
    )
    arg_parser.add_argument(
        "-b", "--brand",
        type=str,
        required=True,
        help="Product brand"
    )
    arg_parser.add_argument(
        "-md", "--model",
        type=str,
        required=True,
        help="Product model"
    )
    arg_parser.add_argument(
        "-l", "--list-products",
        action="store_true",
        help="List all products"
    )

    configs = arg_parser.parse_args()

    if configs.list_products:
        print("https://github.com/KHwang9883/MobileModels")
        sys.exit(0)

    generate_resources(configs.manufacture, configs.brand, configs.model)
