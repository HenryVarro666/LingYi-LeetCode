---
title: "1877. 数组中最大数对和的最小值"
aliases: ["yiduobo的每日leetcode 1877.数组中最大数对和的最小值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/476082643"
zhihu_id: "476082643"
zhihu_title: "yiduobo的每日leetcode 1877.数组中最大数对和的最小值"
question_id: "1877"
question: "数组中最大数对和的最小值"
problem_url: "https://leetcode.cn/problems/minimize-maximum-pair-sum-in-array/"
difficulty: "Medium"
rating: 1301
created: "2022-03-05T00:30:25+08:00"
updated: "2022-03-05T00:30:25+08:00"
upvotes: 0
comments: 0
---

# 1877. 数组中最大数对和的最小值

> **[yiduobo的每日leetcode 1877.数组中最大数对和的最小值](https://zhuanlan.zhihu.com/p/476082643) · 知乎 · 2022-03-05 · 赞同 0**
> 力扣：[1877. 数组中最大数对和的最小值](https://leetcode.cn/problems/minimize-maximum-pair-sum-in-array/) · Medium · 灵茶山艾府：[证明，交换论证法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1877.数组中最大数对和的最小值

[阻断页面](https://leetcode-cn.com/problems/minimize-maximum-pair-sum-in-array/)

为了使得最大数对和最小，那么数组中最大的数就应该跟数组中最小的数配对，证明也很简单。不妨设当前数组中的最大值和最小值分别为ma和mi，那么当ma不是与mi配对时，设x和y为数组中的任意两个数，且ma与x配对，mi与y配对，此时将会产生两个数对和ma + x以及mi + y。

在这里有mi + y \<\= x + y \<\= ma + x，也就是说这两个数对和中ma + x总是较大的那一个。

如果改成让ma和mi配对的话，得到的数对和将变为ma + mi以及x + y。

由于mi \<\= x，因此有ma + mi \<\= ma + x

又由于y \<\= ma，因此有x + y \<\= ma + x

因此在这里让ma和mi配对后肯定是比原始配对更优的

根据上面的结论，将数组中的最大值和最小值配对后，留下数组中新的最大值和最小值也同样符合上面的结论，因此在这里可以将数组先进行排序，然后两侧向中间两两配对，计算这些数对和并取其中的最大值作为答案即可。

最后附上python代码：

```python
class Solution(object):
    def minPairSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums = sorted(nums)
        n = len(nums)
        res = 0
        for index in range(n / 2):
            res = max(res, nums[index] + nums[n - index - 1])
        
        return res
```
