from setuptools import setup, find_packages

setup(
    name='helloworld',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'boto3',
        'apscheduler==2.1.2',
        'flask_cors',
        'requests'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)
