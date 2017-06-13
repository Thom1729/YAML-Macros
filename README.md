# YAML-Macros

A macro system for YAML files powered by Python. Intended for Sublime Text development.

### Usage Example

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
