class Solution:
    def transpose(self, matrix: List[List[int]]) -> List[List[int]]:
        # m = 行数; n = 列数
        m, n = len(matrix), len(matrix[0])
        # 创建 n 行，每行 m 个 0
        ans = [[0] * m for _ in range(n)]
        for i, row in enumerate(matrix):
            for j, x in enumerate(row):
                ans[j][i] = x
        return ans