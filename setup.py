from setuptools import setup, find_packages

setup(name="tscrnsvr",
    version="0.1.0a",
    description="Cool screensavers for the terminal",
    long_description="""`Repo
<https://github.com/illinoisjackson/tscrnsvr/>`_""",
    url="https://github.com/illinoisjackson/terminal-screensavers",
    author="illinoisjackson",
    author_email="icantpostmyemailhere@gmail.com",
    license="MIT License",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
    ],
    keywords="screensaver terminal",
    packages=find_packages(exclude=["images"]),
	entry_points = {
        'console_scripts': ['tscrnsvr=tscrnsvr.cmdline:main'],
    }
)