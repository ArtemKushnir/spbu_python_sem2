from argparse import ArgumentParser

from src.exam.final_test.bfs_find_path import *


def main(links_path: list[str], n_jobs: int, unique: bool) -> list[str]:
    cnt_links = len(links_path)
    if n_jobs // cnt_links == 0:
        task_per_worker = 1
    else:
        task_per_worker = n_jobs // cnt_links

    bfs_wiki = BFSWiki(unique)
    if not unique:
        pass
    all_paths = []
    with ProcessPoolExecutor(len(links_path)) as executor:
        for i in range(len(links_path) - 1):
            start_url = links_path[i]
            end_url = links_path[i + 1]
            all_paths.append(executor.submit(bfs_wiki.find_path_two_url, start_url, end_url, task_per_worker))
        result_path = [links_path[0]]
        for path in all_paths:
            result_path.extend(path.result()[1:])
        return result_path


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("links_path", nargs="+", type=str, help="url to find path")
    argparser.add_argument("n_jobs", type=int, help="count process")
    argparser.add_argument("--unique", action="store_true", help="is it possible to visit the page twice")
    my_args = argparser.parse_args()
    try:
        print(main(**vars(my_args)))
    except DepthError as e:
        print(e)
    except ConnectionError as e:
        print(e)
