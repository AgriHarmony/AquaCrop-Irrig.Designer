
class ConfigHolder():
    config = {
            "controllerK": {
                "kp":1,
                "ki":1,
                "kd":1
            }
    }
    def get(self):
        return self.config

