---
title: "1940. 排序数组之间的最长公共子序列"
aliases: ["yiduobo的每日leetcode 1940.排序数组之间的最长公共子序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/array"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/623891120"
zhihu_id: "623891120"
zhihu_title: "yiduobo的每日leetcode 1940.排序数组之间的最长公共子序列"
question_id: "1940"
question: "排序数组之间的最长公共子序列"
problem_url: "https://leetcode.cn/problems/longest-common-subsequence-between-sorted-arrays/"
difficulty: "Medium"
created: "2023-04-22T02:49:22+08:00"
updated: "2023-04-22T02:49:22+08:00"
upvotes: 0
comments: 0
---

# 1940. 排序数组之间的最长公共子序列

> **[yiduobo的每日leetcode 1940.排序数组之间的最长公共子序列](https://zhuanlan.zhihu.com/p/623891120) · 知乎 · 2023-04-22 · 赞同 0**
> 力扣：[1940. 排序数组之间的最长公共子序列](https://leetcode.cn/problems/longest-common-subsequence-between-sorted-arrays/) · Medium · 灵茶山艾府：[Go 统计每个元素的出现次数](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1940.排序数组之间的最长公共子序列

[力扣](https://leetcode.cn/problems/longest-common-subsequence-between-sorted-arrays/)

最终答案一定完整地出现在了array[0]中，因此可以遍历一趟array[0]，检测其中的每个数字是否都在其他的array中出现过。

由于所有array都是有序的，因此在这里对每个array维护一个p，其中p\[i\]表示中满足array\[i\]\[p\[i\]\]大于等于当前遍历到的array\[0\]中的数值的最小下标。

随着array[0]的遍历，目标值是逐渐增大的，因此每个数组对应的p也是逐渐增大的，在这里利用单调性就可以在均摊O(1)的时间内完成单个数组对应的p的更新，从而在O(n)的时间内判断当前遍历到的数是否也存在于其他数组中，这里的n是数组的总数。

最后附上python代码：

```python
class Solution(object):
    def longestCommonSubsequence(self, arrays):
        """
        :type arrays: List[List[int]]
        :rtype: List[int]
        """

        n = len(arrays)
        p = [0] * n
        res = []
        while True:
            target = arrays[0][p[0]]
            end_flag = False
            same_flag = True
            for index in range(1, n):
                while p[index] < len(arrays[index]) and arrays[index][p[index]] < target:
                    p[index] += 1
                
                if p[index] == len(arrays[index]):
                    end_flag = True
                    break
                
                if arrays[index][p[index]] != target:
                    same_flag = False
                    break
            
            if end_flag:
                break
            
            if same_flag:
                res.append(target)
            
            p[0] += 1
            if p[0] == len(arrays[0]):
                break
        
        return res
```
