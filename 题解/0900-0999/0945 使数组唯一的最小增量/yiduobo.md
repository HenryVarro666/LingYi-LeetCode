---
title: "945. 使数组唯一的最小增量"
aliases: ["yiduobo的每日leetcode 945.使数组唯一的最小增量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/358794013"
zhihu_id: "358794013"
zhihu_title: "yiduobo的每日leetcode 945.使数组唯一的最小增量"
question_id: "945"
question: "使数组唯一的最小增量"
problem_url: "https://leetcode.cn/problems/minimum-increment-to-make-array-unique/"
created: "2021-03-21T19:34:44+08:00"
updated: "2021-03-21T19:34:44+08:00"
upvotes: 0
comments: 0
---

# 945. 使数组唯一的最小增量

> **[yiduobo的每日leetcode 945.使数组唯一的最小增量](https://zhuanlan.zhihu.com/p/358794013) · 知乎 · 2021-03-21 · 赞同 0**
> 力扣：[945. 使数组唯一的最小增量](https://leetcode.cn/problems/minimum-increment-to-make-array-unique/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

945.使数组唯一的最小增量

[力扣](https://leetcode-cn.com/problems/minimum-increment-to-make-array-unique/)

由于每次只能选择一个数增加1，那么对于一个数x而言，若其出现了k次，那么至少需要k - 1次操作，将k - 1个x变为x + 1，此时的x才是唯一的。另外，如果有小于x的数通过变换变成了x，那么则还需要额外的次数将这些数继续向上变化。

注意到这里的数范围在0到40000之间，那么我们可以使用一个dict储存每个数出现的次数，然后从0开始向上枚举直到39998。对于当前处理的x，若目前存在k个x且k大于1，那么就执行k - 1次操作，将k - 1个x变为x + 1，同时更新答案，并将dict中x + 1出现的次数加上k - 1。

当扫描完成后，0到39998出现的次数都只有一次，而39999可能出现多次。设39999出现k次，那么同样需要k - 1次操作，此时将得到k - 1个40000。继续向上执行操作，此时需要将k - 2个40000变为40001，依次类推直到k等于1为止，那么执行操作的次数为

(k - 1) + (k - 2) + ... + 1 \= (k - 1) \* k / 2

最后附上python代码：

```python
class Solution(object):
    def minIncrementForUnique(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        f = [0] * 40000
        for num in A:
            f[num] += 1
        
        res = 0
        for num in range(39999):
            if f[num] > 1:
                res += f[num] - 1
                f[num + 1] += f[num] - 1
        
        if f[-1] > 1:
            res += (f[-1] - 1) * f[-1] / 2
        
        return res
```
