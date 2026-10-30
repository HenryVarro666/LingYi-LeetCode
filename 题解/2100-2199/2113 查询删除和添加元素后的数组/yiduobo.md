---
title: "2113. 查询删除和添加元素后的数组"
aliases: ["yiduobo的每日leetcode 2113.查询删除和添加元素后的数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/626354836"
zhihu_id: "626354836"
zhihu_title: "yiduobo的每日leetcode 2113.查询删除和添加元素后的数组"
question_id: "2113"
question: "查询删除和添加元素后的数组"
problem_url: "https://leetcode.cn/problems/elements-in-array-after-removing-and-replacing-elements/"
created: "2023-05-02T22:59:14+08:00"
updated: "2023-05-02T22:59:14+08:00"
upvotes: 0
comments: 0
---

# 2113. 查询删除和添加元素后的数组

> **[yiduobo的每日leetcode 2113.查询删除和添加元素后的数组](https://zhuanlan.zhihu.com/p/626354836) · 知乎 · 2023-05-02 · 赞同 0**
> 力扣：[2113. 查询删除和添加元素后的数组](https://leetcode.cn/problems/elements-in-array-after-removing-and-replacing-elements/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2113.查询删除和添加元素后的数组

[力扣](https://leetcode.cn/problems/elements-in-array-after-removing-and-replacing-elements/)

找规律的题目，首先数组是按照2n次每轮的长度进行变换，那么对于某个询问[time, index]，可以先将time对2n取模t \= time % 2n，表示当前数组变换到了哪一步。

接下来，数组在前n步是逐渐消减，其长度是从n逐渐减小到1，内容是数组的后缀。而在后n步则是逐渐增长，其长度是从0逐渐增加到n - 1，内容是数组的前缀。根据这个结论，就可以先对比index与数组长度的大小，若数组长度不够，那么对应的答案就是-1，否则若当前的数组处于前n步时，答案就是nums[index + t]，否则答案就是nums[index]。

最后附上python代码：

```python
class Solution(object):
    def elementInNums(self, nums, queries):
        """
        :type nums: List[int]
        :type queries: List[List[int]]
        :rtype: List[int]
        """

        n = len(nums)
        res = []
        for t, index in queries:
            t %= (n + n)
            if t < n:
                if index < n - t:
                    res.append(nums[index + t])
                else:
                    res.append(-1)
            else:
                if index < t - n:
                    res.append(nums[index])
                else:
                    res.append(-1)
        
        return res
```
