class ComponentManager(object):

    def __init__(self):
        self.components = {}
        
    def register_component(self, name, component):
        self.components[name] = component
        
    def add(self, name, entity):
        self.components[name].add(entity)
        
    def remove(self, name, entity):
        self.components[name].remove(entity)
        