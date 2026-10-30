---
title: "2433. 找出前缀异或的原始数组"
aliases: ["yiduobo的每日leetcode 2433.找出前缀异或的原始数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/prefix-sum", "leetcode/chai-fen", "题单/位运算", "题单/位运算/二-异或-XOR-的性质"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/583127358"
zhihu_id: "583127358"
zhihu_title: "yiduobo的每日leetcode 2433.找出前缀异或的原始数组"
question_id: "2433"
question: "找出前缀异或的原始数组"
problem_url: "https://leetcode.cn/problems/find-the-original-array-of-prefix-xor/"
difficulty: "Medium"
rating: 1367
created: "2022-11-14T00:49:41+08:00"
updated: "2022-11-14T00:49:41+08:00"
upvotes: 0
comments: 0
---

# 2433. 找出前缀异或的原始数组

> **[yiduobo的每日leetcode 2433.找出前缀异或的原始数组](https://zhuanlan.zhihu.com/p/583127358) · 知乎 · 2022-11-14 · 赞同 0**
> 力扣：[2433. 找出前缀异或的原始数组](https://leetcode.cn/problems/find-the-original-array-of-prefix-xor/) · Medium · 灵茶山艾府：[利用差分的思想（Python 一行）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2433.找出前缀异或的原始数组

[力扣](https://leetcode.cn/problems/find-the-original-array-of-prefix-xor/)

首先，显然有arr[0] \= pref[0]，接下来对于所有的index > 1，都有

pref[index] \= arr[0] ^ arr[1] ^ ... ^ arr[index]

另一方面

pref[index - 1] \= arr[0] ^ arr[1] ^ ... ^ arr[index - 1]

那么

pref[index] \= pref[index - 1] ^ arr[index]

于是就有

arr[index] \= pref[index] ^ pref[index - 1]

根据这个结论，只需一趟遍历就可以将arr还原出来了。

最后附上python代码：

```python
class Solution(object):
    def findArray(self, pref):
        """
        :type pref: List[int]
        :rtype: List[int]
        """

        res = [pref[0]]
        for index in range(1, len(pref)):
            res.append(pref[index] ^ pref[index - 1])
        
        return res
```
