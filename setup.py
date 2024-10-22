from setuptools import setup, find_packages

setup(
    name="OpenAI-Helper",
    version="0.1.0",
    description="A helper package for OpenAI API",
    author="Yining Hong",
    author_email="yhong3@andrew.cmu.edu",
    packages=find_packages(),  # Automatically finds and includes all packages in the directory
    install_requires=[
        "openai>=1.0.0",
    ],  # List of dependencies, e.g., ['numpy', 'requests']
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
