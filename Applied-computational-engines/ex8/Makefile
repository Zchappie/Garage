all: area_ilp area_lp pdf

area_lp:
	python area.py lp > area_lp.lp
	cat area_lp.lp
	lp_solve area_lp.lp

area_ilp:
	python area.py ilp > area_ilp.lp
	cat area_ilp.lp
	lp_solve area_ilp.lp

pdf:
	pdflatex main.tex

zip: pdf
	mv main.pdf 08_rohloff_meng_abushanab.pdf
	zip -u 08_rohloff_meng_abushanab.zip alloy.lp area.py 08_rohloff_meng_abushanab.pdf
	unzip -l 08_rohloff_meng_abushanab.zip
