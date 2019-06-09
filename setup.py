import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pybess",
    version="0.0.5",
    author="Daniel Tam & Henry Blumentals",
    author_email="daniel.tam07@gmail.com",
    description="Energy Arbitrage for Battery Energy Storage Systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
