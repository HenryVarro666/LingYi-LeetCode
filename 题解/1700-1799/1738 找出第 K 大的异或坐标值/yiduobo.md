---
title: "1738. 找出第K大的异或坐标值"
aliases: ["yiduobo的每日leetcode 1738.找出第K大的异或坐标值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/prefix-sum", "leetcode/quickselect", "leetcode/sorting", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/453366696"
zhihu_id: "453366696"
zhihu_title: "yiduobo的每日leetcode 1738.找出第K大的异或坐标值"
question_id: "1738"
question: "找出第 K 大的异或坐标值"
problem_url: "https://leetcode.cn/problems/find-kth-largest-xor-coordinate-value/"
difficulty: "Medium"
rating: 1671
created: "2022-01-04T23:59:51+08:00"
updated: "2022-01-04T23:59:51+08:00"
upvotes: 0
comments: 0
---

# 1738. 找出第K大的异或坐标值

> **[yiduobo的每日leetcode 1738.找出第K大的异或坐标值](https://zhuanlan.zhihu.com/p/453366696) · 知乎 · 2022-01-04 · 赞同 0**
> 力扣：[1738. 找出第 K 大的异或坐标值](https://leetcode.cn/problems/find-kth-largest-xor-coordinate-value/) · Medium · 灵茶山艾府：[两种方法：二维前缀异或和/列前缀异或和（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1738.找出第K大的异或坐标值

[力扣](https://leetcode-cn.com/problems/find-kth-largest-xor-coordinate-value/)

由于异或操作是没有单调性的，因此想直接从原始矩阵matrix中就得出异或结果的第K大的值是比较困难的，必须先算出每个位置上的异或结果。好在是异或操作满足a^a \= 0以及结合律，那么在这里对于异或结果矩阵中f[i][j]这个位置上的值，可以使用经典的计算方法来求解，即f[i][j] \= f[i - 1][j] ^ f[i][j -1] ^ f[i - 1][j - 1] ^ m[i][j]。

证明也很简单，将这些式子分别列出来就行了：

f[i - 1][j] \= (m[0][0] ^ ... ^ m[0][j]) ^ (m[1][0] ^ ... ^ m[1][j]) ^ ... ^ (m[i - 1][0] ^ ... ^ m[i - 1][j])

如果将j一列的值提出来，那么就有

f[i - 1][j] \= ((m[0][0] ^ ... ^ m[0][j - 1]) ^ ... ^ (m[i - 1][0] ^ ... ^ m[i - 1][j - 1])) ^ (m[0][j] ^ ... ^m[i - 1][j])

可以发现，前面这个括号中的异或和就是f[i - 1][j - 1]，那么这里就有

f[i - 1][j] \= f[i - 1][j - 1] ^ (m[0][j] ^ ... ^ m[i - 1][j])

类似的，对于f[i][j - 1]，将第i行的值提出来就有

f[i][j - 1] \= f[i - 1][j - 1] ^ (m[i][0] ^... ^ m[i][j - 1])

上面的式子对于f[i][j]同样适用，先将第i行提出来，就有

f[i][j] \= f[i - 1][j] ^ (m[i][0] ^ ... ^ m[i][j])

两边同时异或上f[i - 1][j - 1]，并将后面括号中的m[i][j]移出去，就有

f[i][j] ^ f[i - 1][j - 1] \= f[i - 1][j] ^ (f[i - 1][j - 1] ^ (m[i][0] ^ ... ^ m[i][j - 1])) ^ m[i][j]

中间括号里面的式子异或结果就是f[i][j - 1]，那么就有

f[i][j] ^ f[i - 1][j - 1] \= f[i - 1][j] ^ f[i][j - 1] ^ m[i][j]

两边再同时异或上f[i - 1][j - 1]，就有

f[i][j] \= f[i - 1][j] ^ f[i][j - 1] ^ f[i - 1][j - 1] ^ m[i][j]

有了这个式子，就可以从上到下从左至右遍历每个位置，并在O(1)的时间复杂度内计算出这个位置上的异或结果了。得到所有的异或结果之后，可以采用排序或者快速选择法找出其中第k大的数。对于快速选择法找第k大的数可以参考215题的题解，这里就不展开了。

由于这里的f每一行只与上一行的结果有关，因此可以将f滚动起来省去一维。

最后附上python代码：

```python
class Solution(object):
    def kthLargestValue(self, matrix, k):
        """
        :type matrix: List[List[int]]
        :type k: int
        :rtype: int
        """

        m = len(matrix)
        n = len(matrix[0])
        f = [0] * n
        nums = []
        for i in range(m):
            g = f[:]
            for j in range(n):
                if i == 0:
                    if j == 0:
                        f[j] = matrix[i][j]
                    else:
                        f[j] = f[j - 1] ^ matrix[i][j]
                elif j == 0:
                    f[j] = g[j] ^ matrix[i][j]
                else:
                    f[j] = f[j - 1] ^ g[j] ^ g[j - 1] ^ matrix[i][j]
            
                nums.append(f[j])

        return self.search(nums, 0, len(nums) - 1, len(nums) - k + 1)

    def search(self, nums, left, right, k):
        if left == right:
            return nums[left]

        mid = nums[(left + right) / 2]
        i = left
        j = right
        while i <= j:
            while i <= right and nums[i] < mid:
                i += 1
            while j >= left and nums[j] > mid:
                j -= 1
            if i <= j:
                nums[i], nums[j] = nums[j], nums[i]
                i += 1
                j -= 1

        if j - left + 1 >= k:
            return self.search(nums, left, j, k)
        elif i - left >= k:
            return nums[left + k - 1]
        else:
            return self.search(nums, i, right, k - (i - left))
```
