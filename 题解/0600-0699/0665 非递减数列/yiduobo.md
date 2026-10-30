---
title: "665. 非递减数列"
aliases: ["yiduobo的每日leetcode 665.非递减数列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/289694644"
zhihu_id: "289694644"
zhihu_title: "yiduobo的每日leetcode 665.非递减数列"
question_id: "665"
question: "非递减数列"
problem_url: "https://leetcode.cn/problems/non-decreasing-array/"
created: "2020-11-12T23:21:12+08:00"
updated: "2020-11-12T23:21:12+08:00"
upvotes: 0
comments: 0
---

# 665. 非递减数列

> **[yiduobo的每日leetcode 665.非递减数列](https://zhuanlan.zhihu.com/p/289694644) · 知乎 · 2020-11-12 · 赞同 0**
> 力扣：[665. 非递减数列](https://leetcode.cn/problems/non-decreasing-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

665.非递减数列

[力扣](https://leetcode-cn.com/problems/non-decreasing-array/)

贪心法的题目。对于nums[index]，若其小于nums[index - 1]，那么我们需要改变其中的一个数。为了改变后满足nums[index + 1]大于等于nums[index]，因此我们在这里希望nums[index]尽量小，于是：

1、如果可以通过改变nums[index - 1]达成条件，那么就改变nums[index - 1]，而nums[index]维持原样。

2、若修改nums[index - 1]之后，nums[index - 1]与nums[index - 2]发生冲突，那么此时我们就只能修改nums[index]。为了使得nums[index]最小，且大于等于nums[index - 1]，因此我们应该将nums[index]其修改为nums[index - 1]。

有了上面的结论，我们就可以对nums从头到尾进行一趟扫描，若出现nums[index]小于nums[index - 1]的情况，则按照上面的结论进行修改，同时标记这次修改。若之后再次出现逆序的情况，且已经有了标记，那么就返回false。若成功扫描完整个数组，那么就返回true。

最后附上python代码：

```python
class Solution(object):
    def checkPossibility(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        now = nums[0]
        change = True
        for index in range(1, len(nums)):
            if nums[index] >= now:
                now = nums[index]
            elif change:
                if index == 1 or nums[index - 2] <= nums[index]:
                    now = nums[index]
                change = False
            else:
                return False

        return True
```
