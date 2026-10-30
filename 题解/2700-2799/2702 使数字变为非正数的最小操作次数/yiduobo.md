---
title: "2702. 使数字变为非正数的最小操作次数"
aliases: ["yiduobo的每日leetcode 2702.使数字变为非正数的最小操作次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/650750189"
zhihu_id: "650750189"
zhihu_title: "yiduobo的每日leetcode 2702.使数字变为非正数的最小操作次数"
question_id: "2702"
question: "使数字变为非正数的最小操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-make-numbers-non-positive/"
created: "2023-08-18T02:52:01+08:00"
updated: "2023-08-18T02:52:01+08:00"
upvotes: 0
comments: 0
---

# 2702. 使数字变为非正数的最小操作次数

> **[yiduobo的每日leetcode 2702.使数字变为非正数的最小操作次数](https://zhuanlan.zhihu.com/p/650750189) · 知乎 · 2023-08-18 · 赞同 0**
> 力扣：[2702. 使数字变为非正数的最小操作次数](https://leetcode.cn/problems/minimum-operations-to-make-numbers-non-positive/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2702.使数字变为非正数的最小操作次数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-operations-to-make-numbers-non-positive/description/)

首先注意到题目保证了y小于x，那么在这里很容想到一种贪心的做法，就是让当前剩余的最大值减去x，让其他的数减去y。不过碍于本题的数据规模较大，直接按这个贪心的思路逐步模拟肯定是行不通的，不过可以计算当前最大值需要多少次操作才会小于等于当前的次大值来进行批量操作，但是这里涉及到了相同值的多次处理，细节比较繁杂。

除此之外，还有一种比较省心的做法就是二分答案。执行操作的次数越多，就越有可能让所有数都小于等于0，因此是符合二分的性质的。

对于当前二分到的值mid，表示一共会进行mid次减法，也就是说一共只有mid个x可以减，其他时候都只能减去y。那么在这里就可以一趟遍历，计算出将数组中的每个数在mid次操作中减到小于等于0至少需要使用多少次x。若某个数在减去mid次x之后依然大于0，或者所有数都减到小于等于0所需的x数量大于mid，那么就说明mid次太少了，此时需要更新二分下界，否则更新二分上界。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, x, y):
        """
        :type nums: List[int]
        :type x: int
        :type y: int
        :rtype: int
        """

        left = 1
        right = max(nums) / y + 1
        while left < right:
            mid = (left + right) / 2
            cnt = 0
            for v in nums:
                diff = v - mid * y
                if diff > 0:
                    r = diff / (x - y)
                    if diff % (x - y) != 0:
                        r += 1
                
                    cnt += r
            
            if cnt <= mid:
                right = mid
            else:
                left = mid + 1
        
        return left
```
