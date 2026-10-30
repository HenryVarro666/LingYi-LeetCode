---
title: "738. 单调递增的数字"
aliases: ["yiduobo的每日leetcode 738.单调递增的数字"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/336648886"
zhihu_id: "336648886"
zhihu_title: "yiduobo的每日leetcode 738.单调递增的数字"
question_id: "738"
question: "单调递增的数字"
problem_url: "https://leetcode.cn/problems/monotone-increasing-digits/"
created: "2020-12-13T19:35:23+08:00"
updated: "2020-12-13T19:35:23+08:00"
upvotes: 0
comments: 0
---

# 738. 单调递增的数字

> **[yiduobo的每日leetcode 738.单调递增的数字](https://zhuanlan.zhihu.com/p/336648886) · 知乎 · 2020-12-13 · 赞同 0**
> 力扣：[738. 单调递增的数字](https://leetcode.cn/problems/monotone-increasing-digits/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

738.单调递增的数字

[力扣](https://leetcode-cn.com/problems/monotone-increasing-digits/)

题目要求找出小于等于N，且各位数字单调递增的最大整数，那么若N自身各位数字就是单调递增的，那么答案就是N，否则就需要变更其中的某些位上的数字。

不妨设当前第p位上的数字nums[p] > nums[p + 1]，由于题目要求最终答案必须小于等于N，那么我们不能将nums[p + 1]变大，因此只能将nums[p]变小。为了使得答案尽可能大，我们可以将nums[p]减1，然后从nums[p + 1]开始到末尾全部填上9，此时可以保证从nums[p]开始往后各位数字都是单调递增的，且此时数字是最大的。又由于一开始假设中nums[p] > nums[p + 1]，这里的大于号确定了nums[p]必然是大于等于1的，因此将nums[p]减一是没有任何问题的。

有了上面的结论，我们就只需要从最高位开始往后扫描，找出第一个满足条件的p，然后将nums[p]减1，后面全部填上9，就可以保证从p这一开始往后的所有位都满足条件。但是这样做有一个问题就是此时nums[p]变小了，可能使得nums[p - 1]不再小于等于nums[p]。若此时的nums[p - 1] > nums[p]，那么我们可以执行同样的操作，将nums[p - 1]减1，然后将nums[p]变为9，依次向前类推。

那么此时的做法就是：

1、从高位往低位开始一趟扫描，找出第一个满足nums[p] > nums[p + 1]的位置p。若找不到，说明N本身就是单调递增的，直接返回N即可。

2、从第p位开始往前扫描，若当前nums[index] > nums[index + 1]，那么将nums[index]减1，然后将后面的部分全部置为9，然后继续向前考察第index - 1位，直到当前的index满足nums[index] \<\= nums[index + 1]。此时整个nums数组就满足题目的要求了。

最后附上python代码：

```python
class Solution(object):
    def monotoneIncreasingDigits(self, N):
        """
        :type N: int
        :rtype: int
        """

        s = str(N)
        p = 0
        while p < len(s) - 1 and s[p] <= s[p + 1]:
            p += 1
        
        if p == len(s) - 1:
            return N
        
        while p > 0 and int(s[p]) - 1 < int(s[p - 1]):
            p -= 1

        res = str(int(s[:p + 1]) - 1) + '9' * (len(s) - p - 1)

        return int(res)
```
