# History of Digital Cultures (HDC) project

In this Git is the source code needed for a HDC project.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* A GNU/Linux distribution
* [Python 3.6.4](https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tar.xz)
* [Frog 0.13.9](https://github.com/LanguageMachines/frog/releases/download/v0.13.9/frog-0.13.9.tar.gz)

### Frog overlay for Gentoo

See [this repo](https://github.com/Shoaloak/frog-overlay)

### Python Dependencies

When you have Frog installed, clone our repo, create and activate a virtual python environmenti (venv).
```
python3.6 -m venv venv
source venv/bin/activate
```

Install python dependencies, unfortunately some dependencies are retarded (looking at python-frog).
Which means you must first install Cython or you will run into the
```
ModuleNotFoundError: No module named 'Cython'
```
error. After installing Cython you can install the dependencies using
```
pip install -r requirements.txt
```

We are also using [nltk-frog](https://github.com/paudan/nltk-frog) by Paulius Danenas.
Clone his git and whilst stil active in your venv, navigate to the cloned repo and install his package.
```
python setup.py install
```

### How to use our beautiful software
TODO.


## Authors

* **Axel Koolhaas**
* **Rink Stiekema**
* **Giorgi Kikolashvili**
* **Judith Schermer**
* **Kjell Zijlemaker**
* **Freddy de Greef**

## License

This project is licensed under the ? License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone who's code was used

