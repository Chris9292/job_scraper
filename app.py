from multiprocessing import Pool
import time
from itertools import product
from functions import Scraper, get_urls, write_to_log
import sys
from database import Database

sys.setrecursionlimit(25000)

if __name__ == '__main__':
    start = time.time()
    hrefs = get_urls()
    with Pool(12) as p:
        jobs = p.map(Scraper, hrefs)
        jobs_details = [i.details() for i in jobs]
        p.map(Database, jobs_details)
    duration = time.time()-start
    print(f'Scrape task ended in {duration} seconds.')
    write_to_log(duration)




