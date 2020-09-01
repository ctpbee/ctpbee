import io
import re

import copy
import distutils.cmd
import distutils.log
import subprocess
import sys
from urllib.parse import urlparse
from setuptools import setup
from pkg_resources import parse_version
from setuptools.command.install import install


class Autofix(install):
    """
    此文件用来描述修复安装QA_SUPPORT可能出现的冲突问题
    第一个冲突，pytdx --> tushare 与 quantaxiss使用两个不同的版本的pytdx
    第二个冲突，pandas--> tushare 使用的pandas被限制了版本

    pip 调用示例:
        linux：
            pip install -r <(echo 'ctpbee[QA_SUPPORT] --install-option="--fix=true" --install-option="--uri=https://mirrors.aliyun.com/pypi/simple"') -i https://mirrors.aliyun.com/pypi/simple -v
        windows:
            >>>
    """

    description = 'fix install '
    user_options = install.user_options + [
        ('fix=', None, 'whether to install fix'),
        ("uri=", None, "trusted host to install package")
    ]
    version_need = [
        ("pytdx", ">=1.72"),
        ("pandas", "<=0.24"),
    ]
    command_base = [sys.executable, "-m"]

    def initialize_options(self):
        install.initialize_options(self)
        self.fix = "false"
        self.uri = None

    def check_version(self, name, express) -> bool:
        """ 检查版本问题"""
        output = subprocess.check_output([sys.executable, "-m", "pip", "freeze"]).decode('utf-8')
        version_info = {}
        for _ in map(lambda x: {x.split("==")[0]: x.split("==")[1]} if x != "" else {}, output.split("\n")):
            version_info.update(_)
        if name not in version_info.keys():
            return False
        else:
            v = version_info.get(name)
            return self.get_cmp_signal(v, express)

    @staticmethod
    def get_cmp_signal(version, signal):
        # 根据,获取一个/两个表达式
        expressions = signal.split(",")

        def cmpd(v, ex):
            p = re.findall(r"\d+\.?\d*", ex)
            assert len(p) == 1
            end = ex.replace(p[0], "")
            express = f"parse_version('{str(v)}'){end}parse_version('{str(p[0])}')"
            return eval(express)

        for _ in expressions:
            if not cmpd(version, _):
                """一旦出现不合法的表达式, 那么立即返回False"""
                return False
        return True

    def reinstall(self, name, required):

        command_un = copy.deepcopy(self.command_base) + ['pip', "uninstall", f"{name}", "-y"]
        command_in = copy.deepcopy(self.command_base) + ['pip', "install", f"{name}{required}"]
        if self.fix == "true":
            if self.uri:
                command_in += ["-i", self.uri, "--trusted-host", self.get_domian(self.uri)]
        else:
            return
        self.announce(
            'Running uninstall command: %s' % " ".join(command_un),
            level=distutils.log.WARN)
        subprocess.check_call(command_un)
        self.announce(
            'Running reinstall pytdx: %s' % " ".join(command_in),
            level=distutils.log.WARN)
        subprocess.check_call(command_in)
        self.output(f"\n{name} version fix successfully, hope you can enjoy it", sig="-")

    def fix_install(self):
        if self.fix == "false":
            return
        for _ in self.version_need:
            name, version = _
            r = self.check_version(name, version)
            self.output(f"package: {name}, check result: {str(r)}", sig="-")
            if not r:
                self.reinstall(name, version)

        self.output("All package fixed finished, have a good luck! ")

    def output(self, msg, number=100, sig="*", level=distutils.log.INFO):
        self.announce(
            f"{sig * number}\n                        {msg}\n{sig * number}",
            level=level)

    def finalize_options(self):
        install.finalize_options(self)
        assert type(self.uri) == str or self.uri is None
        assert self.fix in ['false', "true"]

    @staticmethod
    def get_domian(uri) -> str:
        """
        返回解析的的域名信息
        """
        parse = urlparse(uri)
        return parse.netloc

    def run(self):
        """
        Run
        command.
        """

        install.run(self)
        self.fix_install()


with io.open('ctpbee/__init__.py', 'rt', encoding='utf8') as f:
    context = f.read()
    version = re.search(r'__version__ = \'(.*?)\'', context).group(1)

if sys.version_info < (3, 6):
    raise RuntimeError('当前ctpbee只支持python36以及更高版本/ ctpbee only support python36 and highly only ')

# libraries
install_requires = ['flask>=1.1.1', "blinker", "requests", "simplejson", "lxml",
                    'colour_printing>=0.3.16', "ctpbee_api", 'qaenv', "pymongo"]

if sys.version_info.major == 3 and sys.version_info.minor == 6:
    install_requires.append("dataclasses")

runtime_library_dir = []
try:
    import pypandoc

    long_description = pypandoc.convert_file('README.md', 'rst')
except Exception:
    long_description = ""

pkgs = ['ctpbee', 'ctpbee.context', 'ctpbee.exceptions', 'ctpbee.data_handle', 'ctpbee.interface',
        'ctpbee.interface.ctp', "ctpbee.interface.looper", 'ctpbee.jsond', "ctpbee.looper", "ctpbee.indicator",
        "ctpbee.qa_support"]

setup(
    name='ctpbee',
    version=version,
    description="Easy ctp trade and market support",
    author='somewheve',
    long_description=long_description,
    author_email='somewheve@gmail.com',
    url='https://github.com/ctpbee/ctpbee',
    license="MIT",
    packages=pkgs,
    install_requires=install_requires,
    platforms=["Windows", "Linux", "Mac OS-X"],
    package_dir={'ctpbee': 'ctpbee'},
    zip_safe=False,
    include_package_data=True,
    data_files=[],
    package_data={'ctpbee': ['api/ctp/*', 'holiday.json', "*.html"]},
    ext_modules=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    cmdclass={
        "install": Autofix
    },
    entry_points={
        'console_scripts': ['ctpbee = ctpbee.cmdline:execute']
    },
    extras_require={
        'QA_SUPPORT': ["quantaxis", "qifiaccount", "pandas<=0.24.2,>=0.16.2"],
    }
)
