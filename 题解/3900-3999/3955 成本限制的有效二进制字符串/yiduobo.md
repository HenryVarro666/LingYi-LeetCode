---
title: "3955. 成本限制的有效二进制字符串"
aliases: ["yiduobo的每日leetcode 3955.成本限制的有效二进制字符串"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "题单/链表-二叉树与回溯", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2048169723087558534"
zhihu_id: "2048169723087558534"
zhihu_title: "yiduobo的每日leetcode 3955.成本限制的有效二进制字符串"
question_id: "3955"
question: "成本限制的有效二进制字符串"
problem_url: "https://leetcode.cn/problems/valid-binary-strings-with-cost-limit/"
difficulty: "Medium"
rating: 1429
created: "2026-06-10T22:32:47+08:00"
updated: "2026-06-10T22:32:47+08:00"
upvotes: 1
comments: 0
---

# 3955. 成本限制的有效二进制字符串

> **[yiduobo的每日leetcode 3955.成本限制的有效二进制字符串](https://zhuanlan.zhihu.com/p/2048169723087558534) · 知乎 · 2026-06-10 · 赞同 1**
> 力扣：[3955. 成本限制的有效二进制字符串](https://leetcode.cn/problems/valid-binary-strings-with-cost-limit/) · Medium · 灵茶山艾府：[预处理每个数的成本（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3955.成本限制的有效二进制字符串

<https://leetcode.cn/problems/valid-binary-strings-with-cost-limit/description/>

题目给出两个整数n和k，n的大小不超过12，k在0到n \* (n - 1) // 2之间。

二进制字符串s的成本定义为所有满足s[index] \=\= '1'的下标index(从0开始)的总和。

如果一个二进制字符串满足一下条件，则认为它是有效的：

- 不包含两个连续的'1'字符
- 它的成本小于等于k

返回所有长度为n的有效二进制字符串列表，顺序不限。

题目中n的规模较小，在这里可以直接暴力枚举所有长度为n的进制字符串，然后遍历这个字符串，检测是否存在相邻的1，同时计算其成本。若其有效，则将其加入到答案数组中。

最后附上python代码：

```python
class Solution(object):
    def generateValidStrings(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: List[str]
        """
        
        res = []
        for state in range(1 << n):
            cost = 0
            s = []
            for index in range(n):
                if (state & (1 << index)) == (1 << index):
                    cost += index
                    if s and s[-1] == '1':
                        cost = k + 1
                        break
                    
                    s.append('1')
                else:
                    s.append('0')
            
            if cost <= k:
                res.append(''.join(s))
        
        return res
```
