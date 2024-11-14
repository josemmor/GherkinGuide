#TODO: habria que pensar en tags tambien no?
class Feature:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.scenarios = []

    def add_scenario(self, scenario):
        self.scenarios.append(scenario)

class Scenario:
    def __init__(self, name):
        self.name = name
        self.steps = []

    def add_step(self, step):
        self.steps.append(step)

class Step: 
    def __init__(self, keyword, text):
        self.keyword = keyword
        self.text = text

