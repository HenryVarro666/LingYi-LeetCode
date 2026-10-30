---
title: "944. 删列造序"
aliases: ["yiduobo的每日leetcode 944.删列造序"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bian-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/358790846"
zhihu_id: "358790846"
zhihu_title: "yiduobo的每日leetcode 944.删列造序"
question_id: "944"
question: "删列造序"
problem_url: "https://leetcode.cn/problems/delete-columns-to-make-sorted/"
difficulty: "Easy"
created: "2021-03-21T19:11:05+08:00"
updated: "2021-03-21T19:11:05+08:00"
upvotes: 1
comments: 0
---

# 944. 删列造序

> **[yiduobo的每日leetcode 944.删列造序](https://zhuanlan.zhihu.com/p/358790846) · 知乎 · 2021-03-21 · 赞同 1**
> 力扣：[944. 删列造序](https://leetcode.cn/problems/delete-columns-to-make-sorted/) · Easy · 灵茶山艾府：[简单题，简单做（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

944.删列造序

[力扣](https://leetcode-cn.com/problems/delete-columns-to-make-sorted/)

比较基础的题目， 直接枚举每一列，然后检测该列是否按升序排列即可。

最后附上python代码：

```python
class Solution(object):
    def minDeletionSize(self, strs):
        """
        :type strs: List[str]
        :rtype: int
        """

        n = len(strs)
        l = len(strs[0])
        
        res = 0
        for i in range(l):
            for j in range(n - 1):
                if strs[j][i] > strs[j + 1][i]:
                    res += 1
                    break
        
        return res
```
