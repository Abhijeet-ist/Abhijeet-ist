from pathlib import Path


class Renderer:

    def __init__(

        self,

        template,

        output

    ):

        self.template = Path(template)

        self.output = Path(output)

    def render(self, values):

        svg = self.template.read_text()

        for key, value in values.items():

            svg = svg.replace(

                "{{" + key + "}}",

                str(value)

            )

        self.output.write_text(svg)