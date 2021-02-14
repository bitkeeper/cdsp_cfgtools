import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

#TODO: also setup 3 scripts for the configuration generators
setuptools.setup(
    name="cdsp_cfgtools",
    version="0.1.0",
    author="Marcel van de Weert",
    author_email="bikeeper@ghub-norepley.com",
    description="A library and tools for generating CamillaDSP configuration from sveral sources",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bitkeeper/cdsp_cfgtools",
    packages=setuptools.find_packages(),
    python_requires=">=3",
    install_requires=["PyYAML"],
)