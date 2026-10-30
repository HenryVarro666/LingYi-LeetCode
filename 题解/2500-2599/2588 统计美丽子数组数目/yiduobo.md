---
title: "2588. 统计美丽子数组数目"
aliases: ["yiduobo的每日leetcode 2588.统计美丽子数组数目"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/位运算", "题单/常用数据结构/一-前缀和", "题单/位运算/二-异或-XOR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/643220786"
zhihu_id: "643220786"
zhihu_title: "yiduobo的每日leetcode 2588.统计美丽子数组数目"
question_id: "2588"
question: "统计美丽子数组数目"
problem_url: "https://leetcode.cn/problems/count-the-number-of-beautiful-subarrays/"
difficulty: "Medium"
rating: 1697
created: "2023-07-13T03:22:47+08:00"
updated: "2023-07-13T03:22:47+08:00"
upvotes: 0
comments: 0
---

# 2588. 统计美丽子数组数目

> **[yiduobo的每日leetcode 2588.统计美丽子数组数目](https://zhuanlan.zhihu.com/p/643220786) · 知乎 · 2023-07-13 · 赞同 0**
> 力扣：[2588. 统计美丽子数组数目](https://leetcode.cn/problems/count-the-number-of-beautiful-subarrays/) · Medium · 灵茶山艾府：[转化成 560 题（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2588.统计美丽子数组数目

[力扣](https://leetcode.cn/problems/count-the-number-of-beautiful-subarrays/)

题目给出的减去2^k这一操作，要求两个操作数的二进制表示的第k位上都是1，那么对于一个美丽子数组而言，其包含的所有数的二进制表示中，每一位出现的次数必然都是偶数。更进一步的，子数组中的数的异或值也同样为0。到了这里，题目就变成了找出数组中异或值为0的子数组数目。

对于这个问题，则可以将其转化为前缀异或进行求解。若前缀nums[:l]的异或值与nums[:r + 1]的异或值相同，那么就说明nums[l : r + 1]的异或值等于0。于是可以一趟遍历，使用一个哈希表cnt记录前缀中每种异或值出现的次数，那么对于当前遍历到的数v，先将其与已有的前缀异或值now进行异或操作，接下来使用cnt[now]更新答案，然后将cnt[now]加上1后继续向后遍历即可。

最后附上python代码：

```python
class Solution(object):
    def beautifulSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        cnt = {0 : 1}
        now = 0
        res = 0
        for v in nums:
            now ^= v
            res += cnt.get(now, 0)
            cnt[now] = cnt.get(now, 0) + 1
        
        return res
```
