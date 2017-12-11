class OutputPanel():
    def __init__(self, window, name):
        self.window = window
        self.name = name

        self.view = self.window.create_output_panel(self.name)

    def show(self):
        self.window.run_command('show_panel', {'panel': 'output.%s' % self.name})

    def print(self, text):
        self.view.run_command('append', {'characters': text + '\n'})
