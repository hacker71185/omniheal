from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="omniheal",
    version="2.4.0",
    author="hacker71185",
    author_email="hacker71185@gmail.com",
    description="OmniHeal™ — Autonomous Endpoint Diagnostics & 1-Click Self-Healing Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hacker71185/omniheal",
    py_modules=["cli"],
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Monitoring",
    ],
    install_requires=[
        "fastapi>=0.110.0",
        "uvicorn>=0.28.0",
        "psutil>=5.9.8",
        "pydantic>=2.6.0"
    ],
    entry_points={
        "console_scripts": [
            "omniheal=cli:main",
            "omniheal-cli=cli:main"
        ]
    },
    python_requires=">=3.10",
)
