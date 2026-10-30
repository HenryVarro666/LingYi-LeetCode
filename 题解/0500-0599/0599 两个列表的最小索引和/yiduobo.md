---
title: "599. 两个列表的最小索引和"
aliases: ["yiduobo的每日leetcode 599.两个列表的最小索引和"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/268422956"
zhihu_id: "268422956"
zhihu_title: "yiduobo的每日leetcode 599.两个列表的最小索引和"
question_id: "599"
question: "两个列表的最小索引和"
problem_url: "https://leetcode.cn/problems/minimum-index-sum-of-two-lists/"
created: "2020-10-24T21:26:09+08:00"
updated: "2020-10-24T21:26:09+08:00"
upvotes: 0
comments: 0
---

# 599. 两个列表的最小索引和

> **[yiduobo的每日leetcode 599.两个列表的最小索引和](https://zhuanlan.zhihu.com/p/268422956) · 知乎 · 2020-10-24 · 赞同 0**
> 力扣：[599. 两个列表的最小索引和](https://leetcode.cn/problems/minimum-index-sum-of-two-lists/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

599.两个列表的最小索引和<https://leetcode-cn.com/problems/minimum-index-sum-of-two-lists/>

比较基础的题目。使用哈希表储存其中一个索引中餐厅的位置，然后遍历另一个索引，求每个餐厅在两个索引中的和，找出最大的即可。

最后附上python代码：

```python
class Solution(object):
    def findRestaurant(self, list1, list2):
        """
        :type list1: List[str]
        :type list2: List[str]
        :rtype: List[str]
        """

        s_dict = {}
        for index, s in enumerate(list1):
            s_dict[s] = index
        
        res = []
        index_sum = None
        
        for index, s in enumerate(list2):
            if s in s_dict:
                if index_sum is None or index_sum > s_dict[s] + index:
                    index_sum = s_dict[s] + index
                    res = [s]
                elif index_sum == s_dict[s] + index:
                    res.append(s)
        
        return res
```
