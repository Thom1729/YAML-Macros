# YAML-Macros

A macro system for YAML files powered by Python. Intended for Sublime Text development.

### Usage Example

example.yaml.yaml-macros:

```yaml
%YAML 1.2
%TAG ! macro/example_macros/
---
text: !fancy title
```

example_macros.py:

```python
def fancy(str):
    return '=== %s ===' % str.capitalize()
```

Output at example.yaml:

```yaml
%YAML 1.2
---
text: === Title ===
```
