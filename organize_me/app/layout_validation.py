from functools import wraps
from typing import Any

# TODO: change the typehints to be more specific for the validation functions prototypes


def validate_table_exists(func: Any) -> Any:
    """Ensure that the table exists and is not None."""
    @wraps(func)
    def wrapper(instance: Any, *args: Any, **kwargs: Any) -> Any:
        if not instance.table:
            raise ValueError("No table available. Cannot perform action on None or uninitialized table.")
        return func(instance, *args, **kwargs)
    return wrapper


def validate_table_not_empty(func: Any) -> Any:
    """Ensure that the table has data (is not empty) before performing an action."""
    @wraps(func)
    def wrapper(instance: Any, *args: Any, **kwargs: Any) -> Any:
        if not instance.table.rows:
            raise ValueError("Table is empty. Cannot perform action on empty data.")
        return func(instance, *args, **kwargs)
    return wrapper


def validate_item_exists(func: Any) -> Any:
    """Ensure that an item is provided with a valid ID."""
    @wraps(func)
    def wrapper(instance: Any, *args: Any, **kwargs: Any) -> Any:
        item = args[0]
        if not item:
            raise ValueError("No item provided. Cannot act on None item.")
        if item.get("id") is None:
            raise ValueError("No item ID provided. Cannot act on item with None ID.")
        return func(instance, *args, **kwargs)
    return wrapper


def safe_action(func: Any) -> Any:
    """Ensure that the action is performed safely."""
    @wraps(func)
    def wrapper(instance: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            return func(instance, *args, **kwargs)
        except Exception as e:
            instance.update_label_status(f"Error: {e}")
    return wrapper
