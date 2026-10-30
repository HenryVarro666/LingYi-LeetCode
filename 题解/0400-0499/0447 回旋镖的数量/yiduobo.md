---
title: "447. 回旋镖的数量"
aliases: ["yiduobo的每日leetcode 447.回旋镖的数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/209033691"
zhihu_id: "209033691"
zhihu_title: "yiduobo的每日leetcode 447.回旋镖的数量"
question_id: "447"
question: "回旋镖的数量"
problem_url: "https://leetcode.cn/problems/number-of-boomerangs/"
difficulty: "Medium"
created: "2020-08-31T21:54:57+08:00"
updated: "2020-08-31T21:54:57+08:00"
upvotes: 0
comments: 0
---

# 447. 回旋镖的数量

> **[yiduobo的每日leetcode 447.回旋镖的数量](https://zhuanlan.zhihu.com/p/209033691) · 知乎 · 2020-08-31 · 赞同 0**
> 力扣：[447. 回旋镖的数量](https://leetcode.cn/problems/number-of-boomerangs/) · Medium · 灵茶山艾府：[简洁写法，附相似题目（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

447.回旋镖的数量<https://leetcode-cn.com/problems/number-of-boomerangs/>

题目要求找出所有的三元组(i，j，k)，使得i到j的距离等于i到k的距离。我的做法是先枚举点i，然后计算其他所有点到点i的距离，并将这个距离保存在dict中。不妨设到点i距离为dis的点一共有n个，那么这n个点两两组合，然后再带上点i就能形成一个符合条件的元组，那么距离为dis的回旋镖一共有n \* (n - 1)组。

由于这里的坐标都是整数，因此在计算距离时可以不开方，这样就不会产生丢失精度的问题。

最后附上python代码：

```python
class Solution(object):
    def numberOfBoomerangs(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        ans = 0
        for x1, y1 in points:
            dis_dict = {}
            for x2, y2 in points:
                if x1 == x2 and y1 == y2:
                    continue
                dis = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)
                dis_dict[dis] = dis_dict.get(dis, 0) + 1
            
            for dis, cnt in dis_dict.items():
                ans += cnt * (cnt - 1)

        return ans
```
