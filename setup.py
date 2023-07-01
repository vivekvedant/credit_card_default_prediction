from setuptools import find_packages,setup

def get_packages():
    requirements_list = list()
    with open("requirements.txt", "r") as f:
        content = f.read()

    for package in content.split("\n"):
        if "-e ." not in package:
            requirements_list.append(package)
    
    return requirements_list


setup(
    name = "default_credit_card_predictor",
    version = "0.1",
    description = "Predict next month default credit cards",
    author = "vivek",
    author_email = "vivekvedant86@gmail.com",
    packages=find_packages(),
    install_requires =get_packages()
)