from functools import wraps
import inspect
from typing import Any, Callable, get_type_hints

from pydantic import create_model


# TODO: check reddit post
def function(f: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    # Extract annotations and defaults
    annotations = get_type_hints(f)
    defaults = dict(inspect.signature(f).parameters)

    fields_dict = {}
    for name, type_ in annotations.items():
        default_value = (
            defaults[name].default
            if defaults[name].default != inspect.Parameter.empty
            else None
        )
        fields_dict[name] = (type_, default_value)

    input_model = create_model(f"InputModel_{f.__name__}", **fields_dict)

    # Generate JSON schema
    schema = input_model.model_json_schema()

    # Attach metadata to the wrapper function
    wrapper.schema = dict(name=f.__name__, description=f.__doc__, parameters=schema)

    return wrapper
