import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends  # type: ignore


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends = get_friends(user_id, fields=["bdate"]).items
    current_date = dt.datetime.now()
    current_year = current_date.year
    ages = []
    for friend in friends:
        if "bdate" in friend and len(friend["bdate"]) >= 9:  # type: ignore
            bdate = friend["bdate"]  # type: ignore
            byear = int(bdate[-4:])
            ages.append(current_year - byear)
    median_age = statistics.median(ages) if ages else None
    return median_age


if __name__ == "__main__":
    print(age_predict(189183825))
