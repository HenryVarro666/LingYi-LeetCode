---
title: "1337. 矩阵中战斗力最弱的K行"
aliases: ["yiduobo的每日leetcode 1337.矩阵中战斗力最弱的K行"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/395619097"
zhihu_id: "395619097"
zhihu_title: "yiduobo的每日leetcode 1337.矩阵中战斗力最弱的K行"
question_id: "1337"
question: "矩阵中战斗力最弱的K行"
problem_url: "https://leetcode.cn/problems/the-k-weakest-rows-in-a-matrix/"
created: "2021-08-02T22:58:10+08:00"
updated: "2021-08-02T22:58:10+08:00"
upvotes: 2
comments: 0
---

# 1337. 矩阵中战斗力最弱的K行

> **[yiduobo的每日leetcode 1337.矩阵中战斗力最弱的K行](https://zhuanlan.zhihu.com/p/395619097) · 知乎 · 2021-08-02 · 赞同 2**
> 力扣：[1337. 矩阵中战斗力最弱的K行](https://leetcode.cn/problems/the-k-weakest-rows-in-a-matrix/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1337.矩阵中战斗力最弱的K行

[力扣](https://leetcode-cn.com/problems/the-k-weakest-rows-in-a-matrix/)

比较基础的题目，统计每一行中1的数目，从小到大排序后输出行号即可。

最后附上python代码：

```python
class Solution(object):
    def kWeakestRows(self, mat, k):
        """
        :type mat: List[List[int]]
        :type k: int
        :rtype: List[int]
        """

        cnt_list = []
        for index, line in enumerate(mat):
            cnt_list.append([sum(line), index])
        
        return [x[1] for x in sorted(cnt_list, key=lambda d:(d[0], d[1]))[:k]]
```
