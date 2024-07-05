from .environment import State

class Phone(State):
    def __init__(self):
        super().__init__(
            "phone",
            "Apps available: discord. Notifications - discord: 5 notifications.",
            {
                "open_app_discord": {
                    "next_state": "discord_home",
                    "params": {}
                },
                "put_away_phone": {
                    "next_state": "root",
                    "params": {}
                }
            }
        )