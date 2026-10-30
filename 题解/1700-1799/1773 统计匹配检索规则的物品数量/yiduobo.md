---
title: "1773. 统计匹配检索规则的物品数量"
aliases: ["yiduobo的每日leetcode 1773.统计匹配检索规则的物品数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/461527431"
zhihu_id: "461527431"
zhihu_title: "yiduobo的每日leetcode 1773.统计匹配检索规则的物品数量"
question_id: "1773"
question: "统计匹配检索规则的物品数量"
problem_url: "https://leetcode.cn/problems/count-items-matching-a-rule/"
created: "2022-01-25T00:29:46+08:00"
updated: "2022-01-25T00:29:46+08:00"
upvotes: 0
comments: 0
---

# 1773. 统计匹配检索规则的物品数量

> **[yiduobo的每日leetcode 1773.统计匹配检索规则的物品数量](https://zhuanlan.zhihu.com/p/461527431) · 知乎 · 2022-01-25 · 赞同 0**
> 力扣：[1773. 统计匹配检索规则的物品数量](https://leetcode.cn/problems/count-items-matching-a-rule/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1773.统计匹配检索规则的物品数量

[力扣](https://leetcode-cn.com/problems/count-items-matching-a-rule/)

比较基础的题目，首先根据要检索的种类确定在数组中寻找的下标，然后一趟扫描枚举就行了。

最后附上python代码：

```python
class Solution(object):
    def countMatches(self, items, ruleKey, ruleValue):
        """
        :type items: List[List[str]]
        :type ruleKey: str
        :type ruleValue: str
        :rtype: int
        """

        cnt = 0
        if ruleKey == 'type':
            check_index = 0
        elif ruleKey == 'color':
            check_index = 1
        else:
            check_index = 2

        res = 0
        for item in items:
            if item[check_index] == ruleValue:
                res += 1

        return res
```
