---
title: "1817. 查找用户活跃分钟数"
aliases: ["yiduobo的每日leetcode 1817.查找用户活跃分钟数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/465966575"
zhihu_id: "465966575"
zhihu_title: "yiduobo的每日leetcode 1817.查找用户活跃分钟数"
question_id: "1817"
question: "查找用户活跃分钟数"
problem_url: "https://leetcode.cn/problems/finding-the-users-active-minutes/"
created: "2022-02-10T23:03:12+08:00"
updated: "2022-02-10T23:03:12+08:00"
upvotes: 0
comments: 0
---

# 1817. 查找用户活跃分钟数

> **[yiduobo的每日leetcode 1817.查找用户活跃分钟数](https://zhuanlan.zhihu.com/p/465966575) · 知乎 · 2022-02-10 · 赞同 0**
> 力扣：[1817. 查找用户活跃分钟数](https://leetcode.cn/problems/finding-the-users-active-minutes/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1817.查找用户活跃分钟数

[力扣](https://leetcode-cn.com/problems/finding-the-users-active-minutes/)

题目描述比较复杂，但是实际上是很容易的题目。使用set来给每个用户活跃分钟数去重，然后使用哈希表统计每个用户活跃的分钟数目，并用这个数目更新答案。

具体来说，就是枚举logs，对于当前这一条log记录的用户u在第m分钟活跃这个信息，首先判断m是否已经被u对应的set记录过了。若没有，则将其加入到set中，并将u活跃分钟数加上1，然后用这个新的活跃分钟数更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def findingUsersActiveMinutes(self, logs, k):
        """
        :type logs: List[List[int]]
        :type k: int
        :rtype: List[int]
        """

        res = [0] * k
        used_minute = {}
        cnt_dict = {}
        for id, minute in logs:
            if id not in used_minute:
                used_minute[id] = set()
            if minute not in used_minute[id]:
                used_minute[id].add(minute)
                cnt_dict[id] = cnt_dict.get(id, 0) + 1
                if cnt_dict[id] == 1:
                    res[0] += 1
                else:
                    res[cnt_dict[id] - 2] -= 1
                    if cnt_dict[id] <= k:
                        res[cnt_dict[id] - 1] += 1
        
        return res
```
