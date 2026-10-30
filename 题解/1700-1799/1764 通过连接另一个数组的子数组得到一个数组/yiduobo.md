---
title: "1764. 通过连接另一个数组的子数组得到一个数组"
aliases: ["yiduobo的每日leetcode 1764.通过连接另一个数组的子数组得到一个数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/460499703"
zhihu_id: "460499703"
zhihu_title: "yiduobo的每日leetcode 1764.通过连接另一个数组的子数组得到一个数组"
question_id: "1764"
question: "通过连接另一个数组的子数组得到一个数组"
problem_url: "https://leetcode.cn/problems/form-array-by-concatenating-subarrays-of-another-array/"
created: "2022-01-21T22:43:20+08:00"
updated: "2022-01-21T22:43:20+08:00"
upvotes: 0
comments: 0
---

# 1764. 通过连接另一个数组的子数组得到一个数组

> **[yiduobo的每日leetcode 1764.通过连接另一个数组的子数组得到一个数组](https://zhuanlan.zhihu.com/p/460499703) · 知乎 · 2022-01-21 · 赞同 0**
> 力扣：[1764. 通过连接另一个数组的子数组得到一个数组](https://leetcode.cn/problems/form-array-by-concatenating-subarrays-of-another-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1764.通过连接另一个数组的子数组得到一个数组

[力扣](https://leetcode-cn.com/problems/form-array-by-concatenating-subarrays-of-another-array/)

由于题目要求答案必须满足是按照groups的先后顺序排布的，也就是说对于groups中的数组而言，应该尽可能靠前地去匹配nums。对于数组匹配问题，在这里可以视为字符串匹配，那么问题就变成了给出若干个字符串，依次与主字符串进行匹配。若能匹配上，那么就选择主字符串最靠前的位置进行匹配，然后将匹配位置的结束位置开始进行下一个字符串的匹配，直到全部匹配成功或者出现无法匹配的情况为止。

而对于字符串匹配问题，则可以采用kmp算法来进行优化。

最后附上python代码：

```python
class Solution(object):
    def canChoose(self, groups, nums):
        """
        :type groups: List[List[int]]
        :type nums: List[int]
        :rtype: bool
        """

        p = 0
        for group in groups:
            f = [0]
            pos = 0
            for num in group[1:]:
                while pos > 0 and num != group[pos]:
                    pos = f[pos - 1]
                if num == group[pos]:
                    pos += 1
                f.append(pos)
            
            pos = 0
            flag = False
            for index in range(p, len(nums)):
                while pos > 0 and nums[index] != group[pos]:
                    pos = f[pos - 1]
                if nums[index] == group[pos]:
                    pos += 1
                if pos == len(group):
                    flag = True
                    p = index + 1
                    break
            
            if not flag:
                return False
        
        return True
```
