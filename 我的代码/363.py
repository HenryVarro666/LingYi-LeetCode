# ### https://leetcode.cn/problems/max-sum-of-rectangle-no-larger-than-k/

# class Solution:
#     def maxSumSubmatrix(self, matrix: List[List[int]], k: int) -> int:
#         m, n = len(matrix), len(matrix[0])
#         for i in range(m):
#             for j in range(1,n):
#                 matrix[i][j] += matrix[i][j-1]
#         ans = -inf
#         for i in range(n):
#             for j in range(i, n):
#                 pres = SortedList([0])
#                 pre = 0
#                 for r in range(m):
#                     pre += matrix[r][j] - (0 if i == 0 else matrix[r][i - 1])
#                     idx = pres.bisect_left(pre - k)
#                     if idx < len(pres):
#                         ans = max(ans, pre - pres[idx])
#                     pres.add(pre)
#         return ans

from sortedcontainers import SortedList

class Solution:
    def maxSumSubmatrix(self, matrix: List[List[int]], k: int) -> int:

        m, n = len(matrix), len(matrix[0])

        # 第一步：先把每一行变成“行前缀和”
        # 这样以后想求某一行在 [left, right] 这一段的和，
        # 就可以 O(1) 算出来：
        # row[right] - row[left - 1]
        for row in matrix:
            for j in range(1, n):
                row[j] += row[j - 1]

        # 答案可能是负数，所以初始化为负无穷
        ans = float('-inf')

        # 第二步：枚举矩形的左边界 left
        for left in range(n):
            # 第三步：枚举矩形的右边界 right
            for right in range(left, n):

                # 现在左右边界固定了，
                # 我们就把二维问题压成一维问题：
                # 对于每一行 r，计算这一行在 [left, right] 之间的元素和
                # 然后问题就变成：
                # “在这个一维数组里，找一个子数组，
                #  使得子数组和 <= k，并且尽量大”

                # s 存的是“历史前缀和”，并保持有序
                # 先放一个 0，表示“前面一个数都没选”
                s = SortedList([0])

                # pre 表示当前扫描到第 r 行时的前缀和
                pre = 0

                # 第四步：按行往下扫，把二维变成的一维数组做“前缀和 + 有序查找”
                for r in range(m):
                    # cur 表示第 r 行在 [left, right] 这一段的区间和
                    # 如果 left == 0，说明就是从 0 到 right，直接取 matrix[r][right]
                    # 否则减去 left 前一列的前缀和
                    cur = matrix[r][right] - (matrix[r][left - 1] if left > 0 else 0)

                    # 更新当前前缀和
                    pre += cur

                    # 我们想找某个历史前缀和 old_pre，使得：
                    # pre - old_pre <= k
                    #
                    # 变形得到：
                    # old_pre >= pre - k
                    #
                    # 也就是说：
                    # 在历史前缀和里，找“第一个 >= pre - k 的数”
                    idx = s.bisect_left(pre - k)

                    # 如果找到了这样的 old_pre，
                    # 那么 pre - old_pre 就是一个 <= k 的子数组和
                    # 并且因为我们找的是“最小的满足条件的 old_pre”，
                    # 所以这个子数组和尽量大
                    if idx < len(s):
                        ans = max(ans, pre - s[idx])

                    # 别忘了把当前前缀和放进去，供后面使用
                    s.add(pre)

        return ans
    

# 这题我先枚举矩形左右边界，把二维矩阵压成一维数组，数组的每个元素表示某一行在这两列之间的区间和。然后问题就变成：在一维数组里找一个连续子数组，使得和不超过 k 且尽量大。这个一维问题用前缀和加有序集合做：对当前前缀和 pre，在历史前缀和里二分找第一个大于等于 pre-k 的值，就能得到一个尽量大的、且不超过 k 的子数组和。

# 枚举左右边界，二维压一维；然后用前缀和 + 有序集合，二分找最小的满足 old_pre >= pre-k 的历史前缀和，更新答案。

# 为什么能二维压一维？
# 因为固定左右边界后，矩形只剩上下边界没定，每一行在这个列区间上的和可以看成一个一维数组元素。
# 为什么要二分找 pre-k？
# 因为子数组和是 pre-old_pre，要求 <=k，所以 old_pre >= pre-k。
# 为什么要有序集合？
# 因为要快速找到“第一个大于等于某个值的历史前缀和”。