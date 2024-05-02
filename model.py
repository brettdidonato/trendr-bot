class Model:
  """A machine learning model."""
  def __init__(
      self,
      model_family: str,
      model_version: str,
      service: str,
      **kwargs):
    """Initilize Model objects.

    Args:
      model_family: The family name e.g. "Gemini".
      model_version: The model version e.g. "gemini-1.5-pro-preview-0409".
      service: The hosting service e.g. "Google Cloud".

    Returns:
      Model object.

    """
    self.model_family = model_family
    self.model_version = model_version
    self.service = service
    self.attributes = kwargs

  def __repr__(self):
    attributes_str = ", ".join(f"{k}={v}" for k, v in self.attributes.items())
    return f"Model(model_family='{self.model_family}', model_version='{self.model_version}', service='{self.service}' {attributes_str})"