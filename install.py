import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    setuptools.setup(
    name='vks',
    version='1.1.9',
    author="v1a0",
    author_email="contact@v1a0.dev",
    description="vk.com opensource stalkerware",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/v1a0/vks",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['lxml', 'requests', 'sqlite3', 'Pillow']
)