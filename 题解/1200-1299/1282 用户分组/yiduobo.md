---
title: "1282. 用户分组"
aliases: ["yiduobo的每日leetcode 1282.用户分组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/388480029"
zhihu_id: "388480029"
zhihu_title: "yiduobo的每日leetcode 1282.用户分组"
question_id: "1282"
question: "用户分组"
problem_url: "https://leetcode.cn/problems/group-the-people-given-the-group-size-they-belong-to/"
created: "2021-07-10T18:20:08+08:00"
updated: "2021-07-10T18:20:08+08:00"
upvotes: 1
comments: 0
---

# 1282. 用户分组

> **[yiduobo的每日leetcode 1282.用户分组](https://zhuanlan.zhihu.com/p/388480029) · 知乎 · 2021-07-10 · 赞同 1**
> 力扣：[1282. 用户分组](https://leetcode.cn/problems/group-the-people-given-the-group-size-they-belong-to/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1282.用户分组

[力扣](https://leetcode-cn.com/problems/group-the-people-given-the-group-size-they-belong-to/)

由于题目只要求组里的人数达标，因此可以使用一个dict，key为组中的人数，而value为一个list，表示当前组内的用户。

遍历每个用户，将当前用户加入到对应的组中。若某一时刻组中人数等于key，那么就将组内的用户加入到答案中，并将该组清空。

最后附上python代码：

```python
class Solution(object):
    def groupThePeople(self, groupSizes):
        """
        :type groupSizes: List[int]
        :rtype: List[List[int]]
        """

        group_dict = {}
        res = []
        for index, size in enumerate(groupSizes):
            if size not in group_dict:
                group_dict[size] = []
            group_dict[size].append(index)
            if len(group_dict[size]) == size:
                res.append(group_dict[size][:])
                group_dict[size] = []
        
        return res
```
