from setuptools import setup, find_packages
# python setup.py develop
setup(
    name='dbaric_parser_gid',
    version="0.0.1",
    author="Davor Baric",
    author_email="davorbaric1r@example.com",
    description="package for parse_gid script",
    url="https://github.com/dbaric95/BigData_Parser/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'parse_gid_files=parse_gid_files:main',
        ],
    },
    package_dir={'': 'src'},
    py_modules=["parse_gid_files"],
    python_requires='>=3.7',
    install_requires=[
        'statistics'
    ],
)

