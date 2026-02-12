from os import path
from io import open
from setuptools import setup, find_packages


def get_spec(filename: str, mode: str="r"):
    def wrapper():
        here = path.dirname(__file__)
        result = {}
        with open(path.join(here, filename), encoding="utf8") as src_file:
            if mode == "d":
                exec(src_file.read(), result)
            else:
                result = src_file.read()
        return result
    return wrapper


get_about = get_spec("./modi_plus/about.py", "d")
get_readme = get_spec("README.md")
get_history = get_spec("HISTORY.md")
get_requirements_dev = get_spec("requirements-dev.txt")

# 최소 의존성 (Pyodide 호환)
INSTALL_REQUIRES = [
    'nest-asyncio>=1.5.4',
    'packaging>=21.3',
]

# Optional 의존성
EXTRAS_REQUIRE = {
    'serial': [
        'pyserial>=3.5',
    ],
    'ble': [
        'bleak>=0.13.0; sys_platform == "win32"',
        'bleak>=0.13.0; sys_platform == "darwin"',
    ],
    'websocket': [
        'websocket-client>=1.2.3',
    ],
    'all': [
        'pyserial>=3.5',
        'bleak>=0.13.0; sys_platform == "win32"',
        'bleak>=0.13.0; sys_platform == "darwin"',
        'websocket-client>=1.2.3',
        'winusbcdc>=1.4; sys_platform == "win32"',
        'pexpect; sys_platform == "linux"',
    ],
}
EXTRAS_REQUIRE['dev'] = get_requirements_dev()

about = get_about()
setup(
    name=about["__title__"],
    version=about["__version__"],
    author=about["__author__"],
    author_email=about["__email__"],
    description=about["__summary__"],
    long_description=get_readme() + "\n" + get_history(),
    long_description_content_type="text/markdown",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    license=about["__license__"],
    include_package_data=True,
    keywords=["python", "modi", "modi-plus", "modi_plus", "modi+"],
    packages=find_packages(
        include=[
            "modi_plus", "modi_plus.util", "modi_plus.task", "modi_plus.task.ble_task",
            "modi_plus.module",
            "modi_plus.module.setup_module",
            "modi_plus.module.input_module",
            "modi_plus.module.output_module"
        ]
    ),
    test_suite="tests",
    url=about["__url__"],
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
