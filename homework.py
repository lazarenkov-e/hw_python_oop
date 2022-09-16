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
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # длина шага в метрах.
    M_IN_KM = 1000  # коэффициент для перевода значений из километров в метры.
    MIN_IN_H = 60  # коэффициент перевода значений из часов в минуты.

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
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    CAL_MULT_AV_SPEED = 18  # расход калорий при средней скорости.
    SHIFT_AV_SPEED = 20  # сдвиг средней скорости.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.CAL_MULT_AV_SPEED * self.get_mean_speed()
                - self.SHIFT_AV_SPEED
            )
            * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float
    MULT_WEIGHT = 0.035  # множитель веса.
    MULT_CAL = 0.029  # множитель калорий.

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (
                self.MULT_WEIGHT * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.MULT_CAL * self.weight
            )
            * self.duration * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # длина гребка в метрах
    SPEED_SHIFT = 1.1  # сдвиг скорости.
    MULT_CAL = 2  # множитель калорий.

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (
            self.length_pool * self.count_pool
            / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.SPEED_SHIFT)
            * self.MULT_CAL
            * self.weight
        )


WORKOUTS = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking,
}


def read_package(workout_type: str, data: List[float]) -> Training:
    """Прочитать данные полученные от датчиков."""
    try:
        return WORKOUTS[workout_type](*data)
    except (KeyError, TypeError):
        raise ('Неправильные входные данные')


def main(training: Training) -> None:
    """Главная функция.

    Выводит в консоль информацию с рассчетами показателей тренировки:
    длительность, дистанцию, среднюю скорость и количество потраченных калорий.
    """
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
