from setuptools import setup, find_packages

setup(
    name ='CrickFev',
    version ='0.1',
    description = 'CLI tool for live update of cricket matches',
    author = 'Shubham Maddhashiya',
    author_email = 'shubhamsipah@iitkgp.ac.in',
    packages = find_packages(),
    include_package_data = True,
    install_requires=[
        'Click',
        'requests',
        'urllib3',
        'bs4',
    ],
    entry_points='''
        [console_scripts]
        score=CrickFev.scripts.score:cli
        levent=CrickFev.scripts.levent:main
        lscore=CrickFev.scripts.lscore:main
        lscorecard=CrickFev.scripts.lscorecard:main
    ''',
)
