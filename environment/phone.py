from .state import State

class Phone(State):
    def __init__(self):
        super().__init__(
            "phone",
            """I am checking my phone. \n
            I see Available Apps: Discord, Arxiv
            """,
            {
                "open_app_discord": {
                    "next_state": "discord_home",
                    "params": {}
                },
                "open_app_arxiv": {
                    "next_state": "arxiv_app",
                    "params": {}
                },
                "put_away_phone": {
                    "next_state": "root",
                    "params": {}
                }
            }
        )
