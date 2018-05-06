from lifoid.renderer import Renderer


class StdoutRenderer(Renderer):

    api = 'stdout'

    def render(self, message, receiver_id):
        print(message)
