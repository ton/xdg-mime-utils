#!/usr/bin/env python3

import argparse
import os
import sys
import textwrap

description = '''
Will update `~/.config/mimeapps.list` to add mime type associations for all
mime types that can be opened as listed in the given application `.desktop`
file. Will update `~/.config/mimeapps.list` such that it first contains a new
`[Default Applications]` section with a sorted list of all existing, newly
added, and overwritten mime type associations after processing the given
`.desktop` file, then the remaining contents of `~/.config/mimeapps.list`.
'''

parser = argparse.ArgumentParser(description=description)
parser.add_argument('desktop_file', metavar='<application .desktop file>', type=str,
        help='Path to the application .desktop file, usually in "/usr/share/applications".')

args = parser.parse_args()

if not os.path.exists(args.desktop_file):
    print(f"Error, '{args.desktop_file}' does not exist.")
    sys.exit(1)

# Read mime types from the desktop file.
mime_type_prefix = "MimeType="
application_mime_types = []
with open(args.desktop_file) as f:
    for line in f.read().splitlines():
        if line.startswith(mime_type_prefix):
            application_mime_types.extend(list(filter(None, line[len(mime_type_prefix):].strip().split(';'))))

# Read in default mime application settings.
mimeapps_filename = os.path.expanduser("~/.config/mimeapps.list")
mimeapps_lines = []
if os.path.exists(mimeapps_filename):
    with open(mimeapps_filename) as f:
        mimeapps_lines = [line.strip() for line in f.read().splitlines()]

# Construct a list of mime-type to application pairs.
default_associations = []
default_applications_header = "[Default Applications]"
other_mimeapps_lines = []
parsing_defaults = False
for line in mimeapps_lines:
    if line.startswith('['):
        parsing_defaults = line == default_applications_header
    elif parsing_defaults:
        default_associations.append(tuple(line.split('=')))
    if not parsing_defaults:
        other_mimeapps_lines.append(line)

# Remove existing file associations if overwritten, and add new mime type
# associations.
default_associations = list(filter(lambda assoc: assoc[0] not in application_mime_types, default_associations))
default_associations.extend([(mime_type, os.path.basename(args.desktop_file)) for mime_type in application_mime_types])

# Write out the new contents to ~/.config/mimeapps.list.
with open(mimeapps_filename, 'w+') as f:
    if default_associations:
        print(default_applications_header, file=f)
        for mime_type, application in sorted(default_associations):
            print(f"{mime_type}={application}", file=f)
    for line in other_mimeapps_lines:
        print(line, file=f)
