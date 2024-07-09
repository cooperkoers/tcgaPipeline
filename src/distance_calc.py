import pandas as pd
import numpy as np
import sys

# different distance calculations for two depth files
def distance(depth1, depth2, method):
    # relative distance calculation
    depth1 = pd.read_csv(depth1, sep="\t", header=None)
    depth1.columns = ["chrom", "start", "end", "depth"]
    depth2 = pd.read_csv(depth2, sep="\t", header=None)
    depth2.columns = ["chrom", "start", "end", "depth"]

    # calculate the relative distance between the two depth files
    result = []
    for chrom in depth1["chrom"].unique():
        for start in depth1[depth1["chrom"] == chrom]["start"].unique():
            if start in depth2[depth2["chrom"] == chrom]["start"].unique():
                # relative distance calculation
                if method == 'relative':
                    result.append(
                        {
                            "chrom": chrom,
                            "start": start,
                            "distance": np.abs(
                                depth1[
                                    (depth1["chrom"] == chrom) & (depth1["start"] == start)
                                ]["depth"]
                                - depth2[
                                    (depth2["chrom"] == chrom) & (depth2["start"] == start)
                                ]["depth"]
                            ) / (depth1[
                                (depth1["chrom"] == chrom) & (depth1["start"] == start)
                                ]["depth"])
                        }
                    )
                # mean squared error calculation
                if method == 'mse':
                    result.append(
                        {
                            "chrom": chrom,
                            "start": start,
                            "distance": np.abs(
                                depth1[
                                    (depth1["chrom"] == chrom) & (depth1["start"] == start)
                                ]["depth"]
                                - depth2[
                                    (depth2["chrom"] == chrom) & (depth2["start"] == start)
                                ]["depth"]
                            ) ** 2
                        }
                    )
                else:
                    sys.exit("Invalid method. Please choose either 'relative' or 'mse'.")
    
    # return sum of distances
    return sum([x["distance"] for x in result])