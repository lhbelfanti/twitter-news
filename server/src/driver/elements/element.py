class Element(object):
    def __init__(self, element, driver, tag=""):
        self.element = element
        self.driver = driver
        self.tag = tag if tag != "" else element.tag_name
