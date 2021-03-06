import setuptools
exec(open('nomedoimport/modulo/_version.py').read())

setuptools.setup(
    name="PackageMeu",
    version=__version__,
    author="arthurkafer",
    author_email="arthurkafer@gmail.com",
    description="pactinho teste",
    long_description="logger basico em classe pra teste de install de pacote por pip, e outras cositas mas",
    url="https://github.com/arthurkafer/private_pip_package",
    packages=setuptools.find_packages(),
	install_requires=[
		'opencv-python>=4.1.1',
		'fuzzysearch==0.7.3',
		'fuzzywuzzy==0.18.0',
		'google-cloud==0.34.0',
		'google-cloud-vision==2.4.2'
	],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)