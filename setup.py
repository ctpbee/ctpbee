from distutils.core import setup
from setuptools import find_packages

import ast
import platform
import re
from setuptools import Extension, find_packages, setup

with open("ctpbee/__init__.py", "rb") as f:
    version_line = re.search(
        r"__version__\s+=\s+(.*)", f.read().decode("utf-8")
    ).group(1)
    version = str(ast.literal_eval(version_line))

if platform.uname().system == "Windows":
    compiler_flags = [
        "/MP", "/std:c++17",  # standard
        "/O2", "/Ob2", "/Oi", "/Ot", "/Oy", "/GL",  # Optimization
        "/wd4819"  # 936 code page
    ]
    extra_link_args = []
else:
    compiler_flags = [
        "-std=c++17",  # standard
        "-O3",  # Optimization
        "-Wno-delete-incomplete", "-Wno-sign-compare",
    ]
    extra_link_args = ["-lstdc++"]

vnctpmd = Extension(
    "ctpbee.api.ctp.vnctpmd",
    [
        "ctpbee/api/ctp/vnctp/vnctpmd/vnctpmd.cpp",
    ],
    include_dirs=["ctpbee/api/ctp/include",
                  "ctpbee/api/ctp/vnctp", ],
    define_macros=[],
    undef_macros=[],
    library_dirs=["ctpbee/api/ctp/libs", "ctpbee/api/ctp"],
    libraries=["thostmduserapi_se", "thosttraderapi_se", ],
    extra_compile_args=compiler_flags,
    extra_link_args=extra_link_args,
    depends=[],
    runtime_library_dirs=["$ORIGIN"],
    language="cpp",
)
vnctptd = Extension(
    "ctpbee.api.ctp.vnctptd",
    [
        "ctpbee/api/ctp/vnctp/vnctptd/vnctptd.cpp",
    ],
    include_dirs=["ctpbee/api/ctp/include",
                  "ctpbee/api/ctp/vnctp", ],
    define_macros=[],
    undef_macros=[],
    library_dirs=["ctpbee/api/ctp/libs", "ctpbee/api/ctp"],
    libraries=["thostmduserapi_se", "thosttraderapi_se", ],
    extra_compile_args=compiler_flags,
    extra_link_args=extra_link_args,
    runtime_library_dirs=["$ORIGIN"],
    depends=[],
    language="cpp",
)

if platform.system() == "Windows":
    # use pre-built pyd for windows ( support python 3.7 only )
    ext_modules = []
elif platform.system() == "Darwin":
    ext_modules = []
else:
    ext_modules = [vnctptd, vnctpmd]


def is_psycopg2_exists():
    try:
        import psycopg2  # noqa
        return True
    except ImportError:
        return False


pkgs = find_packages()
install_requires = ['flask']
setup(name='ctpbee',
      version='0.12',
      author='somewheve',
      author_email='somewheve@gmail.com',
      description="easy ctp trade and market support",
      url='https://github.com/somewheve/ctpbee',
      license="MIT",
      packages=pkgs,
      install_requires=install_requires,
      package_data={"": [
          "*.ini",
          "*.dll",
          "*.so",
          "*.pyd",
      ]},
      ext_modules=ext_modules
      )
