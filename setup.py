from setuptools import setup, find_packages

setup(
    name="PySharer",
    version="1.0.0",
    description="A Flask-based web application for sharing files using LAN.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Muhammad Bilal Azaad",
    author_email="mr.bilal2066@gmail.com",
    url="https://github.com/Mr-Bilal-Ashraf/PySharer",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'PySharer': [
            'templates/*.html',
            'static/**/*',
        ],
    },
    install_requires=[
        "Flask>=2.0.0",
        "Werkzeug>=2.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Flask",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "pysharer=PySharer.run:start",
        ],
    },
)
