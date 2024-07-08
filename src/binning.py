import pandas as pd
import numpy as np
import os

def depth_binning(df, bin_size):
    """
    bins the depth values in the dataframe by basepair position and chromosome,
    with each bin being the size of bin_size based on the difference between the 
    start and end columns – grouped by chromosome. 
    
    The number of counts are then summed for each and this is turned 
    into an rpkm value for each bin.

    example df:
    chr  start   end     depth
    chr1 10000   10001   10
    chr1 10101   10102   20
    chr1 10202   10203   30
    chr1 12003   10304   40
    """