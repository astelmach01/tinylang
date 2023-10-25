import inspect
from typing import Any, Callable, Dict, get_type_hints

from pydantic import create_model


def function(f: Callable[..., Any]) -> Dict[str, Any]:
    # Extract annotations and defaults
    annotations = get_type_hints(f)
    defaults = dict(inspect.signature(f).parameters)

    fields_dict = {}
    for name, type_ in annotations.items():
        default_value = (
            defaults[name].default
            if defaults[name].default != inspect.Parameter.empty
            else ...
        )
        fields_dict[name] = (type_, default_value)

    input_model = create_model(f"InputModel_{f.__name__}", **fields_dict)  # type: ignore

    # Generate JSON schema
    schema = input_model.model_json_schema()

    # Remove titles from properties
    for prop in schema["properties"]:
        schema["properties"][prop].pop("title", None)

    # Remove top-level title
    schema.pop("title", None)

    return dict(name=f.__name__, description=f.__doc__, parameters=schema)
