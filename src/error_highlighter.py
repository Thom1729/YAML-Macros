import sublime

PHANTOM_TEMPLATE="""
<div class="error">{}</div>
"""

class ErrorHighlighter():
    def __init__(self, window, name, *, clear=True):
        self.window = window
        self.name = name
        if clear: self.clear()

    def clear(self):
        for view in self.window.views():
            view.erase_phantoms(self.name)

    def highlight(self, file_path, row, col, message):
        view = self.window.find_open_file(file_path)
        if view:
            view.add_phantom(
                self.name,
                sublime.Region(row, col),
                PHANTOM_TEMPLATE.format(message),
                sublime.LAYOUT_BELOW,
            )
