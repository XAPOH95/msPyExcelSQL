from setuptools import find_packages, setup

with open("msPyExcelSQL/README.md", "r") as f:
    long_description = f.read()

setup(
    name="msPyExcelSQL",
    version="1.0.0",
    description="Package let to treat excel file as database directly or via class entity",
    package_dir={"msPyExcelSQL":"src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XAPOH95/msPyExcelSQL",
    author="Vladimir Polyakov",
    author_email="xapoh.deathsoft95@gmail.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows only",
    ],
    install_requires=["pyodbc>=4.0.39"],
    python_requires=">=3.10",    
)