from uuid import UUID


def custom_serializer(obj):
    if isinstance(obj, UUID):
        return str(obj)
    if hasattr(obj, "__dict__"):
        return obj.__dict__
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
