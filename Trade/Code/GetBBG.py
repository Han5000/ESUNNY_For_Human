from concurrent.futures import ThreadPoolExecutor as Pool
from pickle import dump

from Bin.Config import bbg_contract
from Code.xbbg import blp


def dump_file(snap):
    print(snap)
    with open(f"Bin\\BBGData\\{snap['TICKER']}.lc", 'wb') as f:
        dump(snap, f)


def get_bbg():
    with Pool(500) as exe:
        for snap in blp.live(bbg_contract, flds=['Last_Price', 'Ask', 'Ask_Size', 'Bid', 'BID_SIZE']):
            exe.submit(dump_file, snap)
