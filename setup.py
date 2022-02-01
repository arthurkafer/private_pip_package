import setuptools

setuptools.setup(
    name="packagemaior",
    version="0.0.1",
    author="arthurkafer",
    author_email="arthurkafer@gmail.com",
    description="pactinho teste",
    long_description="logger basico em classe pra teste de install de pacote por pip, e outras cositas mas",
    url="https://github.com/arthurkafer/private_pip_package",
    packages=setuptools.find_packages(),
	install_requires=[
		'numpy'
	],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)