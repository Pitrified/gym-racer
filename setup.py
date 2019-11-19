import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# define the name to import the env
# import gym_racer
setuptools.setup(
    name="gym_racer",
    version="0.0.2",
    author="Pitrified",
    author_email="pitrified.git@gmail.com",
    description="OpenAI gym environment of a racing car.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pitrified/gym-racer",
    packages=setuptools.find_packages(where="."),
    install_requires=["gym", "pygame", "numpy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
