# xdg-mime-utils

Collection of scripts that helps with easily setting file associations using
`xdg-mime`.

### `xdg-mime-default-all.py`

Will update `~/.config/mimeapps.list` to add mime type associations for all
mime types that can be opened as listed in the given application `.desktop`
file. Then outputs the contents for a new `mimeapps.list` file to standard
output, with a `[Default Applications]` section containing a sorted list of
existing and new file associations, and then the remainder of the input
`~/.config/mimeapps.list` file.
