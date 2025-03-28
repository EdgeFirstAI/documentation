![toonshaded](static/toonshaded_small.png)

# EdgeFirst Modules User Manual

This is the source for the EdgeFirst Modules User Manual.  The documentation is writen using Sphinx and rendered into HTML and PDF formats.

# Setup

Make sure you have `git-lfs` correctly configured as it is required to manage binary assets, such as images.  Otherwise you'll need Python with the `virtualenv` module to create a virtual environment (not strictly required but suggested).

```bash
git clone git@github.com:MaivinAI/manual.git
cd manual
git lfs pull
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
make
```

Note: Windows needs to replace `source venv/bin/activate` with `venv\Scripts\activate.bat`.

