from core import get_work, flush_cache, get_related_work_urls, export_data, cache, flatten_sets
from functools import partial
from multiprocessing.dummy import Pool


NUM_STEPS = 3
NUM_WORKERS = 5
EMAIL = ""
BASE_PAPER = ""
EXPORT_FILENAME = "openalex_data.json"

current_round = {BASE_PAPER}
included_works = current_round.copy()
next_round = []
workers = Pool(NUM_WORKERS)

work_function = partial(get_work, email=EMAIL)

for steps in range(NUM_STEPS):
    works = workers.map(work_function, current_round)
    for work in filter(None, works):
        next_round.append(get_related_work_urls(work))

    included_works = included_works.union(current_round)
    current_round = flatten_sets(next_round)
    next_round = []

flush_cache()
export_data(EXPORT_FILENAME, included_works)

print(f"Cache hit rate: %.2f" % cache.cache_hit_rate)
