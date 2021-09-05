# Sample Usage

This document contains a guide for the usage of the `pdfsplit` script.

## Setup

This guide uses the Adobe PDF 1.6 specification file (~9 MB).

It can be downloaded using:

```shell
$ wget https://wwwimages2.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/pdf_reference_archives/PDFReference16.pdf
```

or from [https://www.pdfa.org/resource/pdf-specification-index/](https://www.pdfa.org/resource/pdf-specification-index/).

The shell commands in this file assume `pdfsplit` is in your `PATH`.

### Offset

There are 22 pages in the PDF file before the page numbered `1`.
This PDF conveniently numbers these pages using roman numerals, but
you may need to manually count or use your PDF reader's "current page"
function.

## Extracting Chapters

[pdf-1.6-chapters.txt](pdf-1.6-chapters.txt) contains a manually parsed
list from the PDF's table of contents for chapters. With some PDFs you may
need to manually search for the ending page of each chapter since they may
have miscellaneous pages in between chapters.

We'll extract the chapters from the PDF into a directory called "Chapters"
and name each chapter PDF as `chXX.pdf` with the following commands:

```shell
$ mkdir Chapters
$ pdfsplit PDFReference16.pdf pdf-1.6-chapters.txt "Chapters/ch{_i:02d}.pdf" -o 22
$ ls -1 Chapters
ch01.pdf
ch02.pdf
ch03.pdf
ch04.pdf
ch05.pdf
ch06.pdf
ch07.pdf
ch08.pdf
ch09.pdf
ch10.pdf
```

## Extracting Appendices

[pdf-1.6-appendices.txt](pdf-1.6-appendices.txt) contains a manually parsed
list from the PDF's table of contents for appendices.

Appendices are often named using letters instead of numbers. Since the
`out_fmt` string is interpreted as a Python f-string, we can execute
Python code to convert 1-indexed numbers to capital letters.

```shell
$ mkdir Appendices
$ pdfsplit \
    PDFReference16.pdf \
    pdf-1.6-appendices.txt \
    "Appendices/Appendix {chr(ord('A') - 1 + _i)}.pdf" \
    -o 22
$ ls -1 Appendices
'Appendix A.pdf'
'Appendix B.pdf'
'Appendix C.pdf'
'Appendix D.pdf'
'Appendix E.pdf'
'Appendix F.pdf'
'Appendix G.pdf'
'Appendix H.pdf'
'Appendix I.pdf'
```
