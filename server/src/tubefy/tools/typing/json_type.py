from typing import Dict
from typing import List
from typing import Type
from typing import Union


JsonType = Union[Dict[str, 'JsonType'], List['JsonType'], int, str, float, bool, Type[None]]
