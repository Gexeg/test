def calculate_percentile(sorted_values: list[int], percentile_value: int):
    if not sorted_values:
        raise ValueError("The input list is empty")

    sorted_values.sort()
    position = (percentile_value / 100) * (len(sorted_values) - 1)
    lower_bound_index = int(position)
    upper_bound_index = min(lower_bound_index + 1, len(sorted_values) - 1)
    interpolation_weight = position - lower_bound_index

    return (
        sorted_values[lower_bound_index] * (1 - interpolation_weight)
        + sorted_values[upper_bound_index] * interpolation_weight
    )
