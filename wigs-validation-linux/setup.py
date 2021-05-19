import os
from setuptools import setup, find_packages

setup(
    name="pre_wigs_validation",
    version=os.environ.get("BUILD_VERSION", "development-build"),
    description="Pre-WIG Validator for Linux",
    author="steno",
    author_email="steno@amazon.com",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=[
        "requests==2.22.0",
        "dataclasses==0.6",
        "distro==1.4.0",
        "PrettyTable==0.7.2",
        "PyInstaller==3.4",
    ]
    # Maybe include dev dependencies in a txt file
)
