#! /usr/bin/env python3

import argparse
import os
import re
import time

from PyPDF2 import PdfFileReader, PdfFileWriter


def parse_args() -> argparse.Namespace:
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(description="Split PDF files.")

    parser.add_argument("infile", help="The PDF file to split.", type=str)

    parser.add_argument(
        "pagefile", help="A text file containing 1-indexed page ranges.", type=str
    )

    parser.add_argument(
        "out_fmt", help="A Python format string for output files.", type=str
    )

    parser.add_argument(
        "-o",
        "--offset",
        default=0,
        metavar="offset",
        help="The number of leading pages in the `infile` to skip.",
        type=int,
    )

    args = parser.parse_args()

    # argument validation
    if not args.infile.endswith(".pdf") or not os.path.exists(args.infile):
        raise OSError(f"`{args.infile}` is not a PDF file.")

    if not os.path.exists(args.pagefile):
        raise FileNotFoundError(f"`{args.pagefile}` does not exist.")

    if not args.out_fmt.endswith(".pdf"):
        args.out_fmt += ".pdf"

    # TODO: move this to parse_page_ranges
    with open(args.pagefile, "r") as pagefile:
        lines = pagefile.readlines()
        for line_no, line in enumerate(lines):
            line = line.strip()
            if not re.fullmatch(r"^\d+( +\d+)?$", line):
                raise ValueError(
                    f"`{args.pagefile}` is not formatted correctly\n"
                    f"(line {line_no + 1}: {line})"
                )

    return args


def extract(reader: PdfFileReader, start: int, end: int, o_filename: str) -> None:
    """Create a new PDF from the page range [start, end) in the PDF
    opened by `reader`.

    Assumes the interval [start, end) is within the page range of `reader`.

    Args:
        reader: A PdfFileReader containing the PDF to split.
        start: The index of the first page to include in the new PDF.
        end: The terminating page number of the inclusion interval.
        o_filename: The name of the new PDF.
    """
    start_time = time.time()

    writer = PdfFileWriter()
    for page in range(start, end):
        writer.addPage(reader.getPage(page))

    # TODO: If I remember correctly, there were problems opening some
    # split PDFs due to broken links. Is there a way to keep links that
    # still work after the split?
    writer.removeLinks()
    writer.write(open(o_filename, "w+b"))

    elapsed = time.time() - start_time
    print(f"`{o_filename}` processed in {elapsed:.2f} seconds", flush=True)


def parse_page_ranges(pagefile: str, offset: int) -> list[tuple[int, int]]:
    """Parse the intervals in the `pagefile`."""
    assert offset >= 0, "Offset should not be negative."

    page_ranges: list[list[int]] = []

    with open(pagefile, "r") as f:
        for line in f:
            line = line.strip()
            # The numbers specified in the `pagefile` should be 1-indexed.
            # PdfFileReader uses 0-indexing.
            interval = [int(token) + offset - 1 for token in line.split()]
            page_ranges.append(interval)

    for i in range(len(page_ranges) - 1):
        # Complete intervals without an end index using the start index
        # of the next interval
        if len(page_ranges[i]) == 1:
            page_ranges[i].append(page_ranges[i + 1][0])

    if len(page_ranges[-1]) == 1:
        # Remove the last entry in `page_ranges` if it does not
        # constitute a valid interval.
        page_ranges.pop()

    return [(r[0], r[1]) for r in page_ranges]


def main() -> None:
    args = parse_args()

    page_ranges = parse_page_ranges(args.pagefile, args.offset)
    reader = PdfFileReader(args.infile)

    for (i, (start, end)) in enumerate(page_ranges):
        # format the output filename with 1-indexed numbers
        o_filename = args.out_fmt.format(i + 1)
        extract(reader, start, end, o_filename)


if __name__ == "__main__":
    main()
