from core import get_work, flush_cache, get_related_work_urls, cache, flatten_sets, save_json_for_vos
from io_utilities import load_config
from functools import partial
from multiprocessing.dummy import Pool
from pathlib import Path


NUM_STEPS = 2
NUM_WORKERS = 3
EXPORT_FILENAME = Path("openalex_data.json")


config = load_config()
email = config.get("email", "")
base_paper = config.get("base_paper")

current_round = {base_paper}
included_works = current_round.copy()
next_round = []
workers = Pool(NUM_WORKERS)

work_function = partial(get_work, email=email)

for steps in range(NUM_STEPS):
    works = workers.map(work_function, current_round)
    for work in filter(None, works):
        next_round.append(get_related_work_urls(work))

    included_works = included_works.union(current_round)
    current_round = flatten_sets(next_round)
    next_round = []

flush_cache()
save_json_for_vos(EXPORT_FILENAME, included_works)

print(f"Cache hit rate: %.2f" % cache.cache_hit_rate)
