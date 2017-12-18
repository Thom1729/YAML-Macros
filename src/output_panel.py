class OutputPanel():
    def __init__(self, window, name, *, clear=True, show=True):
        self.window = window
        self.name = name

        self.view = (
            self.window.find_output_panel(self.name) or
            self.window.create_output_panel(self.name)
        )

        if clear: self.clear()
        if show: self.show()

    def show(self):
        self.window.run_command('show_panel', {'panel': 'output.%s' % self.name})

    def print(self, text=''):
        self.view.run_command('append', {'characters': text + '\n'})

    def clear(self):
        self.view.run_command('clear_view')
