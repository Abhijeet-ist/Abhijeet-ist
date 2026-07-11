from .renderer import Renderer
from .theme import DARK, LIGHT

class SVG:

    def __init__(self, stats):

        self.stats = stats

    def generate(self):

        Renderer(

            "templates/card.svg",

            "dark_mode.svg"

        ).render(

            {

                "BACKGROUND": DARK["background"],

                "TEXT": DARK["foreground"],

                "USERNAME": self.stats.username

            }

        )

        Renderer(

            "templates/card.svg",

            "light_mode.svg"

        ).render(

            {

                "BACKGROUND": LIGHT["background"],

                "TEXT": LIGHT["foreground"],

                "USERNAME": self.stats.username

            }

        )