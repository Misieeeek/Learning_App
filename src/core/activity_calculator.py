from datetime import datetime, timedelta


class Activity_Calculator:
    def __init__(self):
        pass

    def calculate_date_to_hours(self, data):
        intervals = self.get_intervals(data)
        daily_hours = {}

        for start_str, end_str in intervals:
            start = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S")

            if end <= start:
                continue

            current_start = start

            while current_start.date() < end.date():
                end_of_day = datetime.combine(
                    current_start.date(), datetime.max.time()
                ).replace(microsecond=0)
                duration = (end_of_day - current_start).total_seconds() / 3600.0

                day_str = current_start.strftime("%Y-%m-%d")
                daily_hours[day_str] = daily_hours.get(day_str, 0) + duration

                current_start = end_of_day + timedelta(seconds=1)

            day_str = end.strftime("%Y-%m-%d")
            duration = (end - current_start).total_seconds() / 3600.0
            daily_hours[day_str] = daily_hours.get(day_str, 0) + duration

        sorted_days = sorted(daily_hours.keys())
        hours_list = [daily_hours[day] for day in sorted_days]
        return hours_list

    def get_intervals(self, data):
        intervals = []
        for day_item in data:
            if day_item == 0.0:
                continue
            intervals.extend(day_item)

        return intervals
