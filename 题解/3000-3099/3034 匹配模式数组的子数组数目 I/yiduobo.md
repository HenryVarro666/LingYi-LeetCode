---
title: "3034. 匹配模式数组的子数组数目I & 3036. 匹配模式数组的子数组数目II"
aliases: ["yiduobo的每日leetcode 3034.匹配模式数组的子数组数目I && 3036.匹配模式数组的子数组数目II", "3034. 匹配模式数组的子数组数目I", "3036. 匹配模式数组的子数组数目II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string-matching", "leetcode/hard", "题单/字符串", "题单/字符串/一-KMP-前缀的后缀"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/695651523"
zhihu_id: "695651523"
zhihu_title: "yiduobo的每日leetcode 3034.匹配模式数组的子数组数目I && 3036.匹配模式数组的子数组数目II"
question_id: ["3034", "3036"]
question: ["匹配模式数组的子数组数目 I", "匹配模式数组的子数组数目 II"]
problem_url: ["https://leetcode.cn/problems/number-of-subarrays-that-match-a-pattern-i/", "https://leetcode.cn/problems/number-of-subarrays-that-match-a-pattern-ii/"]
difficulty: ["Medium", "Hard"]
rating: 1895
created: "2024-05-02T03:04:34+08:00"
updated: "2024-05-02T03:04:34+08:00"
upvotes: 1
comments: 0
---

# 3034. 匹配模式数组的子数组数目I & 3036. 匹配模式数组的子数组数目II

> **[yiduobo的每日leetcode 3034.匹配模式数组的子数组数目I && 3036.匹配模式数组的子数组数目II](https://zhuanlan.zhihu.com/p/695651523) · 知乎 · 2024-05-02 · 赞同 1**
> 力扣：[3034. 匹配模式数组的子数组数目 I](https://leetcode.cn/problems/number-of-subarrays-that-match-a-pattern-i/) · Medium · 灵茶山艾府：[两种 O(n) 做法：KMP / Z函数（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[3036. 匹配模式数组的子数组数目 II](https://leetcode.cn/problems/number-of-subarrays-that-match-a-pattern-ii/) · Hard · 灵茶山艾府：[两种方法：KMP / Z函数（Python/Java/C++/Go）](../3036%20匹配模式数组的子数组数目%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3034.匹配模式数组的子数组数目I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-subarrays-that-match-a-pattern-i/description/)

3036.匹配模式数组的子数组数目II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-subarrays-that-match-a-pattern-ii/description/)

两题的题设相同，第二题的数据规模较大。

如果现根据题目中nums数组相邻元素的大小关系将其转化成由-1、0、1构成的数组，那么问题就变成了非常标准的模式匹配问题，直接套用kmp算法就行了。

kmp算法相关可以参考之前的28题：

[yiduobo：yiduobo的每日leetcode 28.实现 strStr()](https://zhuanlan.zhihu.com/p/117670077)

最后附上python代码：

```python
class Solution(object):
    def countMatchingSubarrays(self, nums, pattern):
        """
        :type nums: List[int]
        :type pattern: List[int]
        :rtype: int
        """

        f = [0]
        p = 0
        for index in range(1, len(pattern)):
            while p and pattern[p] != pattern[index]:
                p = f[p - 1]
            if pattern[p] == pattern[index]:
                p += 1
            f.append(p)
        
        res = 0
        p = 0
        for index in range(1, len(nums)):
            if nums[index] > nums[index - 1]:
                v = 1
            elif nums[index] < nums[index - 1]:
                v = -1
            else:
                v = 0
            
            while p and v != pattern[p]:
                p = f[p - 1]
            if pattern[p] == v:
                p += 1
                if p == len(pattern):
                    res += 1
                    p = f[p - 1]
        
        return res
```
