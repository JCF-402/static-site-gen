import sys

from utilities import (
    copy_source_to_destination,
    del_and_create_dst,
    generate_pages_recursive
)

def main():
    if not sys.argv[1]:
        basepath = "/"
    else:
        basepath = sys.argv[1]
    del_and_create_dst("docs")
    copy_source_to_destination("static","docs")

    generate_pages_recursive("content","template.html","docs",basepath)


main()