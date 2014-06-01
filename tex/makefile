
# use bash
SHELL=/bin/bash

# input file (latest matching v*.tex)
source = $(basename $(shell ls -t v*.tex | head -1))

# set options
result = report
tex_comp = lualatex
bib_comp = bibtex
pdf_crop = pdfcrop
pdf_viewer = evince
mode = -interaction=nonstopmode -halt-on-error
opts = 
pipe = | grep -v "texmf"

# directly included pdf files (ignore color coding)
includes = $(shell cat $(source).tex | grep '\\include{.*}' | sed 's/.*include{\(.*\)}.*/\1/')
incltexs = $(includes:=.tex)

# image files
imgpgfs = $(wildcard *.pgf)
imgtexs = $(imgpgfs:.pgf=.tex)
imgpdfs = $(imgpgfs:.pgf=.pdf)

# compile everything
all: $(result).pdf
	if [ -f "$(result).pdf" ]; then echo "use 'make show' to open the pdf"; else echo "no '$(result).pdf'; making failed?"; fi;

# compile everything and show
show: $(result).pdf
	if [ -f "$(result).pdf" ]; then $(pdf_viewer) $(result).pdf; else echo "no '$(result).pdf'; making failed?"; fi;

# compile the final .pdf using all the image .pdfs
# repeat until there are no more rerun requests (max 5 times)
$(result).pdf: $(source).tex $(imgpdfs) $(incltexs)
	$(tex_comp) $(mode) $(opts) -jobname=$(result) $(source).tex $(pipe)
	k=1; while [ $$k -le 5 ] && grep 'Rerun to get ' "$(result).log"; do $(tex_comp) $(mode) $(opts) -jobname=$(result) $(source).tex $(pipe); ((k++)); done
	if grep 'Please (re)run BibTeX' $(result).log; then $(bib_comp) $(result).aux; $(tex_comp) $(mode) $(opts) -jobname=$(result) $(source).tex $(pipe); fi;
	k=1; while [ $$k -le 5 ] && grep 'Rerun to get ' "$(result).log"; do $(tex_comp) $(mode) $(opts) -jobname=$(result) $(source).tex $(pipe); ((k++)); done
	if [ -f "$(result).pdf" ] && grep 'no output PDF file produced' "$(result).log"; then /bin/rm -rf "$(result).pdf"; fi;

# convert image .tex files to .pdf files
$(imgpdfs): %.pdf: %.tex
	$(tex_comp) $(mode) $(opts) "$(basename $@).tex" $(pipe)
	$(pdf_crop) $@ $@

# convert image .pgf files to .tex files
$(imgtexs): %.tex: %.pgf
	printf '\\include{header1} \\togglefalse{headers} \\usepackage{lipsum} \\include{header2} \\begin{document} \\pagenumbering{gobble} \\input{$(basename $@).pgf} \\end{document}' > "$(basename $@).tex"

# remove temporary tex files
clean:
	/bin/rm -rf *.log *.aux *.toc *-blx.bib *.run.xml *.bbl *.blg *.out .waste

# remove temporary and result files (not source and not images)
rm:	clean
	/bin/rm -rf *.pdf $(imgtexs) .waste


