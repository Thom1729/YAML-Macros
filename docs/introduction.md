## How It Works

To use YAML Macros, you need two things.

A **macro library** is a Python module defining macros that you can use. Several libraries are included with the YAML Macros package, or you can write your own library with your own user-defined macros.

A **source file** is a YAML file that references a macro library and uses special syntax to invoke macros from that library.

### Basic Example

Suppose that we have two files, `example.yaml.yaml-macros` and `example.py`. These files can be found in this repository under /docs/examples/basic/.

The macro library, `example.py`:

```py
def uppercase(str):
    return str.upper()
```

This library provides a single macro, `uppercase`, which converts its argument to uppercase.

The source file, `example.yaml.yaml-macros`:

```yaml
%YAML 1.2
%TAG ! tag:yaml-macros:YAMLMacros.docs.examples.basic.example:
---
text: !uppercase 'Hello, World!'
```

Source files use YAML tags, a standard but lesser-known YAML feature. The `!uppercase` tag tells the YAML Macros engine that the value `Hello, World!` should be run through a macro called `uppercase`. The `%TAG` directive at the beginning of the file tells YAML Macros that tags beginning with `!` refer to macros in a library found at `YAMLMacros.docs.examples.basic.example`.

When you build the source file `example.yaml.yaml-macros`, the YAML Macros engine will open the source file, import the specified macro library, evaluate the `!uppercase` macro, and save the result to `example.yaml`:

```yaml
%YAML 1.2
---
text: 'HELLO, WORLD!'
```

It's as simple as that!
