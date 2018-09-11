from exceptions import ElementNotFound


def get_element_by(by, element_id, from_item):
    elements = from_item.find_elements(by, element_id)
    size = len(elements)

    if size > 0:
        return elements[0]
    else:
        raise ElementNotFound()


def get_elements_by(by, element_id, from_item):
    elements = from_item.find_elements(by, element_id)
    return elements
