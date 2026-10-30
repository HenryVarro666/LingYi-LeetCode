---
title: "2120. 执行所有后缀指令"
aliases: ["yiduobo的每日leetcode 2120.执行所有后缀指令"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/string", "leetcode/simulation", "leetcode/bao-li"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/524643680"
zhihu_id: "524643680"
zhihu_title: "yiduobo的每日leetcode 2120.执行所有后缀指令"
question_id: "2120"
question: "执行所有后缀指令"
problem_url: "https://leetcode.cn/problems/execution-of-all-suffix-instructions-staying-in-a-grid/"
difficulty: "Medium"
created: "2022-06-06T00:14:19+08:00"
updated: "2022-06-06T00:14:19+08:00"
upvotes: 0
comments: 0
---

# 2120. 执行所有后缀指令

> **[yiduobo的每日leetcode 2120.执行所有后缀指令](https://zhuanlan.zhihu.com/p/524643680) · 知乎 · 2022-06-06 · 赞同 0**
> 力扣：[2120. 执行所有后缀指令](https://leetcode.cn/problems/execution-of-all-suffix-instructions-staying-in-a-grid/) · Medium · 灵茶山艾府：[暴力+模拟](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2120.执行所有后缀指令

[力扣](https://leetcode.cn/problems/execution-of-all-suffix-instructions-staying-in-a-grid/)

由于题目中m的规模很小，因此直接枚举每一种后缀指令然后模拟执行就行了。模拟的过程中需要注意不要走出边界。除此之外，感觉应该也有O(m)的做法，即利用当前后缀指令中的某些性质推导前一个后缀指令的执行情况，简单来说就是当前后缀指令中某个出界的指令可能被前一个后缀指令的首个命令拉回来，同时当前踩着边界的指令也可能被首个命令给挤出边界，但是情况似乎比较多，在这里就没有继续往下想了。

最后附上python代码：

```python
class Solution(object):
    def executeInstructions(self, n, startPos, s):
        """
        :type n: int
        :type startPos: List[int]
        :type s: str
        :rtype: List[int]
        """

        m = len(s)
        res = []
        for start_index in range(m):
            nowy, nowx = startPos
            cnt = 0
            for index in range(start_index, m):
                if s[index] == 'L':
                    nowx -= 1
                elif s[index] == 'R':
                    nowx += 1
                elif s[index] == 'U':
                    nowy -= 1
                else:
                    nowy += 1
                
                if nowx < 0 or nowx > n - 1 or nowy < 0 or nowy > n - 1:
                    break

                cnt += 1
            
            res.append(cnt)
        
        return res
```
