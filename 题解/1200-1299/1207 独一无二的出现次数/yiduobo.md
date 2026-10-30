---
title: "1207. 独一无二的出现次数"
aliases: ["yiduobo的每日leetcode 1207.独一无二的出现次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/382207007"
zhihu_id: "382207007"
zhihu_title: "yiduobo的每日leetcode 1207.独一无二的出现次数"
question_id: "1207"
question: "独一无二的出现次数"
problem_url: "https://leetcode.cn/problems/unique-number-of-occurrences/"
created: "2021-06-19T20:09:07+08:00"
updated: "2021-06-19T20:09:07+08:00"
upvotes: 0
comments: 0
---

# 1207. 独一无二的出现次数

> **[yiduobo的每日leetcode 1207.独一无二的出现次数](https://zhuanlan.zhihu.com/p/382207007) · 知乎 · 2021-06-19 · 赞同 0**
> 力扣：[1207. 独一无二的出现次数](https://leetcode.cn/problems/unique-number-of-occurrences/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1207.独一无二的出现次数

[力扣](https://leetcode-cn.com/problems/unique-number-of-occurrences/)

统计每个数出现的次数，然后再使用哈希表来判断这些次数当中是否存在重复即可。

最后附上python代码：

```python
class Solution(object):
    def uniqueOccurrences(self, arr):
        """
        :type arr: List[int]
        :rtype: bool
        """

        cnt_dict = {}
        for num in arr:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        cnt_set = set()
        for cnt in cnt_dict.values():
            if cnt in cnt_set:
                return False
            cnt_set.add(cnt)
        
        return True
```
