from lifoid.renderer import Renderer


class StdoutRenderer(Renderer):

    api = 'stdout'

    def render(self, messages, receiver_id):
    	for message in messages:
        	print(message)
