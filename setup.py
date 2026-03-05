from setuptools import setup, find_packages

# Try to read requirements.txt, fallback to empty list if not found
try:
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    requirements = []

try:
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Sistema de Controle de Planos - Flask Application"

setup(
    name="controle-planos-flask",
    version="1.0.0",
    description="Sistema de Controle de Planos - Flask Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/controle-planos-flask",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "controle-planos=app:main",
        ],
    },
    keywords="flask web application controle planos seguros",
)
