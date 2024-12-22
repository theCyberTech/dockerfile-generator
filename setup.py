from setuptools import setup, find_packages

setup(
    name="dockerfile-generator",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click>=8.1.0',
        'pyyaml>=6.0.1',
        'typing-extensions>=4.7.1',
    ],
    entry_points={
        'console_scripts': [
            'dockerfile-generator=dockerfile_generator.main:main',
        ],
    },
    python_requires='>=3.8',
    author="Codeium",
    author_email="support@codeium.com",
    description="A CLI tool to analyze codebases and generate optimized Dockerfiles",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/codeium/dockerfile-generator",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
