from .state import State

class VirtualSpace(State):
    def __init__(self):
        super().__init__(
            "root",
            """I am in virtual space. \n
            Here are the actions I can take: \n\n
            """,
            {
                "open_phone": {
                    "next_state": "phone",
                    "params": {}
                },
            }
        )