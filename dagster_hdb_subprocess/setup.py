from setuptools import find_packages, setup

setup(
    name="dagster_hdb_subprocess",
    packages=find_packages(exclude=["dagster_hdb_subprocess_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
