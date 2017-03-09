import setuptools

packages = setuptools.find_packages()
package_name = packages[0]
project_name = package_name.replace('_', '-')
setuptools.setup(
    name=project_name,
    version='1.2',
    license='MIT',
    author='thewizardplusplus',
    author_email='thewizardplusplus@yandex.ru',
    url='https://github.com/thewizardplusplus/'+project_name,
    packages=packages,
    install_requires=['Pillow'],
    entry_points={
        'console_scripts': [
            '{:s} = {:s}:main'.format(project_name, package_name),
        ],
    },
)
