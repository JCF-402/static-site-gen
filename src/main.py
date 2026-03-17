
from utilities import (
    copy_source_to_destination,
    del_and_create_dst,
    generate_pages_recursive
)

def main():
    del_and_create_dst("public")
    copy_source_to_destination("static","public")

    generate_pages_recursive("content","template.html","public")


main()