---
title: "1995. 统计特殊四元组"
aliases: ["yiduobo的每日leetcode 1995.统计特殊四元组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/500805076"
zhihu_id: "500805076"
zhihu_title: "yiduobo的每日leetcode 1995.统计特殊四元组"
question_id: "1995"
question: "统计特殊四元组"
problem_url: "https://leetcode.cn/problems/count-special-quadruplets/"
created: "2022-04-18T21:15:01+08:00"
updated: "2022-04-18T21:15:01+08:00"
upvotes: 0
comments: 0
---

# 1995. 统计特殊四元组

> **[yiduobo的每日leetcode 1995.统计特殊四元组](https://zhuanlan.zhihu.com/p/500805076) · 知乎 · 2022-04-18 · 赞同 0**
> 力扣：[1995. 统计特殊四元组](https://leetcode.cn/problems/count-special-quadruplets/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1995.统计特殊四元组

[力扣](https://leetcode-cn.com/problems/count-special-quadruplets/)

稍微转化一下就是四数之和问题，可以使用之前相同的方法来处理，具体做法可以参考

[yiduobo：yiduobo的每日leetcode 18.四数之和](https://zhuanlan.zhihu.com/p/115110040)

我在这里偷懒，直接使用了四次方的暴力算法。

最后附上python代码：

```python
class Solution(object):
    def countQuadruplets(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        res = 0

        for a in range(n - 3):
            for b in range(a + 1, n - 2):
                for c in range(b + 1, n - 1):
                    for d in range(c + 1, n):
                        if nums[a] + nums[b] + nums[c] == nums[d]:
                            res += 1
        
        return res
```
