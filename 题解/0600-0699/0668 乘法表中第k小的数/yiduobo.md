---
title: "668. 乘法表中第k小的数"
aliases: ["yiduobo的每日leetcode 668.乘法表中第k小的数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/292258596"
zhihu_id: "292258596"
zhihu_title: "yiduobo的每日leetcode 668.乘法表中第k小的数"
question_id: "668"
question: "乘法表中第k小的数"
problem_url: "https://leetcode.cn/problems/kth-smallest-number-in-multiplication-table/"
difficulty: "Hard"
created: "2020-11-13T22:41:11+08:00"
updated: "2020-11-13T22:41:11+08:00"
upvotes: 0
comments: 0
---

# 668. 乘法表中第k小的数

> **[yiduobo的每日leetcode 668.乘法表中第k小的数](https://zhuanlan.zhihu.com/p/292258596) · 知乎 · 2020-11-13 · 赞同 0**
> 力扣：[668. 乘法表中第k小的数](https://leetcode.cn/problems/kth-smallest-number-in-multiplication-table/) · Hard · 灵茶山艾府：[第 k 小/大问题的通用转化方法 + 优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

668.乘法表中第k小的数

[力扣](https://leetcode-cn.com/problems/kth-smallest-number-in-multiplication-table/)

对于某个数x而言，其在第k行中的位置就是x / k，同理，在第k列中的位置也是x / k，因此我们可以枚举行和列中较短的那一维，计算x在当前行或列中排第几，然后将这个排名累加，就是x在当前表中的排名。

有了这个排名之后，我们就可以进行二分来确定最终的答案是多少。

最后附上python代码：

```python
class Solution(object):
    def findKthNumber(self, m, n, k):
        """
        :type m: int
        :type n: int
        :type k: int
        :rtype: int
        """

        l = 1
        r = m * n

        while l < r:
            mid = (l + r) >> 1
            cnt = 0
            for index in range(1, min(m, n) + 1):
                cnt += min(mid / index, max(m, n))
            if cnt >= k:
                r = mid
            else:
                l = mid + 1
        
        return l
```
