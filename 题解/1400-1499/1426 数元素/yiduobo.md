---
title: "1426. 数元素"
aliases: ["yiduobo的每日leetcode 1426.数元素"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/615929686"
zhihu_id: "615929686"
zhihu_title: "yiduobo的每日leetcode 1426.数元素"
question_id: "1426"
question: "数元素"
problem_url: "https://leetcode.cn/problems/counting-elements/"
created: "2023-03-22T00:02:39+08:00"
updated: "2023-03-22T00:02:39+08:00"
upvotes: 0
comments: 0
---

# 1426. 数元素

> **[yiduobo的每日leetcode 1426.数元素](https://zhuanlan.zhihu.com/p/615929686) · 知乎 · 2023-03-22 · 赞同 0**
> 力扣：[1426. 数元素](https://leetcode.cn/problems/counting-elements/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

1426.数元素

[力扣](https://leetcode.cn/problems/counting-elements/)

使用集合统计所有出现的数，接下来一趟遍历，对于当前遍历到的数num，检测num + 1是否存在与集合中并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def countElements(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        num_set = set(arr)
        res = 0
        for num in arr:
            if num + 1 in num_set:
                res += 1
        
        return res
```
