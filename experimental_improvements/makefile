
# LATEX MAKEFILE
# make rules for LaTeX projects, as used by Mark V in 2015 (and beyond?)
# document can contain bibtex, pythontex or gnuplot and is recompiled until stabile
# no more includes or excessive automation in this version;
#  a few things should be set by hand, marked by CAPITAL HEADERS
# 
# requires:
# - lualatex
# - bibtex if used
# - pythontex if used
# - bardeen/mpl for matplotlib image autogeneration [discouraged]
# - pdfcrop if ^
# - 

# PROJECT SETTINGS
result = report
source = $(basename $(shell ls -t v*.tex | head -1))

# makefile settings
SHELL = /bin/bash
REPORT_PATH = $(HOME)/mods/TEX/report
VPATH = $(REPORT_PATH)/tex

# latex settings
tex_compile = lualatex -interaction=nonstopmode -halt-on-error -output-directory="textmp~"
bibtex_compile = bibtex
pytex_compile = pythontex --interpreter python:python2
pdf_crop = pdfcrop
pdf_viewer = evince
max_print_line = 1024
export max_print_line
pipe = | grep -v "texmf" | grep -v "^\*"
pipe = | sed -n -e '/^! /,$$p' || true

# build the report by default
show: $(result).pdf
	# show the document, silencing useless errors
	evince "$<" 2>&1 | grep "No such file or directory" || true

# OWN DEPENDENCIES BELOW HERE

$(result).pdf: genimg~/default.pdf

genimg~/default.pdf: default.gp



# preparation steps to execute once at the start
prep:
	#todo
	@echo "warning about seeing full error log, and all-but-errors being stripped from lualatex output"
	mkdir -p textmp~/ genimg~/

# cleaning up
clean:
	rm -rf textmp~/ genimg~/
rm: clean
	rm -rf *.log *.aux *.toc *-blx.bib *.run.xml *.bbl *.blg *.out .waste *.pyc *.pytxcode pythontex-files-* $(result).pdf

# make the actual pdf file
$(result).pdf: prep $(source).tex
	# compile normally
	( $(tex_compile) -jobname="$(result)" "$(source).tex" || exit $$? ) $(pipe)
	# compile bibtex only if needs be
	if grep 'Please (re)run BibTeX' "textmp~/$(result).log"; then \
		/bin/cd "textmp~" || exit $$?; \
		$(bibtex_compile) "$(result).aux" || exit $$?; \
	fi;
	# compile pythontex only if needs be
	if grep 'pythontex.sty' "textmp~/$(result).log"; then \
		$(pytex_compile) "textmp~/$(result).pytxcode" || exit $$?; \
	fi;
	# it is assumed for now that bibtex and pythontex will need only one compile
	#@## @if grep 'Please (re)run BibTeX' "textmp~/$(result).log" || grep 'pythontex.sty' "textmp~/$(result).log"; then $(compile_cmd); fi;
	# recompile up to three times until no reruns requested
	k=3; \
	while [ $$k -gt 0 ] && grep 'Rerun to get ' "textmp~/$(result).log"; do \
		( $(tex_compile) -jobname="$(result)" "$(source).tex" || exit $$? ) $(pipe); \
		((k++)); echo "recompile #$$k/3"; \
	done
	# check if the compile was succesful
	#todo: invert to succeed only on positive match (added bonus: grep will return 1 if no result, so this will make the command fail)
	if grep 'no output PDF file produced' "textmp~/$(result).log"; then /bin/rm -f "$(result).pdf"; exit 1; else /bin/mv "textmp~/$(result).pdf" "$(result).pdf"; fi;

# create a pdf from an image tex file (gnuplot, matplotlib)
genimg~/%.pdf: genimg~/%.tex
	( $(tex_compile) -output-directory="genimg~" "$(source).tex" || exit $$? ) $(pipe)
	# compile
	# check if compile worked with grep && false || true
	# todo genimg~/%.pdf: genimg~/%.tex

# create a tex file from a gnuplot config file
# make sure that this gnuplot file is set as first preriquisite for the specific image
genimg~/%.tex: prep
	gnuplot -e "term='epslatex'; outname='$@'" default.gp
	sed -e 's/genimg~\//genimg\\string~\//' '$@' > '$@~'
	printf '\documentclass[pstricks,border=0pt,0pt]{standalone}\n\\usepackage{graphicx}\n\\begin{document}\n%s\n\\end{document}' "$$(cat '$@~')" > '$@'


#todo
#rule for turning generated images into displayable format and eog-ing (/evincing) them



