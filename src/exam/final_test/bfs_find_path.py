from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager, active_children
from queue import Queue

from loguru import logger

from src.exam.final_test.parse_url import *

MAX_DEPTH = 6


class DepthError(Exception):
    pass


class BFSWiki:
    def __init__(self, unique: bool = True) -> None:
        self.parser: Parse = Parse()
        self.unique: bool = unique
        self.visited: set[str] = set()

    def find_path_two_url(self, start_url: str, end_url: str, n_workers: int) -> list[str]:
        if self.unique:
            self.visited.add(start_url)
        with Manager() as manager, ProcessPoolExecutor(max_workers=n_workers) as executor:
            current_wave_queue = manager.Queue()
            current_wave_queue.put(URLNode(start_url, None))
            for depth in range(MAX_DEPTH):
                logger.info(f"current depth: {depth + 1}")
                futures = [
                    executor.submit(self.parser.get_all_href, current_wave_queue.get())
                    for _ in range(current_wave_queue.qsize())
                ]
                for future in futures:
                    curr_node_links: list[URLNode] = future.result()
                    output = self.check_links(curr_node_links, end_url, current_wave_queue)
                    if output is not None:
                        logger.info(f"find path: from {start_url} to {end_url}")
                        return output

            raise DepthError("The maximum depth has been exceeded")

    def check_links(
        self, curr_node_links: list[URLNode], end_url: str, current_wave_queue: Queue
    ) -> Optional[list[str]]:
        for curr_node_link in curr_node_links:
            if curr_node_link.url == end_url:
                for process in active_children():
                    process.kill()
                return curr_node_link.get_path()
            if self.unique:
                if curr_node_link.url not in self.visited:
                    current_wave_queue.put(curr_node_link)
                self.visited.add(curr_node_link.url)
            else:
                current_wave_queue.put(curr_node_link)
