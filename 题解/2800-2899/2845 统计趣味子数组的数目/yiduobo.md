---
title: "2845. 统计趣味子数组的数目"
aliases: ["yiduobo的每日leetcode 2845.统计趣味子数组的数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/660196150"
zhihu_id: "660196150"
zhihu_title: "yiduobo的每日leetcode 2845.统计趣味子数组的数目"
question_id: "2845"
question: "统计趣味子数组的数目"
problem_url: "https://leetcode.cn/problems/count-of-interesting-subarrays/"
difficulty: "Medium"
rating: 2073
created: "2023-10-09T03:08:57+08:00"
updated: "2023-10-09T03:08:57+08:00"
upvotes: 0
comments: 0
---

# 2845. 统计趣味子数组的数目

> **[yiduobo的每日leetcode 2845.统计趣味子数组的数目](https://zhuanlan.zhihu.com/p/660196150) · 知乎 · 2023-10-09 · 赞同 0**
> 力扣：[2845. 统计趣味子数组的数目](https://leetcode.cn/problems/count-of-interesting-subarrays/) · Medium · 灵茶山艾府：[前缀和，枚举右维护左（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2845.统计趣味子数组的数目

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/count-of-interesting-subarrays/description/)

按照题目描述，只有对modulo取模为k的元素才会被统计到趣味子数组的cnt中，因此在这里可以先根据nums中每个元素对modulo取模的结果是否为k将其变形为一个新的01数组score，接下来的任务就是找出score中1的个数模modulo等于k的子数组数目。

由于score是01数组，那么这里子数组中1的个数实际上就等价于子数组之和，而对于区间和问题很自然想到使用前缀和来进行处理。题目要求区间和对modulo取模为k，就可以转化成两个前缀和之差对modulo取模为k，但是这里较长的前缀和必须要大于等于k才行。

更具体的，对于某个前缀和now，若now >\= k，实际上要求的就是之前出现过的前缀和对modulo取模等于(now - k) % modulo的前缀数目。

对于这个问题，只需一趟遍历，使用哈希表记录对modulo取模后的前缀和出现的次数，然后一边计算当前前缀和更新答案，一边更新哈希表即可。

最后附上python代码：

```python
class Solution(object):
    def countInterestingSubarrays(self, nums, modulo, k):
        """
        :type nums: List[int]
        :type modulo: int
        :type k: int
        :rtype: int
        """

        score = [1 if v % modulo == k else 0 for v in nums]
        cnt = {0 : 1}
        res = 0
        now = 0
        for v in score:
            now += v
            if now >= k:
                res += cnt.get((now - k) % modulo, 0)
            
            cnt[now % modulo] = cnt.get(now % modulo, 0) + 1
        
        return res
```
