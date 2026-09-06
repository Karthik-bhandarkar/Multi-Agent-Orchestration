from setuptools import setup, find_packages

setup(
    name="edupulse-ai",
    version="0.1.0",
    description="EduPulse AI - Enterprise Multi-Agent Educational Governance System",
    author="<your-name>",
    packages=find_packages(include=["src", "src.*"]),
    python_requires=">=3.10",
    install_requires=[],
    include_package_data=True,
)