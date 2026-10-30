---
title: "1133. 最大唯一数"
aliases: ["yiduobo的每日leetcode 1133.最大唯一数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/610557178"
zhihu_id: "610557178"
zhihu_title: "yiduobo的每日leetcode 1133.最大唯一数"
question_id: "1133"
question: "最大唯一数"
problem_url: "https://leetcode.cn/problems/largest-unique-number/"
created: "2023-03-01T21:34:16+08:00"
updated: "2023-03-01T21:34:16+08:00"
upvotes: 0
comments: 0
---

# 1133. 最大唯一数

> **[yiduobo的每日leetcode 1133.最大唯一数](https://zhuanlan.zhihu.com/p/610557178) · 知乎 · 2023-03-01 · 赞同 0**
> 力扣：[1133. 最大唯一数](https://leetcode.cn/problems/largest-unique-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1133.最大唯一数

[力扣](https://leetcode.cn/problems/largest-unique-number/)

一趟遍历，使用哈希表统计每个数出现的次数，然后从大到小遍历这些数，找到第一个出现次数为1的数即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def largestUniqueNumber(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        cnt = [0] * 1001
        for num in nums:
            cnt[num] += 1
        
        for num in range(1000, -1, -1):
            if cnt[num] == 1:
                return num
        
        return -1
```
