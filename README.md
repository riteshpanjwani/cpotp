# cpotp
[![PyPI](https://img.shields.io/pypi/v/cpotp.svg)](https://pypi.python.org/pypi/cpotp)

Command line tool to copy the latest OTP received in the connected Android device to the clipboard.

## Why?
Simply because I don't want to pickup my phone, open the SMS app, remember the OTP, and then enter it.

Now you might say, haven't you heard about https://messages.google.com? Well, that's what is being used in the package. Selenium Chrome driver automates this process.

## Prerequisite
- Python >= 3.6
- [Google Chrome](https://www.google.com/intl/en_in/chrome/) / [Chromium](https://download-chromium.appspot.com/) / [Microsoft Edge](https://www.microsoft.com/en-us/edge) / [Microsoft Edge Dev for Linux](https://www.microsoftedgeinsider.com/en-us/)
- [xclip](https://github.com/astrand/xclip) (if you're on Linux)
- Android device

## Installation

### Install cpotp

cpotp can be installed using pip

```
pip install cpotp
```

or install it from the source

```
git clone https://github.com/riteshpanjwani/cpotp.git
cd cpotp
python setup.py install
```

### Install xclip (Linux only)

If you are using any fairly recent Debian Linux-based OS:

```
sudo apt install xclip
```

else, you can install it directly from the source:

```
git clone https://github.com/astrand/xclip.git
./bootstrap
./configure
make
make install
```
Verify that it installed:

```
man xclip
```

### Set an environment variable
Next, you need to set an environment variable called CHROME_USER_DATA_DIR, in Chrome/Edge/Chromium browser new tab
```
chrome://version
```

and set this environment variable to path given in "Profile Path"
except the "/Default" part. For example:
```
export CHROME_USER_DATA_DIR=/home/<username>/.config/google-chrome
```
Selenium will create a Chrome user profile called "cpotp" in this directory.

## Usage

Note: the following command downloads the following files on the first run:
- appropriate [Chromium drivers](https://chromedriver.chromium.org/) using [pyderman](https://pypi.org/project/pyderman/)
- [NLTK punkt package](https://www.nltk.org/data.html) to [tokenize](https://nlp.stanford.edu/IR-book/html/htmledition/tokenization-1.html) the SMS

Close any instance of https://messages.google.com and fire up a terminal / command prompt and run:

```
cpotp
```

On the first run, scan the QR code using your Messages app on the phone and pair it.

## License
For license information, see [LICENSE.md](LICENSE.md).
