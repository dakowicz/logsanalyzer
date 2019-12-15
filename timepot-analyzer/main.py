import datetime
import itertools
import os

import matplotlib.dates
import matplotlib.pyplot


def processFile(filepath):
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
                # print parsedDate
                parsedDates.append(parsedDate)
    grouped = itertools.groupby(parsedDates, lambda x: x.date())
    return map(lambda (x, y): (x, len(list(y))), grouped)


def to_group_counter(x, y):
    groupList = list(y)
    print groupList
    return x, sum(map(lambda (x, y): y, groupList))


def group_by_date_and_count():
    grouped = itertools.groupby(flatten, lambda (x, _): x)
    return map(lambda (x, y): to_group_counter(x, y), grouped)


if __name__ == "__main__":
    aggregates = []
    unzipped = '../../timepot/unzipped/'
    for filename in os.listdir('../logs'):
        countOfDay = processFile('../logs/' + filename)
        aggregates.append(countOfDay)
    flatten = list(itertools.chain.from_iterable(aggregates))
    groupedByDate = group_by_date_and_count()
    x = matplotlib.dates.date2num([x for (x, y) in groupedByDate])
    matplotlib.pyplot.plot_date(x, [y for (_, y) in groupedByDate])
    matplotlib.pyplot.gcf().autofmt_xdate()
    matplotlib.pyplot.show()
