import pandas as pd
import numpy as np
import sys

def depth_binning(depthFile, bin_size):
    """
    bins the depth values in the dataframe by basepair position and chromosome,
    with each bin being the size of bin_size based on the difference between the 
    start and end columns – grouped by chromosome. 
    
    The number of counts are then summed for each and this is turned 
    into an rpkm value for each bin.
    """
    df = pd.read_csv(depthFile, sep='\t', header=None)
    df.columns = ['chrom', 'start', 'end', 'depth']

    result = []

    for chrom in df['chrom'].unique():
        chrom_df = df[df['chrom'] == chrom].sort_values(by='start')
        start_pos = chrom_df['start'].min()
        end_pos = chrom_df['end'].max()

        for region_start in range(start_pos, end_pos, bin_size):
            region_end = region_start + bin_size
            region_df = chrom_df[(chrom_df['start'] >= region_start) & (chrom_df['end'] <= region_end)]
            if not region_df.empty:
                count_sum = region_df['depth'].sum()
                row_count = len(region_df)
                result.append({'chrom': chrom, 'start': region_start, 'end': region_end, 'count_sum': count_sum, 'row_count': row_count}, 'rpkm': count_sum / row_count * 1000000)
    
    result_df = pd.DataFrame(result)
    result_df.set_index('chrom', 'start', inplace = True)

    # save the result to a file, with name being the same as the input file with a .binnedcounts.tsv extension and no .bed extension
    result_df.to_csv(depthFile.replace('.bed', '.binnedcounts.tsv'), sep='\t')


if __name__ == '__main__':
    depth_binning(sys.argv[1], sys.argv[2])