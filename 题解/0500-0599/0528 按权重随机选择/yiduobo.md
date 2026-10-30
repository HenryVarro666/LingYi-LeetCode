---
title: "528. 按权重随机选择"
aliases: ["yiduobo的每日leetcode 528.按权重随机选择"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/261165823"
zhihu_id: "261165823"
zhihu_title: "yiduobo的每日leetcode 528.按权重随机选择"
question_id: "528"
question: "按权重随机选择"
problem_url: "https://leetcode.cn/problems/random-pick-with-weight/"
created: "2020-10-04T23:14:24+08:00"
updated: "2020-10-04T23:14:24+08:00"
upvotes: 0
comments: 0
---

# 528. 按权重随机选择

> **[yiduobo的每日leetcode 528.按权重随机选择](https://zhuanlan.zhihu.com/p/261165823) · 知乎 · 2020-10-04 · 赞同 0**
> 力扣：[528. 按权重随机选择](https://leetcode.cn/problems/random-pick-with-weight/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

不小心塌了这一题，今天补上。

528.按权重随机选择<https://leetcode-cn.com/problems/random-pick-with-weight/>

对于w中的权重，我们可以看成有数字标记的小球。例如样例中的W\=[1,3]，可以看成一个标记了数字0的小球，以及3个标记了数字1的小球。那么我们现在的任务就是从这些小球中等概率地选择一个，并返回其标记。

我们可以通过计算W中权重之和，sum，然后从0到sum-1直接随机选择一个数，找到其对应的小球即可。一种可行的做法是将小球按顺序进行编号，例如上面的W\=[1,3]，第0个小球为标记为0的小球，第1、2、3个小球都是标记为1的小球，那么我们就可以通过计算前缀和来确认每种标记的小球所在区间的左右边界。又因为这个边界是单调递增的，所有可以使用二分查找来确定随机到的小球是哪一个。

最后附上python代码：

```python
class Solution(object):

    def __init__(self, w):
        """
        :type w: List[int]
        """
        self.sum_list = [w[0]]
        for index in range(1, len(w)):
            self.sum_list.append(self.sum_list[-1] + w[index])

    def pickIndex(self):
        """
        :rtype: int
        """
        pos = random.randint(0, self.sum_list[-1] - 1)
        l = 0
        r = len(self.sum_list) - 1
        while l < r:
            mid = (l + r) >> 1
            if pos >= self.sum_list[mid]:
                l = mid + 1
            else:
                r = mid
        return l

# Your Solution object will be instantiated and called as such:
# obj = Solution(w)
# param_1 = obj.pickIndex()
```
