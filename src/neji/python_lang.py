import re

__author__ = 'mturilin'



ALLOWED_PACKAGES = [
    "string",
    "re",
    "struct",
    "datetime",
    "numbers",
    "math",
    "decimal",
    "fractions",
    "random",
    "itertools",
    "functool",
    "operator",
    "pickle",
    "cPickle",
    "zlib",
    "gzip",
    "bz2",
    "zipfile",
    "csv",
    "io",
    "time",
    "threading",
    "time",
    "json",
    ]

def skip_until(code, i, look_for, ignore_list):
    while i < len(code) and code[i] != look_for:
        for ignore_str in ignore_list:
            if i + len(ignore_str) < len(code):
                if code[i:i+len(ignore_str)] == ignore_str:
                    i += len(ignore_str)
                    break
        i += 1

    return i



def validate_python_code(code):
    import_errors = []

    no_strings_code = ""

    # Remove strings (they could fool regexps)
    i = 0
    while i < len(code):
        char = code[i]
        if char == '"': # start of the string
            i = skip_until(code, i+1, '"', ['\\"'])
        elif char == "'":
            i = skip_until(code, i+1, "'", ["\\'"])
        else:
            no_strings_code += char
        i += 1

    # Removing split line because they could confuse regexp
    no_split_lines = re.sub("\\\\\\s*\\n", '', no_strings_code)

    # Removing semicolons to we could be sure there's no imports in the end of the lines
    no_semicolons = no_split_lines.replace(";", '\n')

    # Checking import and from statements
    IMPORT_EXP = "^\s*(import|from)\\s+(\\w+(,\\s*\\w+)*)"

    for match in re.finditer(IMPORT_EXP, no_semicolons, re.M):
        module_names_str = match.group(2)
        module_names = [s.strip() for s in module_names_str.split(",")]
        for name in module_names:
            if name not in ALLOWED_PACKAGES:
                import_errors.append(
                    'Import from module "%s" is not allowed. Check Python page for explanation.' % name)

    return import_errors