from enum import Enum


class UserRole(str, Enum):
    ADMIN = "Admin"
    DATA_MANAGER = "Data Manager"
    VIEWER = "Viewer"


ROLE_PERMISSIONS = {
    UserRole.ADMIN: ["create", "read", "update", "delete", "manage_users"],
    UserRole.DATA_MANAGER: ["create", "read", "update"],
    UserRole.VIEWER: ["read"],
}
