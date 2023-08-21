from haversine import haversine, Unit


class DistanceService:

    @classmethod
    def get_address(cls, point: dict) -> str:
        return "Some address..."

    @classmethod
    def calc_links(cls, data: list[dict]) -> dict:
        links = {}
        n = len(data)
        for i in range(n):
            p1 = data[i]
            for j in range(i+1, n):
                p2 = data[j]
                key_inverted = p2['point'], p1['point']
                if key_inverted not in links:
                    key = p1['point'], p2['point']
                    links[key] = links.get(key) or int(haversine(
                        (p1['latitude'], p1['longitude']),
                        (p2['latitude'], p2['longitude']),
                        unit=Unit.METERS
                    ))
        return links

    @classmethod
    def calc_distinct_links(cls, data: list[dict]) -> dict:
        distinct = {row['point']: row for row in data}
        rows = cls.calc_links(list(distinct.values()))

        return {
            'points': [{'name': point, 'address': cls.get_address(d)} for point, d in rows.items()],
            'links': [{'name': "".join(point), 'distance': d} for point, d in rows.items()],
        }
