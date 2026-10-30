---
title: "1640. 能否连接形成数组"
aliases: ["yiduobo的每日leetcode 1640.能否连接形成数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/438661145"
zhihu_id: "438661145"
zhihu_title: "yiduobo的每日leetcode 1640.能否连接形成数组"
question_id: "1640"
question: "能否连接形成数组"
problem_url: "https://leetcode.cn/problems/check-array-formation-through-concatenation/"
created: "2021-11-28T12:45:15+08:00"
updated: "2021-11-28T12:45:15+08:00"
upvotes: 0
comments: 0
---

# 1640. 能否连接形成数组

> **[yiduobo的每日leetcode 1640.能否连接形成数组](https://zhuanlan.zhihu.com/p/438661145) · 知乎 · 2021-11-28 · 赞同 0**
> 力扣：[1640. 能否连接形成数组](https://leetcode.cn/problems/check-array-formation-through-concatenation/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1640.能否连接形成数组

[力扣](https://leetcode-cn.com/problems/check-array-formation-through-concatenation/)

由于题目中保证每个数字都不一样，那么只要知道了某个piece的首个数字，就可以通过哈希表对应地找个这个piece。

那么可以从头开始扫描arr，对于当前位置p，首先是p \= 0的情况。此时的arr[p]必然是某个piece的首个数字，那么可以通过arr[p]找到对应的piece，然后逐个对比这个piece与p之后的若干数字，若不能对上，那么返回false。若都可以对上，那么就将p向后推，直到处理完这个piece。

接下来对于当前的p而言，arr[p]必然又是另一个piece的首个数字。重复这个过程直到出现不匹配或者p移动到arr末尾为止。

最后附上python代码：

```python
class Solution(object):
    def canFormArray(self, arr, pieces):
        """
        :type arr: List[int]
        :type pieces: List[List[int]]
        :rtype: bool
        """

        p = 0
        piece_dict = {}
        for piece in pieces:
            piece_dict[piece[0]] = piece
        while p < len(arr):
            now = arr[p]
            if now not in piece_dict:
                return False
            
            piece = piece_dict[now]
            for num in piece:
                if num != arr[p]:
                    return False
                p += 1
            
        return True
```
