
class Printer:
    @staticmethod
    def print_times(TimeObject, now):
        t = TimeObject
        print(
            "now: {n}\t last_midnight: {lm}\t midnight: {m}\t sunrise: {sr}\t \
                sunset: {ss}\t".format(
                n=now, lm=t.last_midnight, m=t.midnight, sr=t.sunrise, ss=t.sunset
            )
        )