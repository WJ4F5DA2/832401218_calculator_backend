# Code Style (Backend)

This project follows the **PEP 8 — Style Guide for Python Code**
(source: https://peps.python.org/pep-0008/), with the following
project-specific conventions.

## 1. Formatting

- Indent with 4 spaces; never use tabs.
- Limit lines to 79 characters; limit comments and docstrings to 72
  characters (except where longer lines are needed for display).
- Separate top-level functions and classes with 2 blank lines; separate
  methods inside a class with 1 blank line.

## 2. Naming

| Object | Convention | Example |
| --- | --- | --- |
| Modules / packages | lowercase, underscores if needed | `calculator_service` |
| Classes | CapWords | `ExpressionError` |
| Functions / variables / attributes | lowercase_with_underscores | `fetch_all_records` |
| Constants | UPPER_CASE_WITH_UNDERSCORES | `DB_PATH` |
| Private members | single leading underscore | `_parse_expr` |

## 3. Imports

- One import per line, grouped in order: standard library, third-party,
  local modules, with a blank line between groups.
- Never use `from x import *`.

## 4. Comments and Docstrings

- Public modules, classes and functions must have docstrings stating
  responsibility, arguments, return values and raised exceptions.
- Inline comments are separated from code by at least two spaces and
  start with `# `.

## 5. Other Conventions

- Never process user input with `eval`, `exec`, or any equivalent
  arbitrary-code execution facility.
- Prefer f-strings or `%` formatting for string formatting; keep one
  style consistent within a file.
- Use parameterized SQL for all database access; never build SQL by
  string concatenation.
- Catch specific exceptions only; never use a bare `except:`.
