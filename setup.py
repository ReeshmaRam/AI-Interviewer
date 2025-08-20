from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.strip() for req in requirements if req.strip() and not req.startswith('-e')]
    return requirements

setup(
    name="AI_interviewer",
    version="0.0.1",
    author="Reeshma Ram Prasad",
    author_email="reeshmarajan01@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")
)
