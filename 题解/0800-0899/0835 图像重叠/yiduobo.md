---
title: "835. 图像重叠"
aliases: ["yiduobo的每日leetcode 835.图像重叠"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/enumeration", "leetcode/bao-li", "leetcode/fast-fourier-transform", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/346529546"
zhihu_id: "346529546"
zhihu_title: "yiduobo的每日leetcode 835.图像重叠"
question_id: "835"
question: "图像重叠"
problem_url: "https://leetcode.cn/problems/image-overlap/"
difficulty: "Medium"
created: "2021-01-24T22:39:57+08:00"
updated: "2021-01-24T22:39:57+08:00"
upvotes: 0
comments: 0
---

# 835. 图像重叠

> **[yiduobo的每日leetcode 835.图像重叠](https://zhuanlan.zhihu.com/p/346529546) · 知乎 · 2021-01-24 · 赞同 0**
> 力扣：[835. 图像重叠](https://leetcode.cn/problems/image-overlap/) · Medium · 灵茶山艾府：[两种方法：暴力枚举 / 卷积（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

835.图像重叠

[力扣](https://leetcode-cn.com/problems/image-overlap/)

由于这里给出的图像大小很小，因此直接枚举移动的范围然后进行判断就行了。我在这里采用的是枚举B中每个值为1的点经过什么样的操作可以重叠到A中值为1的点，然后统计这些操作出现的次数。统计完成后，若某种操作出现k次，说明B中有k个值为1的点经过该操作之后可以与A重叠，那么此时出现次数最多的操作就是最终答案。

最后附上python代码：

```python
class Solution(object):
    def largestOverlap(self, img1, img2):
        """
        :type img1: List[List[int]]
        :type img2: List[List[int]]
        :rtype: int
        """

        m = len(img1)

        pos1_set = set()
        for x1 in range(m):
            for y1 in range(m):
                if img1[x1][y1] == 1:
                    pos1_set.add((x1, y1))

        pos2_set = set()
        move_dict = {}
        for x2 in range(m):
            for y2 in range(m):
                if img2[x2][y2] == 1:
                    for x1, y1 in pos1_set:
                        delta_x = x1 - x2
                        delta_y = y1 - y2
                        move_dict[(delta_x, delta_y)] = move_dict.get((delta_x, delta_y), 0) + 1
        
        if not move_dict:
            return 0
        return max(move_dict.values())
```
