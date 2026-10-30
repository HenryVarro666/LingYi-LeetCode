---
title: "398. 随机数索引"
aliases: ["yiduobo的每日leetcode 398.随机数索引"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/180509659"
zhihu_id: "180509659"
zhihu_title: "yiduobo的每日leetcode 398.随机数索引"
question_id: "398"
question: "随机数索引"
problem_url: "https://leetcode.cn/problems/random-pick-index/"
created: "2020-08-11T20:38:11+08:00"
updated: "2020-08-11T20:38:11+08:00"
upvotes: 0
comments: 0
---

# 398. 随机数索引

> **[yiduobo的每日leetcode 398.随机数索引](https://zhuanlan.zhihu.com/p/180509659) · 知乎 · 2020-08-11 · 赞同 0**
> 力扣：[398. 随机数索引](https://leetcode.cn/problems/random-pick-index/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

398.随机数索引<https://leetcode-cn.com/problems/random-pick-index/>

又是随机抽样的题目，可以用之前相同的蓄水池抽样来解决（传送门在这里[yiduobo：yiduobo的每日leetcode 382.链表随机节点](https://zhuanlan.zhihu.com/p/166411338)）。

最后附上python代码：

```python
import random

class Solution(object):

    def __init__(self, nums):
        """
        :type nums: List[int]
        """
        self.nums = nums

    def pick(self, target):
        """
        :type target: int
        :rtype: int
        """
        pos = None
        cnt = 0

        for index, num in enumerate(self.nums):
            if num == target:
                if pos is None:
                    pos = index
                else:
                    if random.randint(0, cnt) == 0:
                        pos = index
                cnt += 1

        return pos

# Your Solution object will be instantiated and called as such:
# obj = Solution(nums)
# param_1 = obj.pick(target)
```
