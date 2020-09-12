import mido
import math
from random import random
# python3 -m pip install mido

def rand_adjustment(gap, cumulative_adjustment):
    prob_no_adj = 0.6
    prob_no_adj = 0.1
    if random() < prob_no_adj:
        return 0
    # print(gap)
    adj = int(math.log(1 + random() * gap, 10))
    if random() < 0.5 and gap > 0:
        adj *= -1
    # adj += gap / 2
    # print(gap, adj)
    return adj

def get_adj(times, adjustments):
    # times is list of actual times
    # is adjustments, a dict of actual times
    cumulative_adj = 0
    track_adjustments = []
    # print(adjustments)
    for x in times:
        # print(len(adjustments), x, cumulative_adj,
                # adjustments[x])
        adj = adjustments[x] - cumulative_adj
        cumulative_adj += adj
        track_adjustments.append(adj)
    return track_adjustments

def main2():
    print(rand_adjustment(1, 0))
    print(rand_adjustment(1, 0))
    print(rand_adjustment(1, 0))
    print(rand_adjustment(1, 0))
    print(rand_adjustment(1, 0))
    print(rand_adjustment(5, 0))
    print(rand_adjustment(5, 0))
    print(rand_adjustment(5, 0))
    print(rand_adjustment(5, 0))
    print(rand_adjustment(5, 0))
    print(rand_adjustment(10, 0))
    print(rand_adjustment(10, 0))
    print(rand_adjustment(10, 0))
    print(rand_adjustment(10, 0))
    print(rand_adjustment(10, 0))

def main():
    filename = 'test.midi'
    mid = mido.MidiFile(filename)
    # print(mid.ticks_per_beat) # 384

    actual_times = []
    for track, messages in enumerate(mid.tracks):
        t = 0
        actual_time = []
        for m in messages:
            t += m.time
            actual_time.append(t)
        actual_times.append(actual_time)
    distinct_times = set()
    for ts in actual_times:
        distinct_times = distinct_times.union(ts)
    distinct_times = sorted(list(distinct_times))

    cumulative_adjustment = 0
    adjustments = {}
    for i in range(0, len(distinct_times)):
        t = distinct_times[i]
        if i == 0:
            adjustments[t] = 0
            continue
        if i < len(distinct_times) - 1:
            gap = min(
                distinct_times[i + 1] - distinct_times[i],
                distinct_times[i] - distinct_times[i - 1] - cumulative_adjustment
            )
        else:
            gap = distinct_times[i] - distinct_times[i - 1] - cumulative_adjustment

        adjustments[t] = rand_adjustment(
            gap,
            cumulative_adjustment
        )
        cumulative_adjustment += adjustments[t]
        print(gap, adjustments[t], cumulative_adjustment)

    # for m in mid.tracks[1][10:40]:
        # print(m.time)
    for track, messages in enumerate(mid.tracks):
        # for z in actual_times[track]:
            # print(z)
        msg_adjustments = get_adj(actual_times[track], adjustments)
        for i, m in enumerate(messages):
            # print(m.time, m.time + msg_adjustments[i])
            m.time += msg_adjustments[i]
    # print('after')
    # for m in mid.tracks[1][10:40]:
        # print(m.time)
    mid.save('test_new.mid')

main()
