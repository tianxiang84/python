import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ts_utils", # Replace with your own username
    version="1.0",
    author="Tianxiang Su",
    author_email="su.tianxiang@gmail.com",
    description="My python utils lib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tianxiang84/python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
