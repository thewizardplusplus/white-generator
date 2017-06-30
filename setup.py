import setuptools
import re
import sys
import os.path

if not (0x030400f0 <= sys.hexversion < 0x040000a0):
    raise Exception('requires Python >=3.4, <4.0')

packages = setuptools.find_packages()
package_name = packages[0]
project_name = package_name.replace('_', '-')
with open(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    package_name,
    'consts.py',
)) as consts_file:
    version = re.search(
        "^APP_VERSION = '([^']+)'$",
        consts_file.read(),
        re.MULTILINE,
    ).group(1)
setuptools.setup(
    name=project_name,
    version=version,
    license='MIT',
    author='thewizardplusplus',
    author_email='thewizardplusplus@yandex.ru',
    url='https://github.com/thewizardplusplus/' + project_name,
    packages=packages,
    install_requires=[
        'termcolor >=1.1.0, <2.0',
        'pillow >=4.1.1, <5.0',
    ],
    python_requires='>=3.4, <4.0',
    entry_points={
        'console_scripts': [
            '{:s} = {:s}:main'.format(project_name, package_name),
        ],
    },
)
