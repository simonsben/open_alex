from json import load, dump, loads
from pathlib import Path
from re import compile
from typing import NoReturn, Optional, Set, Iterable, Any
from urllib.request import urlopen


TIMEOUT = 2
MAX_PER_PAGE = 200
RELATED_KEYS = ["related_works", "referenced_works"]

url_pattern = compile(r"(\w+\.)?openalex.org(/works)?")
id_pattern = compile(r"([\w\d]+)$")
api_base_url = "api.openalex.org/works"


class Cache:
    _cache_path: Path
    _data: dict
    _cache_hits: int = 0
    _cache_misses: int = 0

    def __init__(self, file_name: str = "data.json"):
        self._cache_path = Path(file_name)
        self.load_data()

    def load_data(self) -> NoReturn:
        if hasattr(self, "_data"):
            return

        if not self._cache_path.exists():
            self._data = {}
            return

        try:
            with self._cache_path.open('r') as fl:
                self._data = {entry["id"]: entry for entry in load(fl)}
        except Exception as e:
            print(f"There was an issue opening {self._cache_path.name}", e)

    def close(self) -> NoReturn:
        if self._data:
            try:
                with self._cache_path.open('w') as fl:
                    dump(list(self._data.values()), fl)
            except Exception as e:
                print(f"There was an error dumping data to {self._cache_path.name}", e)

    def export(self, path: Path) -> NoReturn:
        with path.open('w') as fl:
            dump({"results": list(self._data.values())}, fl)

    @property
    def cache_hit_rate(self) -> float:
        denominator = (self._cache_hits + self._cache_misses) or 1
        return self._cache_hits / denominator

    def __getitem__(self, data_name: str) -> Optional[dict]:
        data = self._data.get(data_name, None)
        if data:
            self._cache_hits += 1
        else:
            self._cache_misses += 1

        return data

    def __setitem__(self, key: str, value: str) -> NoReturn:
        self._data[key] = value


cache = Cache()


def join_parameters(**kwargs) -> str:
    if not kwargs:
        print("WARNING: parameters passed.")

    start = "?" if not kwargs.pop("addition", False) else "&"
    parameters = "&".join([f"{key}={value}" for key, value in kwargs.items()])
    return f"{start}{parameters}&per_page=200"


def get_work(work_url: str, email: str, addition: bool = False) -> dict:
    cached_data = cache[work_url]
    if cached_data:
        return cached_data

    work_url = url_pattern.sub(api_base_url, work_url, count=1)
    request_url = f"{work_url}{join_parameters(mailto=email, addition=addition)}"

    try:
        response = urlopen(request_url, timeout=TIMEOUT)
        response_data = loads(response.read())
    except Exception as e:
        print(f"There was an issue getting {work_url}.", e)
        return {}

    cache[work_url] = response_data
    return response_data


def flatten_sets(sets: Iterable[Set[str]]) -> Set[str]:
    data = set()
    for _set in sets:
        data = data.union(_set)

    return data


def get_related_work_urls(work: dict) -> Set[str]:
    return flatten_sets((set(work.get(key, [])) for key in RELATED_KEYS))


def flush_cache() -> NoReturn:
    cache.close()


def is_not_null(work: Optional[Any]) -> bool:
    return work or False


def export_data(filename: str, work_ids: Iterable[str] = None) -> NoReturn:
    path = Path(filename)
    if not work_ids:
        cache.export(path)
    else:
        results = filter(is_not_null, (cache[work_id] for work_id in work_ids))
        data = {"results": list(results)}

        with path.open('w') as fl:
            dump(data, fl)
