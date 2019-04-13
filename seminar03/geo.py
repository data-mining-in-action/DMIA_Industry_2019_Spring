import numpy as np

EARTH_RADIUS = 6372795.0


def earth_distance(lon1, lat1, lon2, lat2, is_radians=False):
    """
    Вычисление расстояния между точками заданными географическими координатами
    Если входные пареметры массивы, то возвращается расстояния первый с
    первым и тд
    :param lon1: float or np.array
    :param lat1: float or np.array
    :param lon2: float or np.array
    :param lat2: float or np.array
    :param is_radians: bool - переданны ли координаты в радианах
    :return: float or np.array
    """
    # конвертируем в радианы
    if not is_radians:
        lon1, lat1, lon2, lat2 = map(np.radians, (lon1, lat1, lon2, lat2))
    return EARTH_RADIUS * 2. * np.arcsin(np.sqrt(
        np.sin((lat2 - lat1) / 2.) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(
            (lon2 - lon1) / 2.) ** 2))
