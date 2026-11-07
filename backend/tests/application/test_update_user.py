import pytest

from app.application.use_cases.update_user import UpdateUserUseCase
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRole

from tests.fakes.fake_audit_log_repository import (
    FakeAuditLogRepository,
)
from app.domain.entities.audit_action import AuditAction
from app.domain.entities.audit_result import AuditResult


class FakeUserRepository:

    def __init__(self, users=None):
        self.users = users or []

    def get_by_id(self, user_id):
        return next(
            (
                user
                for user in self.users
                if user.id == user_id
            ),
            None,
        )

    def get_by_email(self, email):
        return next(
            (
                user
                for user in self.users
                if user.email == email
            ),
            None,
        )

    def update(self, user):
        return user

    def update_without_commit(self, user):
        return self.update(user)

class FakeUnitOfWork:
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def commit(self):
        self.committed = True

    def rollback(self):
        self.rolled_back = True

def test_update_user_successfully():

    existing_user = User(
        id=1,
        name="Old Name",
        email="old@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
    )

    user_repository = FakeUserRepository(
        users=[existing_user],
    )

    use_case = UpdateUserUseCase(
        user_repository=user_repository,
        audit_log_repository=FakeAuditLogRepository(),
        unit_of_work=FakeUnitOfWork(),
    )

    result = use_case.execute(
        user_id=1,
        name="Updated Name",
        email="updated@test.com",
        role=UserRole.INVENTORY_OPERATOR,
        updated_by_user_id=10,
    )

    assert result.id == 1
    assert result.name == "Updated Name"
    assert result.email == "updated@test.com"
    assert result.role == UserRole.INVENTORY_OPERATOR
    assert result.hashed_password == "hashed_password"
    assert result.is_active is True

def test_update_user_not_found():

    user_repository = FakeUserRepository()

    use_case = UpdateUserUseCase(
        user_repository=user_repository,
        audit_log_repository=FakeAuditLogRepository(),
        unit_of_work=FakeUnitOfWork(),
    )

    with pytest.raises(
        ValueError,
        match="User not found",
    ):
        use_case.execute(
            user_id=999,
            name="Updated Name",
            email="updated@test.com",
            role=UserRole.SELLER,
            updated_by_user_id=10,
        )

def test_update_user_email_already_exists():

    first_user = User(
        id=1,
        name="First User",
        email="first@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
    )

    second_user = User(
        id=2,
        name="Second User",
        email="second@test.com",
        hashed_password="hashed_password",
        role=UserRole.INVENTORY_OPERATOR,
    )

    user_repository = FakeUserRepository(
        users=[first_user, second_user],
    )

    use_case = UpdateUserUseCase(
        user_repository=user_repository,
        audit_log_repository=FakeAuditLogRepository(),
        unit_of_work=FakeUnitOfWork(),
    )

    with pytest.raises(
        ValueError,
        match="Email already registered",
    ):
        use_case.execute(
            user_id=2,
            name="Second User",
            email="first@test.com",
            role=UserRole.INVENTORY_OPERATOR,
            updated_by_user_id=10,
        )

def test_update_user_registers_audit_log():
    # Arrange
    existing_user = User(
        id=1,
        name="Old Name",
        email="old@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
    )

    user_repository = FakeUserRepository(
        users=[existing_user],
    )
    audit_log_repository = FakeAuditLogRepository()
    unit_of_work = FakeUnitOfWork()

    use_case = UpdateUserUseCase(
        user_repository=user_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    result = use_case.execute(
        user_id=1,
        name="Updated Name",
        email="updated@test.com",
        role=UserRole.INVENTORY_OPERATOR,
        updated_by_user_id=10,
    )

    # Assert
    assert result.id == 1
    assert result.name == "Updated Name"
    assert result.role == UserRole.INVENTORY_OPERATOR

    assert len(audit_log_repository.audit_logs) == 1

    audit_log = audit_log_repository.audit_logs[0]

    assert audit_log.user_id == 10
    assert audit_log.action == AuditAction.UPDATE
    assert audit_log.entity_type == "user"
    assert audit_log.entity_id == "1"
    assert audit_log.result == AuditResult.SUCCESS

    assert audit_log.old_values == {
        "name": "Old Name",
        "role": UserRole.SELLER.value,
    }

    assert audit_log.new_values == {
        "name": "Updated Name",
        "role": UserRole.INVENTORY_OPERATOR.value,
    }

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False

    # Sensitive information must not be audited
    for values in (
        audit_log.old_values,
        audit_log.new_values,
    ):
        assert "password" not in values
        assert "hashed_password" not in values
        assert "email" not in values
