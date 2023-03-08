import io
import re
import sys

from setuptools import setup

with io.open('ctpbee/__init__.py', 'rt', encoding='utf8') as f:
    context = f.read()
    version = re.search(r'__version__ = \'(.*?)\'', context).group(1)

if sys.version_info < (3, 6):
    raise RuntimeError('当前ctpbee只支持python36以及更高版本/ ctpbee only support python36 and higher ')

# libraries
install_requires = ["pytz", "blinker", "requests", "simplejson", "lxml", "jinja2", "redis",
                    'cologer>=2.0', "ctpbee_api>=0.40", "numpy", "pandas"]

if sys.version_info.major == 3 and sys.version_info.minor == 6:
    install_requires.append("dataclasses")

runtime_library_dir = []
try:
    import pypandoc

    long_description = pypandoc.convert_file('README.md', 'rst')
except Exception:
    long_description = ""

pkgs = ['ctpbee', 'ctpbee.context', 'ctpbee.exceptions', 'ctpbee.data_handle', 'ctpbee.interface',
        'ctpbee.interface.ctp', "ctpbee.interface.looper", "ctpbee.interface.ctp_mini", 'ctpbee.jsond', "ctpbee.looper",
        "ctpbee.indicator"]

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
    package_data={'ctpbee': ['api/ctp/*', "*.html"]},
    ext_modules=[],
    entry_points={
        'console_scripts': ['ctpbee = ctpbee.cmdline:execute']
    }
)
