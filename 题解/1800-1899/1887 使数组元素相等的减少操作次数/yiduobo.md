---
title: "1887. 使数组元素相等的减少操作次数"
aliases: ["yiduobo的每日leetcode 1887.使数组元素相等的减少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/滑动窗口与双指针", "题单/滑动窗口与双指针/六-分组循环"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/477848438"
zhihu_id: "477848438"
zhihu_title: "yiduobo的每日leetcode 1887.使数组元素相等的减少操作次数"
question_id: "1887"
question: "使数组元素相等的减少操作次数"
problem_url: "https://leetcode.cn/problems/reduction-operations-to-make-the-array-elements-equal/"
difficulty: "Medium"
rating: 1428
created: "2022-03-08T22:42:28+08:00"
updated: "2022-03-08T22:42:28+08:00"
upvotes: 1
comments: 0
---

# 1887. 使数组元素相等的减少操作次数

> **[yiduobo的每日leetcode 1887.使数组元素相等的减少操作次数](https://zhuanlan.zhihu.com/p/477848438) · 知乎 · 2022-03-08 · 赞同 1**
> 力扣：[1887. 使数组元素相等的减少操作次数](https://leetcode.cn/problems/reduction-operations-to-make-the-array-elements-equal/) · Medium · 灵茶山艾府：[排序后遍历，简洁写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1887.使数组元素相等的减少操作次数

[力扣](https://leetcode-cn.com/problems/reduction-operations-to-make-the-array-elements-equal/)

某一时刻，若数组中的最大值出现了k次，那么就需要执行k次操作让这些数变成次大值，也就是说每次操作都需要直到当前数组中最大值出现的次数。于是可以使用一个变量cnt来维护这个出现次数，并统计数组中每个数出现的次数，然后从大到小一趟遍历，使用当前cnt来更新答案。另外，由于操作后最大值变为了次大值，此时还需要用次大值出现的次数来更新cnt，以此类推。

最后附上python代码：

```python
class Solution(object):
    def reductionOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        res = 0
        cnt = 0
        for num in sorted(cnt_dict.keys(), reverse=True):
            res += cnt
            cnt += cnt_dict[num]
        
        return res
```
