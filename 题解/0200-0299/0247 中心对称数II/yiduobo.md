---
title: "247. 中心对称数II"
aliases: ["yiduobo的每日leetcode 247.中心对称数II"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/592176107"
zhihu_id: "592176107"
zhihu_title: "yiduobo的每日leetcode 247.中心对称数II"
question_id: "247"
question: "中心对称数II"
problem_url: "https://leetcode.cn/problems/strobogrammatic-number-ii/"
created: "2022-12-16T04:55:28+08:00"
updated: "2022-12-16T04:55:28+08:00"
upvotes: 0
comments: 0
---

# 247. 中心对称数II

> **[yiduobo的每日leetcode 247.中心对称数II](https://zhuanlan.zhihu.com/p/592176107) · 知乎 · 2022-12-16 · 赞同 0**
> 力扣：[247. 中心对称数II](https://leetcode.cn/problems/strobogrammatic-number-ii/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

247.中心对称数II

[力扣](https://leetcode.cn/problems/strobogrammatic-number-ii/)

受到回文数的启发，对于本题的中心对称数，也可以采用类似回文数的方式来生成。

首先，不存在长度为0的中心对称数，而长度为1的中心对称数有三个，分别为0、1、8。

接下来，对于长度大于等于2的中心对称数，不妨设其长度为len，那么其去头去尾的部分就必然是一个长度为len - 2的中心对称数，于是可以使用一个数组f记录每种长度的所有中心对称数，接下来对于f[index]，则可以遍历f[index - 2]中的所有数，然后尝试在头尾分别添加[0, 0]、[1, 1]、[6, 9]、[8, 8]、[9, 6]这几个数对来构造出新的中心对称数从而得到f[index]。

需要特别注意的是，这样的构造方式没有去除掉前导0的情况，因此在计算最终答案时，需要将除了0自身以外的其他所有具有前导0的中心对称数去掉。

最后附上python代码：

```python
class Solution(object):
    def findStrobogrammatic(self, n):
        """
        :type n: int
        :rtype: List[str]
        """

        f = []
        f.append([''])
        f.append(['0', '1', '8'])

        for index in range(2, n + 1):
            f.append([])
            for s in f[index - 2]:
                f[-1].append('0' + s + '0')
                f[-1].append('1' + s + '1')
                f[-1].append('6' + s + '9')
                f[-1].append('8' + s + '8')
                f[-1].append('9' + s + '6')
        
        res = []
        for s in f[n]:
            if n == 1 or s[0] != '0':
                res.append(s)

        return res
```
