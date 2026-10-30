---
title: "896. 单调数列"
aliases: ["yiduobo的每日leetcode 896.单调数列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/352979651"
zhihu_id: "352979651"
zhihu_title: "yiduobo的每日leetcode 896.单调数列"
question_id: "896"
question: "单调数列"
problem_url: "https://leetcode.cn/problems/monotonic-array/"
created: "2021-02-25T22:19:12+08:00"
updated: "2021-02-25T22:19:12+08:00"
upvotes: 0
comments: 0
---

# 896. 单调数列

> **[yiduobo的每日leetcode 896.单调数列](https://zhuanlan.zhihu.com/p/352979651) · 知乎 · 2021-02-25 · 赞同 0**
> 力扣：[896. 单调数列](https://leetcode.cn/problems/monotonic-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

896.单调数列

[力扣](https://leetcode-cn.com/problems/monotonic-array/)

比较基础的题目。可以使用一个标记flag表示当前序列是递增还是递减的，初始化为空，然后从头开始往后遍历整个数组。对于当前的A[index]：

1、若A[index] \= A[index - 1]，那么无论是递增还是递减这都是合法情况

2、若flag为空，那么就根据A[index]与A[index - 1]的大小关系设定flag的值，否则需要判断A[index]与A[index - 1]的大小关系是否与flag一致，当出现矛盾时返回false

若能成功遍历完整个数组，那么返回ture

最后附上python代码：

```python
class Solution(object):
    def isMonotonic(self, A):
        """
        :type A: List[int]
        :rtype: bool
        """

        if len(A) <= 2:
            return True
        
        flag = None
        last_num = A[0]
        for num in A[1:]:
            if num == last_num:
                continue
            if flag is None:
                flag = num > last_num
            elif (num > last_num) != flag:
                return False
            last_num = num

        return True
```
