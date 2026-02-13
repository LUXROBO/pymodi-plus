from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pymodi-plus-web",
    version="0.1.0",
    author="LUXROBO",
    author_email="tech@luxrobo.com",
    description="MODI+ Python Library for Web/Pyodide - postMessage communication",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LUXROBO/pymodi-plus-web",
    packages=find_packages(),
    install_requires=[
        "pymodi-plus",  # 코어 재사용 (serial/ble 없이 설치됨)
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Environment :: Web Environment",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["modi", "modi-plus", "pyodide", "web", "webusb", "postmessage"],
)
