---
title: "3843. 频率唯一的第一个元素"
aliases: ["yiduobo的每日leetcode 3843.频率唯一的第一个元素"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2010153530841919669"
zhihu_id: "2010153530841919669"
zhihu_title: "yiduobo的每日leetcode 3843.频率唯一的第一个元素"
question_id: "3843"
question: "频率唯一的第一个元素"
problem_url: "https://leetcode.cn/problems/first-element-with-unique-frequency/"
difficulty: "Medium"
created: "2026-03-01T01:44:46+08:00"
updated: "2026-03-01T01:44:52+08:00"
upvotes: 0
comments: 0
---

# 3843. 频率唯一的第一个元素

> **[yiduobo的每日leetcode 3843.频率唯一的第一个元素](https://zhuanlan.zhihu.com/p/2010153530841919669) · 知乎 · 2026-03-01 · 赞同 0**
> 力扣：[3843. 频率唯一的第一个元素](https://leetcode.cn/problems/first-element-with-unique-frequency/) · Medium · 灵茶山艾府：[统计出现次数的出现次数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3843.频率唯一的第一个元素

<https://leetcode.cn/problems/first-element-with-unique-frequency/description/>

题目给出一个整数数组nums，要求找出其中从左到右第一个出现频率与众不同的元素。若不存在这样的元素，则返回-1。

先对nums进行一趟遍历，使用哈希表freq统计nums中每种元素出现的次数。

接下来再遍历freq中的每个值f，使用哈希表的哈希表freq_freq统计每种f出现的次数。

最后再对nums进行一趟遍历，对于当前遍历到的元素v，若freq\[v\]仅出现过一次，也就是freq_freq\[freq\[v\]\]为1，那么就返回v。若遍历完成还没找到答案，则返回-1。

最后附上python代码：

```python
class Solution(object):
    def firstUniqueFreq(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        freq = {}
        freq_freq = {}

        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        for f in freq.values():
            freq_freq[f] = freq_freq.get(f, 0) + 1
        
        for v in nums:
            if freq_freq[freq[v]] == 1:
                return v
        
        return -1
```
