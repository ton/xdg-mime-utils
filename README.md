# xdg-mime-utils

Collection of scripts that helps with easily setting file associations using
`xdg-mime`.

### xdg-mime-default-all.py

Will update `~/.config/mimeapps.list` to add mime type associations for all
mime types that can be opened as listed in the given application `.desktop`
file. Will update `~/.config/mimeapps.list` such that it first contains a new
`[Default Applications]` section with a sorted list of all existing, newly
added, and overwritten mime type associations after processing the given
`.desktop` file, then the remaining contents of `~/.config/mimeapps.list`.
