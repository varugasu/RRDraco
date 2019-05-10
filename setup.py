import setuptools
import re
import os

with open("README.md", "r") as fh:
    long_description = fh.read()


def find_version(*file_paths):
    """
    function taken from ktbyers's netmiko repository
    """
    base_module_file = os.path.join(*file_paths)
    with open(base_module_file) as f:
        base_module_data = f.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              base_module_data, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name='rrdraco',
    version=find_version('rrdraco', '__init__.py'),
    author='Lucas Vargas Noronha',
    author_email='lvargasnoronha@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    packages=setuptools.find_packages(exclude=("teste*", )),
)
