def find_json_strings(data):
        json_strings = []
        start = data.find('{')
        while start != -1:
            counter = 1
            end = start + 1
            while counter > 0 and end < len(data):
                if data[end] == '{':
                    counter += 1
                elif data[end] == '}':
                    counter -= 1
                end += 1
            if counter == 0:
                json_strings.append(data[start:end])
            start = data.find('{', end)
        return json_strings