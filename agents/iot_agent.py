
class IoTAgent:
    """
    Simulation de commandes Arduino sans carte physique.

    LIGHT_ON  -> 1
    LIGHT_OFF -> 0
    """

    def __init__(self):
        self.light_state = 0

    def execute(self, device, state):
        device = str(device).lower().strip()
        state = str(state).lower().strip()

        if device != "light":
            return {
                "handled": True,
                "agent": "IoTAgent",
                "response": "Cet objet n'est pas reconnu.",
                "emotion": "neutral"
            }

        if state == "on":
            self.light_state = 1
            response = "J'ai allumé la lumière."

        elif state == "off":
            self.light_state = 0
            response = "J'ai éteint la lumière."

        else:
            return {
                "handled": True,
                "agent": "IoTAgent",
                "response": "Commande non reconnue.",
                "emotion": "neutral"
            }

        print("\n" + "=" * 35)
        print("      MONITEUR SERIE VIRTUEL")
        print("=" * 35)
        print(self.light_state)
        print("=" * 35 + "\n")

        return {
            "handled": True,
            "agent": "IoTAgent",
            "response": response,
            "emotion": "happy"
        }
