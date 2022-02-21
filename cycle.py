#! /usr/bin/env python3
""" Utility for simple cycle tracking."""
extended_description = """
When used without arguments, it will display the number of days since the last recorded cycle start (CD).
Can be used to record a cycle start day (-s/--start) or give the likely next cycle start days (-p/--plan).
Requires the Arrow Python module.
"""

from os import path
from json import load
from argparse import ArgumentParser
import arrow

parser = ArgumentParser(__doc__)
parser.add_argument('-s', '--start', nargs='?', type=int, const=0, metavar='N', help='start new cycle; optionally N days ago.')
parser.add_argument('-p', '--plan', action='store_true', help='display likely start days for the next cycle')
commands = parser.parse_args()

with open (path.expanduser('~/.cycle/cycle_config.json')) as configfile:
    config = load(configfile)

today = arrow.now()

def get_answer(question, possible_answers):
    answer = input(question).upper()
    if answer in possible_answers:
        return answer
    else:
        print('Answer {} is not a valid option. Please answer one of '.format(answer), possible_answers)
        return get_answer(question, possible_answers)


def confirm_date(today, shiftval):
    startday = today.shift(days=-shiftval)
    print('registering new cycle at', startday.humanize(locale=config['locale'])+':', startday.format('dddd Do MMMM, YYYY', locale=config['locale']))
    answer = get_answer('(C)ontinue, (M)odify, (A)bort?', ['C', 'M', 'A'])
    if answer == 'C':
        return startday
    elif answer == 'M':
        new_shift = int(input('Give new day difference:'))
        return confirm_date(today, new_shift)
    elif answer == 'A':
        print('No change made.')
        exit()
    else:
        #We should never get here
        raise ValueError('Impossible answer: {}'.format(answer))


if commands.start is None:
    # we are displaying information. Open file for reading.
    with open(path.expanduser(config['cycles_file'])) as data:
        cycles = data.readlines()
        startday = arrow.get(cycles[-1])
        cycle_day = (today - startday).days + 1
        if commands.plan:
            print('Today is {}; cycle day {}.'.format(today.format('dddd Do MMMM, YYYY', locale=config['locale']), cycle_day))
            next_start = startday.shift(days = config['avg_cycle_length'])
            verb = 'is'
            if next_start < today:
                verb = 'was'
            print('Next cycle {} expected on CD {}: {}, {}'.format(verb,
                                                                   config['avg_cycle_length']+1,
                                                                   next_start.format('dddd Do MMMM, YYYY', locale=config['locale']),
                                                                   next_start.humanize(locale=config['locale'])))
        else:
            print('CD: {}'.format(cycle_day))
else:
    # we are modifying information. Open file for writing.
    with open(path.expanduser(config['cycles_file']), 'a') as data:
        startday = confirm_date(today, commands.start)
        print(startday.format('YYYY-MM-DD'), file=data)
