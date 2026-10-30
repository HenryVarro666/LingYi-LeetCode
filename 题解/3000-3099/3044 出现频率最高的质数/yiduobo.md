---
title: "3044. 出现频率最高的质数"
aliases: ["yiduobo的每日leetcode 3044.出现频率最高的质数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/696049353"
zhihu_id: "696049353"
zhihu_title: "yiduobo的每日leetcode 3044.出现频率最高的质数"
question_id: "3044"
question: "出现频率最高的质数"
problem_url: "https://leetcode.cn/problems/most-frequent-prime/"
difficulty: "Medium"
rating: 1737
created: "2024-05-05T22:26:48+08:00"
updated: "2024-05-05T22:26:48+08:00"
upvotes: 1
comments: 0
---

# 3044. 出现频率最高的质数

> **[yiduobo的每日leetcode 3044.出现频率最高的质数](https://zhuanlan.zhihu.com/p/696049353) · 知乎 · 2024-05-05 · 赞同 1**
> 力扣：[3044. 出现频率最高的质数](https://leetcode.cn/problems/most-frequent-prime/) · Medium · 灵茶山艾府：[枚举（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3044.出现频率最高的质数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/most-frequent-prime/description/)

题目给出的数据规模很小，在极限情况下，每个位置在横、竖、左对角线、右对角线上最多只能构造出5个数字，因此可以构造出的数字数量不超过6\*6\*5\*4 \= 720个。实际上，部分位置在对角线上可构造的数字更少，因此实际上可以构造出的数字数量更少，完全可以暴力枚举。

具体来说，遍历矩阵中的每个数作为枚举的起点，然后向八个方向扩散，每次将当前数字加入到构造的数字的末位直到来到边界，在这个过程中将构造的所有数字都加入到哈希表中并统计出现的次数。

枚举完成后，再遍历所有构造出的数字，检测是否为质数，取出现次数最多的质数最为最终答案即可。关于质数的检测，由于本题最大构造出来的数字为999999，但需要检测的数字数量很少，因此在这里使用暴力法来检测反而是更好的。

最后附上python代码：

```python
class Solution(object):
    def mostFrequentPrime(self, mat):
        """
        :type mat: List[List[int]]
        :rtype: int
        """

        num_dict = {}
        m = len(mat)
        n = len(mat[0])

        dx = [0, 1, 1, 1, 0, -1, -1, -1]
        dy = [1, 1, 0, -1, -1, -1, 0, 1]

        for i in range(m):
            for j in range(n):
                for d in range(8):
                    x, y, v = i, j, mat[i][j]
                    while True:
                        x += dx[d]
                        y += dy[d]
                        if 0 <= x < m and 0 <= y < n:
                            v = v * 10 + mat[x][y]
                            num_dict[v] = num_dict.get(v, 0) + 1
                        else:
                            break

        res = -1
        for v in num_dict:
            x = 2
            flag = True
            while x * x <= v:
                if v % x == 0:
                    flag = False
                    break
                x += 1
            
            if flag and (res == -1 or num_dict[res] < num_dict[v] or (num_dict[res] == num_dict[v] and res < v)):
                res = v
        
        return res
```
