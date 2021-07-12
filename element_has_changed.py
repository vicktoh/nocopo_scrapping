class element_has_changed(object):
  """An expectation for checking that an element has a particular css class.
  locator - used to find the element
  returns the WebElement once it has the particular css class
  """
  def __init__(self, locator, oldtext):
    self.locator = locator
    self.oldtext = oldtext

  def __call__(self, driver):
    element = driver.find_element(*self.locator)   # Finding the referenced element
    if element.text != self.oldtext:
        return element
    else:
        return False