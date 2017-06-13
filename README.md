# YAML-Macros

A macro system for YAML files powered by Python. Intended for Sublime Text development.

### Example

[Source file](examples/basic/example.yaml.yaml-macros):

```yaml
%YAML 1.2
%TAG ! tag:yaml-macros:example_macros/
---
text: !fancy title
```

[Macro file](examples/basic/example_macros.py):

```python
def fancy(str):
    return '=== %s ===' % str.capitalize()
```

[Output](examples/basic/example.yaml):

```yaml
%YAML 1.2
---
text: === Title ===
```

For a more elaborate use case, see the [SQL example](examples/sql_syntax).

## Usage

### Command Line

```
usage: cli.py [-h] [-m MACROS_PATH]

optional arguments:
  -h, --help            show this help message and exit
  -m MACROS_PATH, --macros-path MACROS_PATH
                        path to search for macro definitions
```