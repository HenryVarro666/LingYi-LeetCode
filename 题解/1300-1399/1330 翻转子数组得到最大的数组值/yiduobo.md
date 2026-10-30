---
title: "1330. 翻转子数组得到的最大数组值"
aliases: ["yiduobo的每日leetcode 1330.翻转子数组得到的最大数组值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "题单/数学算法", "题单/贪心算法", "题单/数学算法/七-杂项", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/394796743"
zhihu_id: "394796743"
zhihu_title: "yiduobo的每日leetcode 1330.翻转子数组得到的最大数组值"
question_id: "1330"
question: "翻转子数组得到最大的数组值"
problem_url: "https://leetcode.cn/problems/reverse-subarray-to-maximize-array-value/"
difficulty: "Hard"
rating: 2482
created: "2021-07-30T23:03:30+08:00"
updated: "2021-07-30T23:03:30+08:00"
upvotes: 1
comments: 1
---

# 1330. 翻转子数组得到的最大数组值

> **[yiduobo的每日leetcode 1330.翻转子数组得到的最大数组值](https://zhuanlan.zhihu.com/p/394796743) · 知乎 · 2021-07-30 · 赞同 1**
> 力扣：[1330. 翻转子数组得到最大的数组值](https://leetcode.cn/problems/reverse-subarray-to-maximize-array-value/) · Hard · 灵茶山艾府：[化简绝对值（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1330.翻转子数组得到的最大数组值

[力扣](https://leetcode-cn.com/problems/reverse-subarray-to-maximize-array-value/)

设数组的长度为n，不妨设我们翻转了i到j这一段，那么首先可以明确的是，翻转并不会影响到a[0]到a[i - 1]，以及a[j + 1]到a[n - 1]这一段，那么我们只需要考察原来的a[i - 1]到a[j]这一段的数组值的变化。

在翻转之前，数组值为

abs(a[i - 1] - a[i]) + abs(a[i] - a[i + 1]) + ... + abs(a[j - 1] - a[j]) + abs(a[j] - a[j + 1])

而翻转之后，数组值则为

abs(a[i - 1] - a[j]) + abs(a[j] - a[j - 1]) + ... + abs(a[i + 1] - a[i]) + abs(a[i] - a[j + 1])

可以发现，除了首位两组差值，中间的部分是完全相同的，因此实际上的变化就是

abs(a[i - 1] - a[j]) + abs(a[i] - a[j + 1]) - abs(a[i - 1] - a[i]) - abs(a[j] - a[j + 1])

这里需要特别注意的是，当i等于0时，是没有a[i - 1]这一项的。同样地，当j等于n - 1时，也没有a[j + 1]这一项，因此我们需要优先处理这两种特殊情况。

当i \= 0时，此时的差值为abs(a[0] - a[j + 1]) - abs(a[j] - a[j + 1])

当j \= n - 1时，此时的差值为abs(a[i - 1] - a[j]) - abs(a[i - 1] - a[i])

那么对于上面这两种特殊情况，可以一趟扫描，枚举对应的i和j，找出其中最大的变化值

接下来考察一般情况。当我们翻转了i到j这一段时，数组值的变化为

abs(a[i - 1] - a[j]) + abs(a[i] - a[j + 1]) - abs(a[i - 1] - a[i]) - abs(a[j] - a[j + 1])

这个形式与之前做过的某道计算曼哈顿距离的题目一样，做法同样是拆开绝对值符号。需要注意的是，这里四个绝对值中，abs(a[i - 1] - a[j])与abs(a[i] - a[j + 1])的符号是随着i和j的选择出现变化的，而abs(a[i - 1] - a[i])以及abs(a[j] - a[j + 1])的符合是不会变化的，那么拆开之后就有四种情况：

1、a[i - 1] - a[j] + a[i] - a[j + 1] - abs(a[i - 1] - a[i]) - abs(a[j] - a[j + 1])

2、a[i - 1] - a[j] - a[i] + a[j + 1] - abs(a[i - 1] - a[i]) - abs(a[j] - a[j + 1])

3、-a[i - 1] + a[j] + a[i] - a[j + 1] - abs(a[i - 1] - a[i]) - abs(a[j] - a[j + 1])

4、-a[i - 1] + a[j] - a[i] + a[j + 1] - abs(a[i - 1] - a[i]) - abs(a[j] - a[j + 1])

按照i和j分别整理起来，就有

1、(a[i - 1] + a[i] - abs(a[i - 1] - a[i])) - (a[j] + a[j + 1] + abs(a[j] - a[j + 1]))

2、(a[i - 1] - a[i] - abs(a[i - 1] - a[i])) - (a[j] - a[j + 1] + abs(a[j] - a[j + 1]))

3、(-a[i - 1] + a[i] - abs(a[i - 1] - a[i])) - (-a[j] + a[j + 1] + abs(a[j] - a[j +1]))

4、(-a[i - 1] - a[i] - abs(a[i - 1] - a[i])) - (-a[j] - a[j + 1] + abs(a[j] - a[j + 1]))

不妨设x[i] \= a[i] - a[i + 1]，y[i] \= a[i] + a[i + 1]，那么就有

1、(y[i - 1] - abs(x[i - 1])) - (y[j] + abs(x[j]))

2、(x[i - 1] - abs(x[i - 1])) - (x[j] + abs(x[j]))

3、(-x[i - 1] - abs(x[i - 1])) - (-x[j] + abs(x[j]))

4、(-y[i - 1] - abs(x[i - 1])) - (-y[j] + abs(x[j]))

我们的目标是找出一组i和j，那么我们可以一趟扫描，分别找出上面四个式子前半部分的最大值以及后半部分的最小值，分别设为ma[0]到ma[3]，以及mi[0]到mi[3]，那么最终答案就是

max(ma[0] - mi[0], ma[1] - mi[1], ma[2] - mi[2], ma[3] - mi[3])

这里的正确性证明比较复杂，简单来说可以认为若最大值中出现了违反绝对值符号的情况，那么此时将自动归于另一种合法的情况，也就是说最大值必然出现在符合绝对值符号的情况下。

最后附上python代码：

```python
class Solution(object):
    def maxValueAfterReverse(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        x = []
        y = []
        res = 0
        n = len(nums)
        for i in range(n - 1):
            x.append(nums[i] - nums[i + 1])
            y.append(nums[i] + nums[i + 1])
            res += abs(x[-1])
        
        tmp = res
        mi = [x[0] + abs(x[0]), -x[0] + abs(x[0]), y[0] + abs(x[0]), -y[0] + abs(x[0])]
        ma = [x[0] - abs(x[0]), -x[0] - abs(x[0]), y[0] - abs(x[0]), -y[0] - abs(x[0])]
        for i in range(1, n - 1):
            res = max(res, tmp + abs(nums[i + 1] - nums[0]) - abs(x[i]))
            res = max(res, tmp + abs(nums[-1] - nums[i - 1]) - abs(x[i - 1]))
            mi[0] = min(mi[0], x[i] + abs(x[i]))
            mi[1] = min(mi[1], -x[i] + abs(x[i]))
            mi[2] = min(mi[2], y[i] + abs(x[i]))
            mi[3] = min(mi[3], -y[i] + abs(x[i]))
            ma[0] = max(ma[0], x[i] - abs(x[i]))
            ma[1] = max(ma[1], -x[i] - abs(x[i]))
            ma[2] = max(ma[2], y[i] - abs(x[i]))
            ma[3] = max(ma[3], -y[i] - abs(x[i]))

        return max(res, tmp + max(ma[0] - mi[0], ma[1] - mi[1], ma[2] - mi[2], ma[3] - mi[3]))
```
