import pytest
from sqlalchemy.orm import exc

from .models import User

pytestmark = pytest.mark.asyncio


# noinspection PyUnusedLocal
async def test_one(bind, random_name):
    user = await User.create(nickname=random_name)
    u = await User.query.where(User.nickname == random_name).gino.one()
    assert (user.id == u.id)
    with pytest.raises(exc.NoResultFound):
        await User.query.where(User.nickname == random_name*2).gino.one()
    await User.create(nickname=random_name)
    with pytest.raises(exc.MultipleResultsFound):
        await User.query.where(User.nickname == random_name).gino.one()


# noinspection PyUnusedLocal
async def test_one_or_none(bind, random_name):
    user = await User.create(nickname=random_name)
    u = await User.query.where(User.nickname == random_name).gino.one_or_none()
    assert (user.id == u.id)
    u = await User.query.where(
        User.nickname == random_name*2).gino.one_or_none()
    assert(u is None)
    await User.create(nickname=random_name)
    with pytest.raises(exc.MultipleResultsFound):
        await User.query.where(User.nickname == random_name).gino.one_or_none()
