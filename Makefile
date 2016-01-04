
all: exe clean

info:
	cat *.py | wc -l
	cat *.py | grep TODO | grep -v TODONE

clean:
	rm -f *.pyc

exe: *.py
	python main.py
