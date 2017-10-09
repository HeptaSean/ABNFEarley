from distutils.core import setup
setup(
    name='abnfearley',
    packages=['abnfearley'],
    package_dir={'': 'src'},
    version='0.1',
    description='An Earley parser for ABNF grammars',
    author='Benjamin Braatz',
    author_email='sean@heptasean.de',
    url='https://github.com/HeptaSean/abnfearley',
    download_url='https://github.com/HeptaSean/abnfearley/archive/0.1.tar.gz',
    keywords=['parsing', 'ABNF', 'Earley'],
    classifiers=[],
)
