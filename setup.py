import setuptools
import re

packages = setuptools.find_packages()
package_name = packages[0]
project_name = package_name.replace('_', '-')
with open('white_generator/consts.py') as consts_file:
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
    install_requires=['Pillow'],
    entry_points={
        'console_scripts': [
            '{:s} = {:s}:main'.format(project_name, package_name),
        ],
    },
)
