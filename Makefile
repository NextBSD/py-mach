RM ?= /bin/rm
PYTHON ?= /usr/local/bin/python2.7
PREFIX ?= /usr/local

build:
	${PYTHON} setup.py build

install: build
	${PYTHON} setup.py install --prefix ${PREFIX}

clean:
	${PYTHON} setup.py clean
	${RM} -rf build
	${RM} src/*.c
