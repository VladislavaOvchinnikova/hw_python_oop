class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        print(f'Тип тренировки: {self.training_type}; Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км; Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    def __init__(self, action: int, duration: float, weight: float,) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight  
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.distance,
                           self.speed,
                           self.calories)


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        spent_calories = ((coeff_calorie_1 * self.get_mean_speed()
                         - coeff_calorie_2) * self.weight
                         / self.M_IN_KM * self.duration)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float, weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    def get_spent_calories(self) -> float:
        duration_in_min = self.duration * 60
        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029
        spent_calorie = ((coeff_calorie_1 * self.weight
                         + (self.get_mean_speed()**2 // self.height)
                         * coeff_calorie_2 * self.weight)
                         * duration_in_min)
        return spent_calorie

class Swimming(Training):
    """Тренировка: плавание."""
    def __init__(self, action: int, duration: float, weight: float, length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool
    LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        mean_speed = (self.lenght_pool * self.count_pool
                    /self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        spent_calories = (self.get_mean_speed() + coeff_calorie_1) * coeff_calorie_2 * self.weight
        return spent_calories

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_dict = {
        'SWN' : Swimming,
        'RUN' : Running,
        'WLK' : SportsWalking
    }
    if training_dict[workout_type] == Swimming:
        training = Swimming(*data)
    elif training_dict[workout_type] == Running:
        training = Running(*data)
    elif training_dict[workout_type] == SportsWalking:
        training = SportsWalking(*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

