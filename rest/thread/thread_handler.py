from concurrent.futures import ThreadPoolExecutor
import os

gbl_executor = ThreadPoolExecutor(
    max_workers=min(32, (os.cpu_count() or 1) + 4),
    thread_name_prefix="glb_worker"
)
