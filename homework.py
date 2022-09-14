from dataclasses import dataclass
from typing import List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки.
    LEN_STEP - длина шага в метрах.
    M_IN_KM - константа перевода значений из метров в километры.
    M_IN_H - константа: количество минут в 1 часе.
    """

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60
    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            "Необходимо переопределить метод get_spent_calories()!")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    COEFF_CAL_RUN_1 = 18
    COEFF_CAL__RUN_2 = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CAL_RUN_1 * self.get_mean_speed()
                - self.COEFF_CAL__RUN_2)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float
    COEFF_CAL_WLK_1 = 0.035
    COEFF_CAL_WLK_2 = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.COEFF_CAL_WLK_1 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.COEFF_CAL_WLK_2 * self.weight)
                * self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """
    Тренировка: плавание.
    Для Класса Swimming константа LEN_STEP обозначает длину гребка в метрах.
    """

    LEN_STEP = 1.38
    length_pool: float
    count_pool: int
    COEFF_CAL_SWM_1 = 1.1
    COEFF_CAL_SWM_2 = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.get_mean_speed()
                + self.COEFF_CAL_SWM_1) * self.COEFF_CAL_SWM_2 * self.weight)


WORKOUT = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    return WORKOUT[workout_type](*data)


def main(training: Training) -> None:
    print(training.show_training_info().get_message())  # noqa: T201


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
