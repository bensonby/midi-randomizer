import mido
import math
from random import random
# python3 -m pip install mido

def rand_adjustment(gap):
    prob_no_adj = 0.3
    if random() < prob_no_adj:
        return 0
    half_width = min(gap / 12, 90)
    adj = round(random() * half_width * 2 - half_width)
    return adj

def get_adj(times, adjustments):
    # times is list of actual times
    # is adjustments, a dict of actual times
    cumulative_adj = 0
    track_adjustments = []
    for x in times:
        adj = adjustments[x] - cumulative_adj
        cumulative_adj += adj
        track_adjustments.append(adj)
    return track_adjustments

def main():
    filename = 'test2.midi'
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
                distinct_times[i] - distinct_times[i - 1]
            )
        else:
            gap = distinct_times[i] - distinct_times[i - 1]

        adjustments[t] = rand_adjustment(gap)
        cumulative_adjustment += adjustments[t]

    for m in mid.tracks[1][10:400]:
        print(m.time)
    for track, messages in enumerate(mid.tracks):
        msg_adjustments = get_adj(actual_times[track], adjustments)
        for i, m in enumerate(messages):
            m.time += msg_adjustments[i]
    print('after')
    for m in mid.tracks[1][10:400]:
        print(m.time)
    mid.save('test2_new.mid')

main()
