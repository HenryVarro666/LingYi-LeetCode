---
title: "56. 合并区间"
aliases: ["yiduobo的每日leetcode 56.合并区间"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/sorting", "leetcode/sweep-line", "题单/常用数据结构", "题单/贪心算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/常用数据结构/二-差分", "题单/贪心算法/二-区间贪心", "题单/LeetCode-热题-100/普通数组", "题单/面试经典-150-题/区间"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/128126787"
zhihu_id: "128126787"
zhihu_title: "yiduobo的每日leetcode 56.合并区间"
question_id: "56"
question: "合并区间"
problem_url: "https://leetcode.cn/problems/merge-intervals/"
difficulty: "Medium"
created: "2020-04-09T22:58:13+08:00"
updated: "2020-04-09T22:58:13+08:00"
upvotes: 0
comments: 0
---

# 56. 合并区间

> **[yiduobo的每日leetcode 56.合并区间](https://zhuanlan.zhihu.com/p/128126787) · 知乎 · 2020-04-09 · 赞同 0**
> 力扣：[56. 合并区间](https://leetcode.cn/problems/merge-intervals/) · Medium · 灵茶山艾府：[三种方法：排序 / 差分数组 / 扫描线（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

56.合并区间<https://leetcode-cn.com/problems/merge-intervals/>

两个区间重叠的条件是，靠右的那个区间的左边界小于等于靠左的那个区间的右边界。

于是可以先把所有区间按左边界排序，接下以最左侧的区间为基准区间，往后遍历每个区间。

若当前区间的左边界小于等于基准区间的右边界，说明这两个区间重叠，那么有以下两种情况：

1、如果当前区间的右边界也小于等于基准区间的右边界，说明当前区间被基准区间包含，此时不需要做任何操作。

2、如果当前区间的右边界大于基准区间的右边界，那么合并当前区间与基准区间，即将基准区间的右边界更新为当前区间的右边界。

若当前区间的左边界大于基准区间的右边界，说明这两个区间不重叠，此时将基准区间加入答案，然后选择当前区间作为新的基准区间即可。

最后要记得将基准区间也加入到答案中。

排序的复杂度为O(nlogn)，合并的复杂度为O(n)，因此最终的时间复杂度为O(nlogn)。

最后附上python代码：

```python
class Solution(object):
    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        """

        if not intervals:
            return []

        intervals = sorted(intervals, key=lambda d:d[0])

        left = intervals[0][0]
        right = intervals[0][1]
        res = []

        for index, interval in enumerate(intervals):
            if interval[0] <= right:
                right = max(right, interval[1])
            else:
                res.append([left, right])
                left = interval[0]
                right = interval[1]

        res.append([left, right])
        return res
```
