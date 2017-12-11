import sublime

class PhantomManager():
    def __init__(self, view, key, *,
        layout=sublime.LAYOUT_BELOW, template='{}'
    ):
        self.view = view
        self.key = key
        self.layout = layout
        self.template = template

    def add(self, region, content, *, layout=None):
        self.view.add_phantom(
            self.key,
            region,
            self.template.format(content),
            layout if layout else self.layout,
        )

    def clear(self):
        self.view.erase_phantoms(self.key)
