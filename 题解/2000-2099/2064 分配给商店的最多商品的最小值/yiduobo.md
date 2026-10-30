---
title: "2064. 分配给商店的最多商品的最小值"
aliases: ["yiduobo的每日leetcode 2064.分配给商店的最多商品的最小值"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/514680766"
zhihu_id: "514680766"
zhihu_title: "yiduobo的每日leetcode 2064.分配给商店的最多商品的最小值"
question_id: "2064"
question: "分配给商店的最多商品的最小值"
problem_url: "https://leetcode.cn/problems/minimized-maximum-of-products-distributed-to-any-store/"
difficulty: "Medium"
rating: 1886
created: "2022-05-15T14:11:05+08:00"
updated: "2022-05-15T14:11:05+08:00"
upvotes: 0
comments: 0
---

# 2064. 分配给商店的最多商品的最小值

> **[yiduobo的每日leetcode 2064.分配给商店的最多商品的最小值](https://zhuanlan.zhihu.com/p/514680766) · 知乎 · 2022-05-15 · 赞同 0**
> 力扣：[2064. 分配给商店的最多商品的最小值](https://leetcode.cn/problems/minimized-maximum-of-products-distributed-to-any-store/) · Medium · 灵茶山艾府：[二分答案（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2064.分配给商店的最多商品的最小值

[力扣](https://leetcode.cn/problems/minimized-maximum-of-products-distributed-to-any-store/)

一个很直观的想法是，随着x的增大，完成分配的可能性就越高，也就是说本题的答案是符合二分的性质的。于是可以二分这个x，然后对于每种商品，都顶着这个x进行分配，计算最终需要的商店数目cnt。若cnt大于n，说明x太小了，需要更新二分的左边界l为x + 1，否则说明x是一个可行解，此时则应该更新二分的右边界r为x。

最后附上python代码：

```python
class Solution(object):
    def minimizedMaximum(self, n, quantities):
        """
        :type n: int
        :type quantities: List[int]
        :rtype: int
        """

        l = 1
        r = max(quantities)
        while l < r:
            mid = (l + r) >> 1
            cnt = 0
            for q in quantities:
                cnt += q / mid
                if q % mid != 0:
                    cnt += 1

            if cnt > n:
                l = mid + 1
            else:
                r = mid
        
        return l
```
