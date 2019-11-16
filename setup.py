import io
import platform
import re
import sys
from setuptools import setup

with io.open('ctpbee/__init__.py', 'rt', encoding='utf8') as f:
    context = f.read()
    version = re.search(r'__version__ = \'(.*?)\'', context).group(1)

if sys.version_info < (3, 6):
    raise RuntimeError('当前ctpbee只支持python36以及更高版本/ ctpbee only support python36 and highly only ')

# 依赖
install_requires = ['flask>=1.1.1', "blinker", "requests", "simplejson", "lxml", "pandas",
                    'colour_printing>=0.3.16', "ctpbee_api"]

if sys.version_info.major == 3 and sys.version_info.minor == 6:
    install_requires.append("dataclasses")

runtime_library_dir = []
try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except Exception:
    long_description = ""

pkgs = ['ctpbee', 'ctpbee.api', 'ctpbee.context', 'ctpbee.exceptions', 'ctpbee.data_handle', 'ctpbee.interface',
        'ctpbee.event_engine', 'ctpbee.interface.ctp', 'ctpbee.jsond', "ctpbee.looper", "ctpbee.indicator"]

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
    package_data={'ctpbee': ['api/ctp/*', 'holiday.json']},
    ext_modules=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': ['ctpbee = ctpbee.cmdline:execute']
    },
)
