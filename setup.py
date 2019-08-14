import platform
import warnings

from setuptools import Extension, setup

runtime_library_dir = []

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
        "-Wno-delete-incomplete", "-Wno-sign-compare", "-pthread"
    ]
    extra_link_args = ["-lstdc++"]
    runtime_library_dir = ["$ORIGIN"]

vnctpmd = Extension(
    "ctpbee.api.ctp.vnctpmd",
    [
        "ctpbee/api/ctp/vnctp/vnctpmd/vnctpmd.cpp",
    ],
    include_dirs=[
        "ctpbee/api/ctp/include",
        "ctpbee/api/ctp/vnctp",
    ],
    language="cpp",
    define_macros=[],
    undef_macros=[],
    library_dirs=["ctpbee/api/ctp/libs", "ctpbee/api/ctp"],
    libraries=["thostmduserapi_se", "thosttraderapi_se", ],
    extra_compile_args=compiler_flags,
    extra_link_args=extra_link_args,
    depends=[],
    runtime_library_dirs=runtime_library_dir,
)
vnctptd = Extension(
    "ctpbee.api.ctp.vnctptd",
    [
        "ctpbee/api/ctp/vnctp/vnctptd/vnctptd.cpp",
    ],
    include_dirs=[
        "ctpbee/api/ctp/include",
        "ctpbee/api/ctp/vnctp",
    ],
    define_macros=[],
    undef_macros=[],
    library_dirs=["ctpbee/api/ctp/libs",
                  "ctpbee/api/ctp",
                  ],
    libraries=["thostmduserapi_se", "thosttraderapi_se"],
    extra_compile_args=compiler_flags,
    extra_link_args=extra_link_args,
    runtime_library_dirs=runtime_library_dir,
    depends=[],
    language="cpp",
)

vnctpmd_se = Extension(
    "ctpbee.api.ctp.vnctpmd_se",
    [
        "ctpbee/api/ctp/vnctp_se/vnctpmd/vnctpmd.cpp",
    ],
    include_dirs=[
        "ctpbee/api/ctp/include",
        "ctpbee/api/ctp/vnctp_se",
    ],
    language="cpp",
    define_macros=[],
    undef_macros=[],
    library_dirs=["ctpbee/api/ctp/libs", "ctpbee/api/ctp"],
    libraries=["thosttraderapi_se_app", "thostmduserapi_se_app", ],
    extra_compile_args=compiler_flags,
    extra_link_args=extra_link_args,
    depends=[],
    runtime_library_dirs=runtime_library_dir,
)

vnctptd_se = Extension(
    "ctpbee.api.ctp.vnctptd_se",
    [
        "ctpbee/api/ctp/vnctp_se/vnctptd/vnctptd.cpp",
    ],
    include_dirs=[
        "ctpbee/api/ctp/include",
        "ctpbee/api/ctp/vnctp_se",
    ],
    define_macros=[],
    undef_macros=[],
    library_dirs=["ctpbee/api/ctp/libs",
                  "ctpbee/api/ctp",
                  ],
    libraries=["thosttraderapi_se_app", "thostmduserapi_se_app"],
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
    warnings.warn("因为官方并没有发布基于mac的api， 所以当前ctpbee并不支持mac下面的ctp接口")
    ext_modules = []
else:
    ext_modules = [vnctptd, vnctpmd, vnctptd_se, vnctpmd_se]

pkgs = ['ctpbee', 'ctpbee.api', 'ctpbee.context', 'ctpbee.exceptions', 'ctpbee.data_handle', 'ctpbee.interface',
        'ctpbee.event_engine', 'ctpbee.interface.ctp', 'ctpbee.json']
install_requires = ['flask>=1.1.1', "blinker", "dataclasses"]
setup(
    name='ctpbee',
    version='0.25',
    description="Easy ctp trade and market support",
    author='somewheve',
    author_email='somewheve@gmail.com',
    url='https://github.com/somewheve/ctpbee',
    license="MIT",
    packages=pkgs,
    install_requires=install_requires,
    platforms=["Windows", "Linux", "Mac OS-X"],
    package_dir={'ctpbee': 'ctpbee'},
    package_data={'ctpbee': ['api/ctp/*', ]},
    ext_modules=ext_modules,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ]
)
