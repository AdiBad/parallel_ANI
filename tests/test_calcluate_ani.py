"""
Test case for ANI function.
"""

import unittest

from parameterized import parameterized

from parallel_ANI.calculate_ani import ani_score


class TestCalculateANI(unittest.TestCase):

    def setUp(self):
        self.fasta_files = {
            2: r'D:\CodingProjects\parallel_ANI\fasta_data\test_2.fasta',
            3: r'D:\CodingProjects\parallel_ANI\fasta_data\test_3.fasta',
        }
        self.expected_scores = {
            2: 75.0,
            3: 50.0
        }

    @parameterized.expand([(2), (3)])
    def test_ani_score(self, file_2: int):
        fasta_file_1 = r'D:\CodingProjects\parallel_ANI\fasta_data\test_1.fasta'
        assert ani_score(
            fasta_file_1, self.fasta_files[file_2]) == self.expected_scores[file_2]


if __name__ == '__main__':
    unittest.main()
