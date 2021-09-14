import os
import sys
import tempfile
import getpass
from typing import List, Optional
from itertools import zip_longest
from upload_to_website import upload_to_website
from process_photos import process_photos
from drongo_types import Section


class Builder:
    def __init__(self):
        self._sections = []
        self._current_section = None

    def new_section(self, title: Optional[str]):
        if self._current_section is not None:
            self._sections.append(self._current_section)
        self._current_section = Section(title, "")

    def append_line(self, line: str):
        if self._current_section is None:
            self._current_section = Section(title=None, content="")
        self._current_section.content = self._current_section.content + line + "\n"

    def build(self) -> List[Section]:
        self._sections.append(self._current_section)
        return self._sections


def generate_report_text(input_report_file: str, input_photo_dir: str, year: int, upload_dir_name: str) -> List[Section]:
    upload_photo_dir = f"/WebImages/{year}/{upload_dir_name}"
    lightbox_name = upload_dir_name

    with open(input_report_file, 'r', encoding='utf8') as f:
        report_text = f.read()

    report_paragraph_contents: List[str] = [p.strip() for p in report_text.split('\n') if len(p.strip()) > 0]

    photo_names = [f for f in sorted(os.listdir(input_photo_dir)) if "Small" not in f]

    all_photo_html = []
    for i, photo_name in enumerate(photo_names):
        name_without_ext, ext = os.path.splitext(photo_name)
        small_name = name_without_ext + "Small" + ext
        is_even = i % 2 == 0

        photo_html = f"""<a href="{upload_photo_dir}/{photo_name}" data-lightbox="{lightbox_name}"><img src="{upload_photo_dir}/{small_name}" class="Float{'Right' if is_even else 'Left'}Image"></a>"""
        all_photo_html.append(photo_html)

    builder = Builder()

    photo_idx = -1
    for paragraph in report_paragraph_contents:
        if paragraph.startswith('# '):
            builder.new_section(paragraph[1:].strip())
            continue

        photo_idx += 1
        if photo_idx < len(all_photo_html):
            photo = all_photo_html[photo_idx]
        else:
            photo = None

        if photo is not None and paragraph is not None:
            builder.append_line(f"<p>{photo}{paragraph}</p>")
        elif photo is not None:
            builder.append_line(photo)
        elif paragraph is not None:
            builder.append_line(f"<p>{paragraph}</p>")

    return builder.build()


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
