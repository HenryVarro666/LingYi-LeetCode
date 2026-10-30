---
title: "565. 数组嵌套"
aliases: ["yiduobo的每日leetcode 565.数组嵌套"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/266301466"
zhihu_id: "266301466"
zhihu_title: "yiduobo的每日leetcode 565.数组嵌套"
question_id: "565"
question: "数组嵌套"
problem_url: "https://leetcode.cn/problems/array-nesting/"
created: "2020-10-16T21:42:34+08:00"
updated: "2020-10-16T21:42:34+08:00"
upvotes: 0
comments: 0
---

# 565. 数组嵌套

> **[yiduobo的每日leetcode 565.数组嵌套](https://zhuanlan.zhihu.com/p/266301466) · 知乎 · 2020-10-16 · 赞同 0**
> 力扣：[565. 数组嵌套](https://leetcode.cn/problems/array-nesting/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

565.数组嵌套<https://leetcode-cn.com/problems/array-nesting/>

虽然题目描述的是数组嵌套，实际上就与之前做过的找循环是完全一样的题目。

从左往右一趟扫描，对于没有处理过的数字nums[index]，不断迭代同时标记迭代到的数字，直到最终回到index，统计这一轮中迭代的次数并更新答案即可。

由于题目保证数字范围在0到n - 1，因此我使用n作为已经被访问过的标记。

最后附上python代码：

```python
class Solution(object):
    def arrayNesting(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        res = 0

        for index in range(len(nums)):
            now = nums[index]
            if now == len(nums):
                continue
            cnt = 0
            nums[index] = len(nums)
            while now != len(nums):
                tmp = nums[now]
                nums[now] = len(nums)
                now = tmp
                cnt += 1
            
            res = max(res, cnt)

        return res
```
