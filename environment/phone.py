from environment.environment import State

class Phone(State):
    def __init__(self):
        super().__init__(
            "phone",
            """You opened your phone. \n
            Available Apps: Discord, Arxiv
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
