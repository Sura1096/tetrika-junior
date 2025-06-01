"""
Когда пользователь заходит на страницу урока, мы сохраняем время его захода.
Когда пользователь выходит с урока (или закрывает вкладку, браузер –
в общем как-то разрывает соединение с сервером), мы фиксируем время выхода
с урока. Время присутствия каждого пользователя на уроке хранится у нас
в виде интервалов. В функцию передается словарь, содержащий три списка
с таймстемпами (время в секундах):
lesson – начало и конец урока
pupil – интервалы присутствия ученика
tutor – интервалы присутствия учителя
Интервалы устроены следующим образом – это всегда список из четного
количества элементов. Под четными индексами (начиная с 0) время входа
на урок, под нечетными - время выхода с урока.
Нужно написать функцию appearance, которая получает на вход словарь с
интервалами и возвращает время общего присутствия ученика и учителя на
уроке (в секундах).
"""


def appearance(intervals: dict[str, list[int]]) -> int:
    # Преобразование списка в список пар [вход, выход]
    pupil_intervals = format_intervals(intervals['pupil'])
    tutor_intervals = format_intervals(intervals['tutor'])

    # Проверка интервалов и границ урока
    pupil_intervals = check_intervals(intervals['lesson'], pupil_intervals)
    tutor_intervals = check_intervals(intervals['lesson'], tutor_intervals)

    # Объединение пересекающихся интервалов
    pupil_intervals = merge_intervals(pupil_intervals)
    tutor_intervals = merge_intervals(tutor_intervals)

    # Поиск пересечения между интервалами присутствия ученика и учителя
    interval_intersection = get_intervals_intersection(pupil_intervals, tutor_intervals)

    return get_common_appearance(interval_intersection)


def format_intervals(intervals: list[int]) -> list[list[int]]:
    return [[intervals[i], intervals[i + 1]] for i in range(0, len(intervals), 2)]


def check_intervals(
        lesson_interval: list[int],
        intervals: list[list[int]]
) -> list[list[int]]:
    for i in range(len(intervals)):
        intervals[i][0] = max(intervals[i][0], lesson_interval[0])
        intervals[i][1] = min(intervals[i][1], lesson_interval[1])

    return intervals


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort()
    merged_intervals = [intervals[0]]
    for start, end in intervals[1:]:
        last_start, last_end = merged_intervals[-1]
        if start <= last_end:
            merged_intervals[-1] = [last_start, max(last_end, end)]
        else:
            merged_intervals.append([start, end])

    return merged_intervals


def get_intervals_intersection(
        pupil_intervals: list[list[int]],
        tutor_intervals: list[list[int]]
) -> list[list[int]]:
    intersection = []
    i = j = 0
    while i < len(pupil_intervals) and j < len(tutor_intervals):
        pupil_start_intrvl, pupil_end_intrvl = pupil_intervals[i]
        tutor_start_intrvl, tutor_end_intrvl = tutor_intervals[j]
        start = max(pupil_start_intrvl, tutor_start_intrvl)
        end = min(pupil_end_intrvl, tutor_end_intrvl)
        if start < end:
            intersection.append([start, end])
        if pupil_end_intrvl < tutor_end_intrvl:
            i += 1
        else:
            j += 1
    return intersection


def get_common_appearance(intervals: list[list[int]]) -> int:
    common_time = 0
    for start, end in intervals:
        common_time += end - start
    return common_time
