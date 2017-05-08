from setuptools import setup, find_packages

setup(
    name='CrickFev',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'BeautifulSoup',
        'requests',
        'urllib3',
        'bs4',
    ],
    entry_points='''
        [console_scripts]
        score=CrickFev.scripts.score:cli
    ''',
)
