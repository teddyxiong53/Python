import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="xhl_example_pkg",
    version="0.0.3",
    author="xhl",
    author_email="1073167306@qq.com",
    description="xhl example pkg description",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teddyxiong53/xhl_example_pkg",
    packages=setuptools.find_packages(),
    entry_points="""
    [console_scripts]
    xhl_example_pkg_main = xhl_example_pkg.main:main
    """,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        "Operating System :: OS Independent",
        'Topic :: Internet :: Proxy Servers',
    ],
)
