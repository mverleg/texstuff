
# this will find the latest v*.tex file and try to turn it into report.pdf
# the input file is superficially scanned for required images; also any present .pgf files are rendered to .tex and
# then .pdf automatically; anything still missing after that needs to be added manually
# see 'make show'

# use bash
#VPATH = $(strip $(subst . ,,$(subst :, ,$(subst //,,$(TEXINPUTS))))) # needs subdirectories
SHELL = /bin/bash
REPORT_PATH = $(HOME)/mods/TEX/report
VPATH = $(REPORT_PATH)/tex

# input file (latest matching v*.tex)
source = $(basename $(shell ls -t v*.tex | head -1))

# set options
result = report
tex_comp = lualatex
bib_comp = bibtex
python_comp = pythontex --interpreter python:python2 
pdf_crop = pdfcrop
pdf_viewer = evince
img_gen = python images.py
mode = -interaction=nonstopmode -halt-on-error
opts =
pipe = | grep -v "texmf"

# removes comments and double quotes from input and stores it for searching
input = $(shell sed 's/%.*$$//p' $(source).tex | sed 's/"//')
# find images; grep finds input/includegraphics in (only) the main input file, then sed captures the filenames and
# uniq removes duplicates; then department logo is appended
images = $(shell echo "$(input)" | grep --only-matching --regexp \
	'\\\(input\|includegraphics\)\(\[[^][]*\]\)\?{[^{}]\+}' | sed -n 's/.*{\(.*\)}.*/\1/p' | uniq) \
	$(shell sed -n 's/.*{\\departmentlogo}{\([^{}]\+\)}.*/\1/p' $(source).tex)
# find included pdf files; method similar to image search
includes = $(shell echo "$(input)" | grep --only-matching --regexp '\\include{[^{}]*}' | sed 's/.*{\(.*\)}.*/\1.tex/' | uniq)

