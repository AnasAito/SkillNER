# Makefile for Sphinx documentation

# These variables can be set from the CLI.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
BUILDDIR      = _build

OUTPUTDIR = _build/html

# User-friendly check for sphinx-build
ifeq ($(shell which $(SPHINXBUILD) >/dev/null 2>&1; echo $$?), 1)
$(error The '$(SPHINXBUILD)' command was not found. Make sure you have Sphinx installed, then set the SPHINXBUILD environment variable to point to the full path of the '$(SPHINXBUILD)' executable. Alternatively you can add the directory with the executable to your PATH. If you don't have Sphinx installed, grab it from http://sphinx-doc.org/)
endif

# Internal variables.
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .


.PHONY: help
help:
	@echo "Run \`make <target>' where <target> is one of"
	@echo "  html       to make standalone HTML files"
	@echo "  clean      to delete the built documentation"


.PHONY: clean
clean:
	rm -rf $(BUILDDIR)/*
	rm -rf auto_examples/
	rm -rf generated/*
	rm -rf modules/*


.PHONY: html
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."
