"""Multi-tenancy support for OCTALUME."""

from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field

from octalume.utils.logging import get_logger

logger = get_logger(__name__)


class TenantRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class TenantSettings(BaseModel):
    compliance_standards: list[str] = Field(default_factory=list)
    allowed_phases: list[int] = Field(default_factory=lambda: list(range(1, 9)))
    max_agents: int = 10
    max_artifacts: int = 1000
    features: dict[str, bool] = Field(
        default_factory=lambda: {
            "mcp_tools": True,
            "web_dashboard": True,
            "compliance_scanning": True,
            "background_jobs": True,
        }
    )


class TenantMember(BaseModel):
    user_id: str
    email: str
    role: TenantRole
    joined_at: datetime = Field(default_factory=datetime.utcnow)


class Tenant(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    slug: str
    description: str | None = None
    settings: TenantSettings = Field(default_factory=TenantSettings)
    members: dict[str, TenantMember] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True


class TenantManager:
    """Manage multiple tenants in OCTALUME."""

    def __init__(self):
        self._tenants: dict[str, Tenant] = {}
        self._slug_index: dict[str, str] = {}

    def create_tenant(
        self,
        name: str,
        slug: str,
        description: str | None = None,
        owner_id: str | None = None,
        owner_email: str | None = None,
        settings: TenantSettings | None = None,
    ) -> Tenant:
        if slug in self._slug_index:
            raise ValueError(f"Tenant with slug '{slug}' already exists")

        tenant = Tenant(
            name=name,
            slug=slug,
            description=description,
            settings=settings or TenantSettings(),
        )

        if owner_id and owner_email:
            tenant.members[owner_id] = TenantMember(
                user_id=owner_id,
                email=owner_email,
                role=TenantRole.OWNER,
            )

        self._tenants[tenant.id] = tenant
        self._slug_index[slug] = tenant.id

        logger.info("tenant_created", tenant_id=tenant.id, slug=slug)
        return tenant

    def get_tenant(self, tenant_id: str) -> Tenant | None:
        return self._tenants.get(tenant_id)

    def get_tenant_by_slug(self, slug: str) -> Tenant | None:
        tenant_id = self._slug_index.get(slug)
        if tenant_id:
            return self._tenants.get(tenant_id)
        return None

    def list_tenants(self, active_only: bool = True) -> list[Tenant]:
        tenants = list(self._tenants.values())
        if active_only:
            tenants = [t for t in tenants if t.is_active]
        return tenants

    def update_tenant(
        self,
        tenant_id: str,
        name: str | None = None,
        description: str | None = None,
        settings: TenantSettings | None = None,
    ) -> Tenant | None:
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            return None

        if name:
            tenant.name = name
        if description is not None:
            tenant.description = description
        if settings:
            tenant.settings = settings

        tenant.updated_at = datetime.utcnow()
        logger.info("tenant_updated", tenant_id=tenant_id)
        return tenant

    def deactivate_tenant(self, tenant_id: str) -> bool:
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            return False

        tenant.is_active = False
        tenant.updated_at = datetime.utcnow()
        logger.info("tenant_deactivated", tenant_id=tenant_id)
        return True

    def add_member(
        self,
        tenant_id: str,
        user_id: str,
        email: str,
        role: TenantRole = TenantRole.MEMBER,
    ) -> TenantMember | None:
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            return None

        if user_id in tenant.members:
            raise ValueError(f"User {user_id} is already a member")

        member = TenantMember(
            user_id=user_id,
            email=email,
            role=role,
        )
        tenant.members[user_id] = member
        tenant.updated_at = datetime.utcnow()

        logger.info("member_added", tenant_id=tenant_id, user_id=user_id, role=role)
        return member

    def remove_member(self, tenant_id: str, user_id: str) -> bool:
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            return False

        if user_id in tenant.members:
            del tenant.members[user_id]
            tenant.updated_at = datetime.utcnow()
            logger.info("member_removed", tenant_id=tenant_id, user_id=user_id)
            return True
        return False

    def update_member_role(
        self,
        tenant_id: str,
        user_id: str,
        new_role: TenantRole,
    ) -> bool:
        tenant = self._tenants.get(tenant_id)
        if not tenant or user_id not in tenant.members:
            return False

        member = tenant.members[user_id]

        if member.role == TenantRole.OWNER:
            owners = [m for m in tenant.members.values() if m.role == TenantRole.OWNER]
            if len(owners) <= 1:
                raise ValueError("Cannot remove the last owner")

        member.role = new_role
        tenant.updated_at = datetime.utcnow()
        logger.info("member_role_updated", tenant_id=tenant_id, user_id=user_id, role=new_role)
        return True

    def get_user_tenants(self, user_id: str) -> list[Tenant]:
        return [
            tenant
            for tenant in self._tenants.values()
            if user_id in tenant.members and tenant.is_active
        ]

    def check_permission(
        self,
        tenant_id: str,
        user_id: str,
        permission: str,
    ) -> bool:
        tenant = self._tenants.get(tenant_id)
        if not tenant:
            return False

        member = tenant.members.get(user_id)
        if not member:
            return False

        role_permissions = {
            TenantRole.OWNER: ["read", "write", "delete", "admin", "manage_members"],
            TenantRole.ADMIN: ["read", "write", "delete", "admin"],
            TenantRole.MEMBER: ["read", "write"],
            TenantRole.VIEWER: ["read"],
        }

        return permission in role_permissions.get(member.role, [])


tenant_manager = TenantManager()
