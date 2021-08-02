import os
import sys
import tempfile
import getpass
from itertools import zip_longest
from upload_to_website import upload_to_website
from process_photos import process_photos


def generate_report_text(input_report_file: str, input_photo_dir: str, year: int, upload_dir_name: str):
    upload_photo_dir = f"/WebImages/{year}/{upload_dir_name}"
    lightbox_name = upload_dir_name

    with open(input_report_file, 'r', encoding='utf8') as f:
        report_text = f.read()

    report_paragraphs = [f"<p>{p.strip()}</p>" for p in report_text.split('\n')]

    photo_names = [f for f in os.listdir(input_photo_dir) if "Small" not in f]

    all_photo_html = []
    for i, photo_name in enumerate(photo_names):
        name_without_ext, ext = os.path.splitext(photo_name)
        small_name = name_without_ext + "Small" + ext
        is_even = i % 2 == 0

        photo_html = f"""<a href="{upload_photo_dir}/{photo_name}" data-lightbox="{lightbox_name}"><img src="{upload_photo_dir}/{small_name}" class="Float{'Right' if is_even else 'Left'}Image"></a>"""
        all_photo_html.append(photo_html)

    output_parts = []
    for paragraph, photo in zip_longest(report_paragraphs, all_photo_html, fillvalue=None):
        if photo is not None:
            output_parts.append(photo)
        if paragraph is not None:
            output_parts.append(paragraph)

    output_string = "\n".join(output_parts)
    return output_string


def make_report(input_report_file: str, input_photo_dir: str, year: int, upload_dir_name: str, report_title: str,
                username: str, password: str):
    report_content = generate_report_text(input_report_file, input_photo_dir, year, upload_dir_name)

    with tempfile.TemporaryDirectory() as processed_photo_dir:
        process_photos(input_photo_dir, processed_photo_dir)

        upload_to_website(year, processed_photo_dir, upload_dir_name, username, password, report_title, report_content)


def show_help():
    help_text = r"""
    
    USAGE
    python make_report.py <input_report_filename> <input_photo_dir> <year> <upload_dir_name> <report_title> <username>
    
    EXAMPLE
    python make_report.py my_report.txt "C:\Users\Ben Windsor\Pictures\DrongO Event" 2021 20210512DrongOEvent "About a DrongO event" drongousername
    
    """

    print(help_text)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]:
        show_help()
        sys.exit(0)

    if len(sys.argv) != 7:
        show_help()
        sys.exit(1)

    _input_report_file = sys.argv[1]
    _input_photo_dir = sys.argv[2]

    _year = int(sys.argv[3])
    _upload_dir_name = sys.argv[4]

    _report_title = sys.argv[5]

    _username = sys.argv[6]

    _password = getpass.getpass()

    make_report(_input_report_file, _input_photo_dir, _year, _upload_dir_name, _report_title, _username, _password)
