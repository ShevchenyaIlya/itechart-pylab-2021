from .role import Role


def role_validation(role_name: str) -> bool:
    return role_name in Role.get_roles()
