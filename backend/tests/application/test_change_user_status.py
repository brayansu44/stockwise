import pytest

from app.application.use_cases.change_user_status import ChangeUserStatusUseCase
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

def test_deactivate_user_successfully():

    user = User(
        id=1,
        name="Seller User",
        email="seller@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
        is_active=True,
    )

    user_repository = FakeUserRepository(
        users=[user],
    )

    use_case = ChangeUserStatusUseCase(
        user_repository=user_repository,
        audit_log_repository=FakeAuditLogRepository(),
        unit_of_work=FakeUnitOfWork(),
    )

    result = use_case.execute(
        user_id=1,
        is_active=False,
        changed_by_user_id=10,
    )

    assert result.id == 1
    assert result.is_active is False

def test_activate_user_successfully():

    user = User(
        id=1,
        name="Seller User",
        email="seller@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
        is_active=False,
    )

    user_repository = FakeUserRepository(
        users=[user],
    )

    use_case = ChangeUserStatusUseCase(
        user_repository=user_repository,
        audit_log_repository=FakeAuditLogRepository(),
        unit_of_work=FakeUnitOfWork(),
    )

    result = use_case.execute(
        user_id=1,
        is_active=True,
        changed_by_user_id=10,
    )

    assert result.id == 1
    assert result.is_active is True

def test_change_user_status_not_found():

    user_repository = FakeUserRepository()

    use_case = ChangeUserStatusUseCase(
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
            is_active=False,
            changed_by_user_id=10,
        )

def test_deactivate_user_registers_audit_log():
    # Arrange
    user = User(
        id=1,
        name="Seller User",
        email="seller@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
        is_active=True,
    )

    user_repository = FakeUserRepository(users=[user])
    audit_log_repository = FakeAuditLogRepository()
    unit_of_work = FakeUnitOfWork()

    use_case = ChangeUserStatusUseCase(
        user_repository=user_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    result = use_case.execute(
        user_id=1,
        is_active=False,
        changed_by_user_id=10,
    )

    # Assert
    assert result.is_active is False
    assert len(audit_log_repository.audit_logs) == 1

    audit_log = audit_log_repository.audit_logs[0]

    assert audit_log.user_id == 10
    assert audit_log.action == AuditAction.DEACTIVATE
    assert audit_log.entity_type == "user"
    assert audit_log.entity_id == "1"
    assert audit_log.result == AuditResult.SUCCESS

    assert audit_log.old_values == {
        "is_active": True,
    }

    assert audit_log.new_values == {
        "is_active": False,
    }

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False

def test_activate_user_registers_audit_log():
    # Arrange
    user = User(
        id=1,
        name="Seller User",
        email="seller@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
        is_active=False,
    )

    user_repository = FakeUserRepository(users=[user])
    audit_log_repository = FakeAuditLogRepository()
    unit_of_work = FakeUnitOfWork()

    use_case = ChangeUserStatusUseCase(
        user_repository=user_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    result = use_case.execute(
        user_id=1,
        is_active=True,
        changed_by_user_id=10,
    )

    # Assert
    assert result.is_active is True
    assert len(audit_log_repository.audit_logs) == 1

    audit_log = audit_log_repository.audit_logs[0]

    assert audit_log.user_id == 10
    assert audit_log.action == AuditAction.ACTIVATE
    assert audit_log.entity_type == "user"
    assert audit_log.entity_id == "1"
    assert audit_log.result == AuditResult.SUCCESS

    assert audit_log.old_values == {
        "is_active": False,
    }

    assert audit_log.new_values == {
        "is_active": True,
    }

    assert unit_of_work.committed is True
    assert unit_of_work.rolled_back is False

@pytest.mark.parametrize(
    "initial_status, requested_status",
    [
        (True, True),
        (False, False),
    ],
)
def test_change_user_status_rejects_unchanged_status(
    initial_status,
    requested_status,
):
    # Arrange
    user = User(
        id=1,
        name="Seller User",
        email="seller@test.com",
        hashed_password="hashed_password",
        role=UserRole.SELLER,
        is_active=initial_status,
    )

    user_repository = FakeUserRepository(users=[user])
    audit_log_repository = FakeAuditLogRepository()
    unit_of_work = FakeUnitOfWork()

    use_case = ChangeUserStatusUseCase(
        user_repository=user_repository,
        audit_log_repository=audit_log_repository,
        unit_of_work=unit_of_work,
    )

    # Act
    with pytest.raises(
        ValueError,
        match="User already has the requested status",
    ):
        use_case.execute(
            user_id=1,
            is_active=requested_status,
            changed_by_user_id=10,
        )

    # Assert
    assert user.is_active == initial_status
    assert audit_log_repository.audit_logs == []
    assert unit_of_work.committed is False
    assert unit_of_work.rolled_back is False
