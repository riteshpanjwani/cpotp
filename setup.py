from setuptools import setup


with open('README.md') as f:
    long_description = f.read()

setup(
    name='cpotp',
    version='0.0.2',
    url='https://github.com/riteshpanjwani/cpotp',
    author='Ritesh Panjwani',
    author_email='riteshpanjwani@gmail.com',
    license='Apache-2.0 License',
    packages=['cpotp'],
    description='Command line tool to copy the latest OTP received in the connected Android device to the clipboard.',
    long_description=long_description,
    zip_safe=False,
    keywords = ['cpotp', 'python', 'otp', 'copy otp', 'clipboard'],
    install_requires=[line.replace('\n', '') for line in open('requirements.txt').readlines()],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['cpotp=cpotp.command_line:main']
    }
)
