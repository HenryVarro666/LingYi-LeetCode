---
title: "3030. 找出网格的区域平均强度"
aliases: ["yiduobo的每日leetcode 3030.找出网格的区域平均强度"]
tags: ["leetcode", "yiduobo", "leetcode/medium"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695555069"
zhihu_id: "695555069"
zhihu_title: "yiduobo的每日leetcode 3030.找出网格的区域平均强度"
question_id: "3030"
question: "找出网格的区域平均强度"
problem_url: "https://leetcode.cn/problems/find-the-grid-of-region-average/"
difficulty: "Medium"
created: "2024-05-01T01:42:21+08:00"
updated: "2024-05-01T01:42:21+08:00"
upvotes: 1
comments: 0
---

# 3030. 找出网格的区域平均强度

> **[yiduobo的每日leetcode 3030.找出网格的区域平均强度](https://zhuanlan.zhihu.com/p/695555069) · 知乎 · 2024-05-01 · 赞同 1**
> 力扣：[3030. 找出网格的区域平均强度](https://leetcode.cn/problems/find-the-grid-of-region-average/) · Medium · 灵茶山艾府：[阅读理解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3030.找出网格的区域平均强度

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-grid-of-region-average/description/)

题目将所有相邻位置间差的绝对值大小不超过threshold的3\*3网格定义为区域，对于每个区域，需要计算区域的平均值作为该区域的平均强度，然后再对每个单元格计算其所属所有区域平均强度的平均值。由于每个单元格所属的区域可能不同，因此在这里需要两个单元格粒度的数组s和cnt分别统计每个单元格所属区域的平均强度之和，以及该单元格属于多少个区域。

接下来枚举所有区域的中心位置，也就是原始image中除开边界的这一圈之外的其他所有单元格，接下来对于一个区域中心，按上下左右偏移量都为1来划分出其作为中心位置对应的3\*3网格，接下来遍历该网格的上方两行以及左侧两列，检测相邻单元格之差的绝对值是否没有超过threshold，在这个过程中顺便计算网格中的数值之和。若网格符合区域的定义，那么就通过数值之和除以9来计算区域的平均强度，然后更新区域中所有网格对应的s和cnt。

全部计算完成后，再遍历每个网格。若当前网格对应的cnt为0，说明其不属于任何区域，其数值保持不变，否则就用其对应的s除以cnt来计算其对应的最终结果。

最后附上python代码：

```python
class Solution(object):
    def resultGrid(self, image, threshold):
        """
        :type image: List[List[int]]
        :type threshold: int
        :rtype: List[List[int]]
        """

        m = len(image)
        n = len(image[0])

        s = [[0] * n for _ in range(m)]
        cnt = [[0] * n for _ in range(m)]

        def update(x, y):
            tot = 0
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    if i < 1 and abs(image[x + i][y + j] - image[x + i + 1][y + j]) > threshold:
                        return
                    if j < 1 and abs(image[x + i][y + j] - image[x + i][y + j + 1]) > threshold:
                        return
                    
                    tot += image[x + i][y + j]
            
            tot /= 9
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    s[x + i][y + j] += tot
                    cnt[x + i][y + j] += 1

        for i in range(1, m - 1):
            for j in range(1, n - 1):
                update(i, j)
        
        res = []
        for i in range(m):
            res.append([])
            for j in range(n):
                if cnt[i][j] == 0:
                    res[-1].append(image[i][j])
                else:
                    res[-1].append(s[i][j] / cnt[i][j])
        
        return res
```
