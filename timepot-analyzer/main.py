import datetime
import itertools
import os


def to_dates_count(x, y):
    return x, len(list(y))


def to_group_counter(x, y):
    groupList = list(y)
    return x, sum(map(lambda x, y: y, groupList))


def group_by_date_and_count(x):
    grouped = itertools.groupby(x, lambda x, _: x)
    return map(lambda x, y: to_group_counter(x, y), grouped)


if __name__ == "__main__":
    aggregates = []
    unzipped = '../../timepot/unzipped/'
    rootPath = '../../logs/'
    for filename in os.listdir(rootPath):
        filepath = rootPath + filename
        f = open(filepath, "r+")
        allLines = f.readlines()
        loggingLevels = ['INFO', 'DEBUG', 'TRACE', 'ERROR']
        filteredLines = []
        parsedDates = []
        for line in allLines:
            if any(line.startswith(x) for x in loggingLevels):
                filteredLines.append(line)
                splittedLine = line.split(None, 3)
                if splittedLine[1] != '' and splittedLine[2] != '':
                    date = splittedLine[1] + splittedLine[2]
                    parsedDate = datetime.datetime.strptime(date, '%Y-%m-%d%H:%M:%S.%f')
                    parsedDates.append(parsedDate)
        grouped = itertools.groupby(parsedDates, lambda x: x.date())
        countOfDay = map(lambda x: to_dates_count(*x), grouped)
        aggregates.append(countOfDay)
    flatten = itertools.chain.from_iterable(aggregates)
    groupedByDate = group_by_date_and_count(flatten)
    # x = matplotlib.dates.date2num([x for (x, y) in groupedByDate])
    # matplotlib.pyplot.plot_date(x, [y for (_, y) in groupedByDate])
    # matplotlib.pyplot.gcf().autofmt_xdate()
    # matplotlib.pyplot.show()
