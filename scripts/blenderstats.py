import click
import statistics
import math
import random

@click.command()
@click.argument("results")
@click.option("--probs", default=0)
def run_stats(results, probs):
    times = []
    with open(results) as f:
        for line in f:
            result = line.split(" ")[2]
            times.append(__str_to_time(result))

    n = len(times)
    if probs == 0:
        probs = len(times)
    times = random.sample(times, probs)
    mean = statistics.mean(times)
    print "PROBS: {}".format(len(times))
    print "ESTM_TIME: {} ({})".format(__time_to_str(n*mean), n*mean)
    print "MEAN: {} ({})".format(__time_to_str(mean), mean)
    print "DEVIATION: {} ({})".format(__time_to_str(statistics.stdev(times)), statistics.stdev(times))
    print "VARIANCE: {} ({})".format(__time_to_str(statistics.variance(times)), statistics.variance(times))


def __str_to_time(result):
    time_ = result.split(":")
    return float(time_[0]*60) + float(time_[1])


def __time_to_str(time_):
    return "{0}:{1:08.5f}".format(int(math.floor(time_ / 60)), time_ % 60)


if __name__ == "__main__":
    run_stats()