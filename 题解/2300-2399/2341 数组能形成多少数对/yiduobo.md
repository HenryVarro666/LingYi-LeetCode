---
title: "2341. 数组能形成多少数对"
aliases: ["yiduobo的每日leetcode 2341.数组能形成多少数对"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/560027671"
zhihu_id: "560027671"
zhihu_title: "yiduobo的每日leetcode 2341.数组能形成多少数对"
question_id: "2341"
question: "数组能形成多少数对"
problem_url: "https://leetcode.cn/problems/maximum-number-of-pairs-in-array/"
difficulty: "Easy"
created: "2022-08-31T23:58:08+08:00"
updated: "2022-08-31T23:58:08+08:00"
upvotes: 0
comments: 0
---

# 2341. 数组能形成多少数对

> **[yiduobo的每日leetcode 2341.数组能形成多少数对](https://zhuanlan.zhihu.com/p/560027671) · 知乎 · 2022-08-31 · 赞同 0**
> 力扣：[2341. 数组能形成多少数对](https://leetcode.cn/problems/maximum-number-of-pairs-in-array/) · Easy · 灵茶山艾府：[哈希表](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2341.数组能形成多少数对

[力扣](https://leetcode.cn/problems/maximum-number-of-pairs-in-array/)

一趟遍历，使用哈希表统计每个数出现的次数。接下来对于每种数，设其出现了cnt次，由于两个形成一对，那么一共可以形成cnt / 2对，同时又cnt % 2个落单的数，使用这两个值更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def numberOfPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        res = [0, 0]
        for cnt in cnt_dict.values():
            res[0] += cnt / 2
            res[1] += cnt % 2
        
        return res
```
