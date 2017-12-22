# API Reference

### <code>process_macros(<var>input</var>, <var>arguments</var>={})</code>

Interprets <code><var>input</var></code> as YAML, loads and applies any macros, and returns a Python data structure representing the result.

<dl>
<dt><code><var>input</var></code></dt><dd>A <code>string</code> that is a valid YAML document.</dd>
<dt><code><var>arguments</var></code></dt><dd>A <code>dict</code> of arguments to pass to the macro engine.</dd>
</dl>