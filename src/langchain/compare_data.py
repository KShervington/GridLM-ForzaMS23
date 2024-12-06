def compare_telemetry(driver_data, baseline_data):

    def calculate_percentage_delta(baseline, driver):
        deltas = []
        for b, d in zip(baseline, driver):
            if b != 0:
                delta = ((d - b) / b) * 100
                if delta > 0:
                    deltas.append(f"{int(delta)}% higher")
                elif delta < 0:
                    deltas.append(f"{int(abs(delta))}% lower")
                else:
                    deltas.append("identical")
            else:
                # Handling case where baseline value is zero (avoid division by zero)
                if d != 0:
                    deltas.append(f"{round(d, 2)} higher")
                else:
                    deltas.append("identical")
        return deltas

    def compare_most_common_gears(baseline, driver):
        gear_deltas = []
        for b, d in zip(baseline, driver):
            if b == d:
                gear_deltas.append("identical")
            elif b < d:
                gear_deltas.append(f"{int(d - b)} gear(s) higher")
            else:
                gear_deltas.append(f"{int(b - d)} gear(s) lower")
        return gear_deltas

    comparison = {}

    for segment_num, driver_metrics in driver_data["segments"].items():
        if segment_num in baseline_data["segments"]:
            baseline_metrics = baseline_data["segments"][segment_num]

            seg_name = f'Segment {segment_num}'

            comparison[seg_name] = {
                "avg_speed_delta_over_time": calculate_percentage_delta(
                    baseline_metrics["avg_speed_over_time"], driver_metrics["avg_speed_over_time"]
                ),
                "avg_acceleration_delta_over_time": calculate_percentage_delta(
                    baseline_metrics["avg_acceleration_over_time"], driver_metrics["avg_acceleration_over_time"]
                ),
                "avg_brake_pressure_delta_over_time": calculate_percentage_delta(
                    baseline_metrics["avg_brake_pressure_over_time"], driver_metrics["avg_brake_pressure_over_time"]
                ),
                "avg_throttle_percentage_delta_over_time": calculate_percentage_delta(
                    baseline_metrics["avg_throttle_percentage_over_time"], driver_metrics["avg_throttle_percentage_over_time"]
                ),
                "most_common_gear_delta_over_time": compare_most_common_gears(
                    baseline_metrics["most_common_gear_values_over_time"], driver_metrics["most_common_gear_values_over_time"]
                ),
            }

            for attr, value in comparison[seg_name].items():
                comparison[seg_name][attr] = ', '.join([f"{val}" for val in value])

    return comparison
