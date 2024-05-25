"""
Calculate ANI score between 2 FASTA sequences.
"""
import functools
import multiprocessing
import os
import time

import numpy as np
from Bio import SeqIO
from tqdm import tqdm


def ani_score(fasta_file_1: str, fasta_file_2: str) -> float:
    # Parse FASTA files
    seq_1 = SeqIO.read(fasta_file_1, 'fasta')
    seq_2 = SeqIO.read(fasta_file_2, 'fasta')

    # Convert sequences to string
    seq_1 = str(seq_1.seq)
    seq_2 = str(seq_2.seq)

    # Calculate alignment length
    align_len = min(len(seq_1), len(seq_2))

    # Calculate identity
    ani_score = sum(1 for base1, base2 in zip(seq_1, seq_2) if base1 == base2)
    ani_score_over_length = ani_score*100/align_len
    # consider heavy computation task happens below that takes 4 seconds
    # time.sleep(4)
    return ani_score_over_length


if __name__ == "__main__":
    fasta_folder = r'D:\CodingProjects\parallel_ANI\fasta_data'
    file_1 = os.path.join(fasta_folder, 'test_1.fasta')
    second_file_list = [os.path.join(
        fasta_folder, f'test_{num}.fasta') for num in [2, 3, 4, 5]]

    # Default calculation
    start = time.time()
    score = []
    for file in tqdm(second_file_list):
        score.append(ani_score(file_1, file))
    end = time.time()
    print(score)
    print(f'Total time to process: {end-start:.2f}s')

    # Time to multiprocess
    pool = multiprocessing.Pool(processes=7)
    total_records = len(second_file_list)
    results = []
    partial_func = functools.partial(ani_score, file_1)
    start = time.time()
    process = pool.imap(partial_func, second_file_list)
    for result in tqdm(process, total=total_records):
        results.append(result)
    end = time.time()
    print(f'Total time to multi-process: {end-start:.5f}s')
    pool.close()
    pool.join()
    print(results)

    # other options
    pool = multiprocessing.Pool(processes=7)
    total_records = len(second_file_list)
    results = []
    partial_func = functools.partial(ani_score, file_1)
    start = time.time()
    process = pool.imap_unordered(partial_func, second_file_list)
    for result in tqdm(process, total=total_records):
        results.append(result)
    end = time.time()
    print(f'Total time to multi-process (unordered): {end-start:.5f}s')
    pool.close()
    pool.join()
    print(results)

    pool = multiprocessing.Pool(processes=7)
    partial_func = functools.partial(ani_score, file_1)
    results = pool.map(partial_func, second_file_list)
    end = time.time()
    print(f'Total time to multi-process (simple map): {end-start:.5f}s')
    pool.close()
    pool.join()
    print(results)

    pool = multiprocessing.Pool(processes=7)
    process = pool.map_async(partial_func, second_file_list)
    results = process.get()
    end = time.time()
    print(f'Total time to multi-process (async map): {end-start:.5f}s')
    pool.close()
    pool.join()
    print(results)
