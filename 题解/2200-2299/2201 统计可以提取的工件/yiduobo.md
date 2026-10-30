---
title: "2201. 统计可以提取的工件"
aliases: ["yiduobo的每日leetcode 2201.统计可以提取的工件"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/enumeration"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/538976628"
zhihu_id: "538976628"
zhihu_title: "yiduobo的每日leetcode 2201.统计可以提取的工件"
question_id: "2201"
question: "统计可以提取的工件"
problem_url: "https://leetcode.cn/problems/count-artifacts-that-can-be-extracted/"
difficulty: "Medium"
created: "2022-07-08T00:09:33+08:00"
updated: "2022-07-08T00:09:33+08:00"
upvotes: 0
comments: 0
---

# 2201. 统计可以提取的工件

> **[yiduobo的每日leetcode 2201.统计可以提取的工件](https://zhuanlan.zhihu.com/p/538976628) · 知乎 · 2022-07-08 · 赞同 0**
> 力扣：[2201. 统计可以提取的工件](https://leetcode.cn/problems/count-artifacts-that-can-be-extracted/) · Medium · 灵茶山艾府：[暴力枚举 + 哈希表](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2201.统计可以提取的工件

[力扣](https://leetcode.cn/problems/count-artifacts-that-can-be-extracted/)

题目是非常典型的二维矩阵和问题，由于数据规模不大，因此可以使用常规的二维前缀和来进行处理。

具体来说，就是先将原始的网格视为值全部为0的二维数组，接下来将dig过的位置都置为1，然后计算二维前缀和s。接下来对于每一个工件(r1, c1, r2, c2)，就可以利用s来高效地求解这个工件范围内的矩阵和。若这个和恰好等于这个工件覆盖的面积，则说明这个工件可以被提取。

最后附上python代码：

```python
class Solution(object):
    def digArtifacts(self, n, artifacts, dig):
        """
        :type n: int
        :type artifacts: List[List[int]]
        :type dig: List[List[int]]
        :rtype: int
        """

        max_r = max_c = 0
        for r1, c1, r2, c2 in artifacts:
            max_r = max(max_r, r2)
            max_c = max(max_c, c2)
        
        f = [[0] * (max_c + 1) for _ in range(max_r + 1)]

        for r, c in dig:
            if r <= max_r and c <= max_c:
                f[r][c] = 1
        
        s = [[0] * (max_c + 1) for _ in range(max_r + 1)]
        for r in range(max_r + 1):
            for c in range(max_c + 1):
                if r == 0:
                    if c == 0:
                        s[r][c] = f[r][c]
                    else:
                        s[r][c] = s[r][c - 1] + f[r][c]
                elif c == 0:
                    s[r][c] = s[r - 1][c] + f[r][c]
                else:
                    s[r][c] = s[r - 1][c] + s[r][c - 1] - s[r - 1][c - 1] + f[r][c]
        

        res = 0
        for r1, c1, r2, c2 in artifacts:
            if r1 == 0:
                if c1 == 0:
                    now_s = s[r2][c2]
                else:
                    now_s = s[r2][c2] - s[r2][c1 - 1]
            elif c1 == 0:
                now_s = s[r2][c2] - s[r1 - 1][c2]
            else:
                now_s = s[r2][c2] - s[r2][c1 - 1] - s[r1 - 1][c2] + s[r1 - 1][c1 - 1]
            
            if now_s == (r2 - r1 + 1) * (c2 - c1 + 1):
                res += 1
        
        return res
```
