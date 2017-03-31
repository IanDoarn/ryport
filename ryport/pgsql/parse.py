class Parse:

    def __init__(self, data):
        self.data = data

    def soft_search(self, item):
        results = []
        for row in self.data:
            if row.__contains__(item):
                results.append(row)

        return results

    def filter_data(self, filter_for):
        filter_data = {'rows': []}

        for i in range(len(self.data)):
            row = self.data[i]
            if any(map(lambda item: item in row, filter_for)):
                filter_data['rows'].append({'index': i, 'data': self.data[i]})

        if len(filter_data['rows']) is 0:
            return None, None

        self.data = []
        for row in filter_data['rows']:
            self.data.append(row['data'])

        return filter_data, self.data, len(self.data)
