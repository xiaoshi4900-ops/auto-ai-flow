from app.db.models.user import User, RefreshToken


def test_user_create(db):
    user = User(username="testuser", email="test@example.com", hashed_password="hashed")
    db.add(user)
    db.commit()
    assert user.id is not None
    assert user.username == "testuser"
    assert user.is_active is True


def test_user_email_unique(db):
    user1 = User(username="user1", email="same@example.com", hashed_password="h1")
    db.add(user1)
    db.commit()
    user2 = User(username="user2", email="same@example.com", hashed_password="h2")
    db.add(user2)
    from sqlalchemy.exc import IntegrityError
    try:
        db.commit()
        assert False, "Should have raised IntegrityError"
    except IntegrityError:
        db.rollback()


def test_refresh_token_association(db):
    user = User(username="tokenuser", email="token@example.com", hashed_password="h")
    db.add(user)
    db.commit()
    token = RefreshToken(token="rt_abc123", user_id=user.id)
    db.add(token)
    db.commit()
    assert token.id is not None
    assert token.user_id == user.id
    assert token.is_revoked is False


def test_refresh_token_cascade(db):
    user = User(username="cascadeuser", email="cascade@example.com", hashed_password="h")
    db.add(user)
    db.commit()
    token = RefreshToken(token="rt_cascade", user_id=user.id)
    db.add(token)
    db.commit()
    db.delete(user)
    db.commit()
    remaining = db.query(RefreshToken).filter(RefreshToken.token == "rt_cascade").first()
    assert remaining is None
