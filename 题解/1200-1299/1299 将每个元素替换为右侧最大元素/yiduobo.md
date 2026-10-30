---
title: "1299. 将每个元素替换为右侧最大元素"
aliases: ["yiduobo的每日leetcode 1299.将每个元素替换为右侧最大元素"]
tags: ["leetcode", "yiduobo", "leetcode/easy"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/390695269"
zhihu_id: "390695269"
zhihu_title: "yiduobo的每日leetcode 1299.将每个元素替换为右侧最大元素"
question_id: "1299"
question: "将每个元素替换为右侧最大元素"
problem_url: "https://leetcode.cn/problems/replace-elements-with-greatest-element-on-right-side/"
difficulty: "Easy"
created: "2021-07-17T23:40:50+08:00"
updated: "2021-07-17T23:40:50+08:00"
upvotes: 1
comments: 0
---

# 1299. 将每个元素替换为右侧最大元素

> **[yiduobo的每日leetcode 1299.将每个元素替换为右侧最大元素](https://zhuanlan.zhihu.com/p/390695269) · 知乎 · 2021-07-17 · 赞同 1**
> 力扣：[1299. 将每个元素替换为右侧最大元素](https://leetcode.cn/problems/replace-elements-with-greatest-element-on-right-side/) · Easy · 灵茶山艾府：[倒序遍历，维护后缀最大值（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1299.将每个元素替换为右侧最大元素

[力扣](https://leetcode-cn.com/problems/replace-elements-with-greatest-element-on-right-side/)

对于第i个位置，其答案应该是

res[i] \= max(arr[i]，arr[i + 1]，...，arr[-1]）

而对于第i + 1个位置，其答案则为

res[i + 1] \= max(arr[i + 1]，arr[i + 2]，...，arr[-1])

对比这两个式子，可知

res[i] \= max(res[i + 1], arr[i])

于是可以从后向前一趟扫描，根据上面的式子逐个计算当前位置的res即可。

最后附上python代码：

```python
class Solution(object):
    def replaceElements(self, arr):
        """
        :type arr: List[int]
        :rtype: List[int]
        """

        res = []
        max_num = -1
        for num in arr[::-1]:
            res.append(max_num)
            max_num = max(max_num, num)
        
        return res[::-1]
```
