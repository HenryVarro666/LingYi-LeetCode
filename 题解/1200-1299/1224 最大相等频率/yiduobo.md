---
title: "1224. 最大相等频率"
aliases: ["yiduobo的每日leetcode 1224.最大相等频率"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/383728568"
zhihu_id: "383728568"
zhihu_title: "yiduobo的每日leetcode 1224.最大相等频率"
question_id: "1224"
question: "最大相等频率"
problem_url: "https://leetcode.cn/problems/maximum-equal-frequency/"
created: "2021-06-24T23:08:07+08:00"
updated: "2021-06-24T23:08:07+08:00"
upvotes: 0
comments: 0
---

# 1224. 最大相等频率

> **[yiduobo的每日leetcode 1224.最大相等频率](https://zhuanlan.zhihu.com/p/383728568) · 知乎 · 2021-06-24 · 赞同 0**
> 力扣：[1224. 最大相等频率](https://leetcode.cn/problems/maximum-equal-frequency/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1224.最大相等频率

[力扣](https://leetcode-cn.com/problems/maximum-equal-frequency/)

题目要求找到最长的合法前缀，那么一个自然的想法就是从后向前，每一轮移除最后一个数，然后判断当前前缀数组是否符合要求。

我们可以先使用num_dict统计出每个数字出现的次数，然后将这些次数加入到cnt_dict当中方便后续判断前缀数组是否符合要求。接下来每一轮将最后一个数移除，此时我们可以很快更新num_dict以及cnt_dict。

接下来我们需要想办法根据num_dict以及cnt_dict判断当前剩下的数组是否符合要求，那么有以下几种情况：

1、若此时cnt_dict的长度为1，说明此时数组中所有的数出现的次数都相同，那么若此时数组中所有的数都恰好只出现了1次，或者说数组中的所有数都相同，那么就是符合要求的。对应到cnt_dict上，就是cnt_dict中的key只有1，或者cnt_dict中唯一的value就是1。

2、若此时cnt_dict的长度为2，说明此时数组中存在两种不同的出现次数，我们不妨设这两种次数分别为cnt1和cnt2，且cnt1 > cnt2。那么此时：

2-1）cnt1对应的数只有一个，设为x。若我们从数组中删去一个x之后，x的出现次数就变味了cnt1 - 1。若此时的cnt1 - 1恰好等于cnt2，那么我们从数组中删去一个x之后剩下数的出现次数就相等了，说明符合要求。

对应到cnt_dict上，就是cnt_dict[cnt1] \= 1，且cnt1 \= cnt2 + 1

2-2) cnt2对应的数只有一个，设为y。若y在数组中仅出现一次，那么我们可以通过删去y，使得数组中剩下数的出现次数相等。

对应到cnt_dict上，就是cnt_dict[cnt2] \= 1，且cnt2 \= 1

除此之外，其他情况下都是不合法的，此时则应当继续向前扫描。

最后附上python代码：

```python
class Solution(object):
    def maxEqualFreq(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        num_dict = {}
        cnt_dict = {}
        for num in nums:
            num_dict[num] = num_dict.get(num, 0) + 1
        
        for cnt in num_dict.values():
            cnt_dict[cnt] = cnt_dict.get(cnt, 0) + 1

        n = len(nums)
        if self.check(cnt_dict):
            return n

        res = n
        for index in range(n - 1, -1, -1):
            cnt = num_dict[nums[index]]
            num_dict[nums[index]] -= 1
            res -= 1
            cnt_dict[cnt] -= 1
            if cnt_dict[cnt] == 0:
                cnt_dict.pop(cnt)
            if cnt > 1:
                cnt_dict[cnt - 1] = cnt_dict.get(cnt - 1, 0) + 1
            if self.check(cnt_dict):
                return res

    def check(self, cnt_dict):
        if len(cnt_dict) == 1 and (cnt_dict.keys()[0] == 1 or cnt_dict.values()[0] == 1):
            return True

        if len(cnt_dict) == 2:
            cnt1, cnt2 = cnt_dict.keys()
            if cnt1 < cnt2:
                cnt1, cnt2 = cnt2, cnt1
            if cnt1 == cnt2 + 1 and cnt_dict[cnt1] == 1:
                return True
            if cnt2 == 1 and cnt_dict[cnt2] == 1:
                return True
        
        return False
```
