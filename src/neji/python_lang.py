import re

__author__ = 'mturilin'


def skip_until(code, i, look_for, ignore_list):
    while i < len(code) and code[i] != look_for:
        for ignore_str in ignore_list:
            if i + len(ignore_str) < len(code):
                if code[i:i+len(ignore_str)] == ignore_str:
                    i += len(ignore_str)
                    break
        i += 1

    return i


def remove_strings(code):
    no_strings_code = ""
    i = 0
    while i < len(code):
        char = code[i]
        if char == '"': # start of the string
            i = skip_until(code, i + 1, '"', ['\\"'])
        elif char == "'":
            i = skip_until(code, i + 1, "'", ["\\'"])
        else:
            no_strings_code += char
        i += 1
    return no_strings_code


def remove_comments(code):
    return re.sub("#.*$", '', code, flags=re.M)


def remove_line_splits(code):
    return re.sub("\\\\\\s*\\n", '', code)


FORBIDDEN_KEYWORDS = [
    "eval",
    "execfile"
]
def check_keyword_errors(code):
    keyword_errors = []
    for keyword in FORBIDDEN_KEYWORDS:
        if keyword in code:
            keyword_errors.append(
                'Forbidden keyword "%s". Check Python page for explanation.' % keyword)

    return keyword_errors

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
def check_import_errors(code):
    IMPORT_EXP = "^\s*(import|from)\\s+(\\w+(,\\s*\\w+)*)"
    import_errors = []
    for match in re.finditer(IMPORT_EXP, code, re.M):
        module_names_str = match.group(2)
        module_names = [s.strip() for s in module_names_str.split(",")]
        for name in module_names:
            if name not in ALLOWED_PACKAGES:
                import_errors.append(
                    'Import from module "%s" is not allowed. Check Python page for explanation.' % name)

    return import_errors


def validate_python_code(code):
    validation_errors = []

    # Remove strings (they could fool regexps)
    code = remove_strings(code)

    # remove comments
    code = remove_comments(code)

    # checking for forbidden keywords
    validation_errors += check_keyword_errors(code)

    # Removing split line because they could confuse regexp
    code = remove_line_splits(code)

    # Removing semicolons to we could be sure there's no imports in the end of the lines
    code = code.replace(";", '\n')

    # Checking import and from statements
    validation_errors += check_import_errors(code)

    return validation_errors