# image files
img_pgfs = $(sort $(wildcard *.pgf) $(filter %.pgf,$(images)))
img_texs = $(img_pgfs:.pgf=.tex)
img_pdfs = $(img_pgfs:.pgf=.pdf)
report_imgs = $(notdir $(wildcard $(REPORT_PATH)/img/*.pgf) $(wildcard $(REPORT_PATH)/img/*.jpg) $(wildcard $(REPORT_PATH)/img/*.png))
gen_imgs = $(filter-out $(report_imgs),$(images))

# alias
compile = $(tex_comp) $(mode) $(opts) -jobname="$(result)" "$(source).tex" $(pipe)


# default action to compile the whole project
all: show $(img_pdfs)

# compile everything without showing
bg: $(result).pdf
	@if [ -f "$(result).pdf" ]; then echo "use 'make show' to open the pdf"; else echo "no '$(result).pdf'; making failed?"; fi;

# compile everything and show
show: $(result).pdf
	@if [ -f "$(result).pdf" ]; then $(pdf_viewer) "$(result).pdf"; else echo "no '$(result).pdf'; making failed?"; fi;

# recompile
re: rm show
	@echo "clearing derived files and remaking project"

# information
info:
	@echo ""
	@echo "build the latest v*.tex file ($(source).tex) into $(result).pdf, while trying"
	@echo "to generate build dependencies such as pgf->pdf images and mpl generation"
	@echo ""
	@echo "info:   show this info"
	@echo "debug:  show debug info"
	@echo "show:   build the report and open it [default]"
	@echo "bg:     build the report"
	@echo "re:     clear and then rebuild the project"
	@echo "single: one compile iteration (possibly missing references)"
	@echo "merge:  resolve all inputs and replace python by output"
	@echo "clean:  remove temporary build files"
	@echo "rm:     remove many derived files (not images)"
	@echo "imgs:   regenerate all images"
	@echo ""
	@echo "other targets: $(result).pdf $(img_pdfs) $(report_imgs) $(gen_imgs)"
	@echo ""
	@echo "generated images don't check for updates in their dependencies (network of "
	@echo "python files); they have to be manually regenerated using imgs or their filename"
	@echo ""

# debug info - subject to change
debug:
	@echo "SHELL:       $(SHELL)"
	@echo "REPORT_PATH: $(REPORT_PATH)"
	@echo "VPATH:       $(VPATH)"
	@echo "TEXINPUTS:   $(TEXINPUTS)"
	@echo "source:      $(source)"
	@echo "result:      $(result)"
	@echo "tex_comp:    $(tex_comp)"
	@echo "bib_comp:    $(bib_comp)"
	@echo "pdf_crop:    $(pdf_crop)"
	@echo "pdf_viewer:  $(pdf_viewer)"
	@echo "img_gen:     $(img_gen)"
	@echo "mode:        $(mode)"
	@echo "opts:        $(opts)"
	@echo "pipe:        $(pipe)"
	@echo "compile:     $(compile)"
	@echo "img_pgfs:    $(img_pgfs)"
	@echo "img_texs:    $(img_texs)"
	@echo "img_pdfs:    $(img_pdfs)"
	@echo "report_imgs: $(report_imgs)"
	@echo "gen_imgs:    $(gen_imgs)"
	@echo "images:      $(images)"
	@echo "includes:    $(includes)"
	@echo ""
	@echo "if there is no rule to make files like header*.tex, check that REPORT_PATH (top) is set "
	@echo "correctly; currently it is set to $(REPORT_PATH) and tex/ contains: "
	@echo "$(shell ls $(REPORT_PATH)/tex/)"

# remove temporary tex files
clean:
	/bin/rm -rf *.log *.aux *.toc *-blx.bib *.run.xml *.bbl *.blg *.out .waste *.pyc *.pytxcode pythontex-files-*

# remove temporary and result files (not source and not images)
rm:	clean
	/bin/rm -rf *.pdf $(img_pgfs) $(report_imgs)

imgs:
	cp -r $(addprefix $(REPORT_PATH)/img/,$(filter $(report_imgs),$(images))) .
	$(img_gen) $(gen_imgs)

# compile the final .pdf using all the image .pdfs
# repeat until there are no more rerun requests (max 5 times)
$(result).pdf: $(source).tex $(includes) $(images)
	$(compile)
	@k=1; while [ $$k -le 5 ] && grep 'Rerun to get ' "$(result).log"; do $(compile); ((k++)); done
	@if grep 'Please (re)run BibTeX' "$(result).log"; then $(bib_comp) "$(result).aux"; $(compile); fi;
	@if grep 'pythontex.sty' "$(result).log"; then $(python_comp) "$(result).pytxcode"; $(compile); fi;
	@k=1; while [ $$k -le 5 ] && grep 'Rerun to get ' "$(result).log"; do $(compile); ((k++)); done
	@if [ -f "$(result).pdf" ] && grep 'no output PDF file produced' "$(result).log"; then /bin/rm -rf "$(result).pdf"; fi;

# single run compile; may have missing page numbers and references, but faster
single: "$(source).tex" $(includes) $(images)
	$(compile)
	@if grep 'Please (re)run BibTeX' "$(result).log"; then $(bib_comp) "$(result).aux"; fi;
	@if grep 'pythontex.sty' "$(result).log"; then $(python_comp) "$(result).pytxcode"; fi;
	@if grep 'Please (re)run BibTeX' "$(result).log" "$(result).log" || grep 'pythontex.sty' "$(result).log"; then $(compile); fi;
	@if grep 'Rerun to get ' "$(result).log"; then echo "document needs to be compiled again"; fi
	@if [ -f "$(result).pdf" ] && grep 'no output PDF file produced' "$(result).log"; then /bin/rm -rf "$(result).pdf"; else $(pdf_viewer) "$(result).pdf"; fi;

# resolve all includes to create one single document, and replace all python code by it's output
flatten: "$(source).tex" $(includes)
	@echo "NOT YET IMPLEMENTED!"
	# flatex
	# depythontex

# convert image .tex files to .pdf files
$(img_pdfs): %.pdf: %.tex
	$(tex_comp) $(mode) $(opts) "$(basename $@).tex" $(pipe)
	$(pdf_crop) $@ $@

# convert image .pgf files to .tex files
$(img_texs): %.tex: %.pgf
	printf '\\include{header1} \\togglefalse{headers} \\usepackage{lipsum} \\include{header2} \\begin{document} \\pagenumbering{gobble} \\input{$(basename $@).pgf} \\end{document}' > "$(basename $@).tex"

# copy static images that are in report module
$(report_imgs): %: $(REPORT_PATH)/img/%
	cp -r $< $@

# generate images
$(gen_imgs): %:
	$(img_gen) $@


