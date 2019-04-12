from setuptools import find_packages, setup


setup(
    name="whatsapp",
    version="0.0.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
       'tensorflow<2.0',
       'numpy>=1.16',
    ]
)
