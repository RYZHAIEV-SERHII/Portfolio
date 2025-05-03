# Let's break down the `awk` command:

- `-F '='`: This option sets the field separator to '='. This means `awk` will treat each line as a series of fields
  separated by '='.

- `'{ if ($1 != "" && substr($1, 1, 1) != "#") print $1 "="; else print $0 }'`: This is the `awk` script. Here's what it
  does:

  - `$1 != ""`: Checks if the first field (variable name) is not empty.

  - `substr($1, 1, 1) != "#"`: Uses the `substr` function to extract the first character of the first field, and then
      checks if it is not '#'. This condition ensures that we're not considering comment lines.

  - `print $1 "="`: If both conditions are met, it prints the first field (variable name) followed by an equals sign.

  - `else print $0`: If any of the conditions fail (i.e., if the first field is empty or starts with '#'), it prints
      the entire line (`$0`) unchanged.

- `.env > .env.example`: Redirects the output of the `awk` command to a file named `.env.example`.

Overall, this `awk` command iterates through each line of the `.env` file, checking if the first field is not empty and
does not start with '#'. If these conditions are met, it prints the variable name followed by an equals sign. Otherwise,
it prints the entire line unchanged.
