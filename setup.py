from setuptools import setup, find_packages

setup(
    name="tower-defense",
    version="1.0.0",
    description="Mr. Mega's Awesome Tower Defense Game",
    author="Ben",
    author_email="benmega@gmail.com",
    python_requires=">=3.9",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame==2.5.2",
        "pygame-gui==0.6.9",
    ],
    entry_points={
        "console_scripts": [
            "tower-defense=main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Games/Entertainment :: Real Time Strategy",
    ],
    include_package_data=True,
    package_data={
        "": [
            "assets/**/*",
            "src/config/theme.json",
            "src/config/levels/*.json",
        ]
    },
)
