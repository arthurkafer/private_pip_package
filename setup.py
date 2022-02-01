import setuptools
print(setuptools.find_packages())

setuptools.setup(
    name="pacotinho",
    version="0.0.1",
    author="arthurkafer",
    author_email="arthurkafer@gmail.com",
    description="pactinho teste",
    long_description="logger basico em classe pra teste de install de pacote por pip",
    url="https://github.com/arthurkafer/private_pip_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)