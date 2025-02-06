def seconds_to_days_hours(seconds: float) -> str:
    if not seconds:
        return "Немає даних для розрахунку"

    days = int(seconds // 86400)
    remaining_seconds = seconds % 86400
    hours = int(remaining_seconds // 3600)

    if days == 1:
        day_str = "день"
    elif 2 <= days <= 4:
        day_str = "дні"
    else:
        day_str = "днів"

    if hours == 1:
        hour_str = "година"
    elif 2 <= hours <= 4:
        hour_str = "години"
    else:
        hour_str = "годин"

    return f"{days} {day_str} {hours} {hour_str}"
