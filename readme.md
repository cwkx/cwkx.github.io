# cwkx.com sources

This website is based on [suckless.org](https://suckless.org/) and follows the [suckless philosophy](https://suckless.org/philosophy/). It is simple HTML and CSS. I didn't want to use markdown or any horrible third party system such as jekyll, hugo, or wordpress.

It has two time saving scripts:

- [genbib.py](/data/genbib.py) converts the BibTeX [cgw.bib](/data/cgw.bib) into html, then injects it into `publications.html` and `index.html` accordingly. This is kept tidy using [BibTeX tidy](https://flamingtempura.github.io/bibtex-tidy/) with sort fields `-year -month -day`.

- [genblog.py](/data/genblog.py) extracts the articles from their pages, then injects them and the sidebar into `blog.html` accordingly. Run `python3 data/genblog.py` after editing a post; its `posts` list sets article order and sidebar categories.
