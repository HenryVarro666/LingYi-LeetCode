---
title: "LCS 01. 下载插件"
aliases: ["yiduobo的每日leetcode LCS 01.下载插件"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/bit-manipulation", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/580783619"
zhihu_id: "580783619"
zhihu_title: "yiduobo的每日leetcode LCS 01.下载插件"
question_id: "LCS 01"
question: "下载插件"
problem_url: "https://leetcode.cn/problems/Ju9Xwi/"
difficulty: "Easy"
created: "2022-11-05T23:21:49+08:00"
updated: "2022-11-05T23:21:49+08:00"
upvotes: 0
comments: 0
---

# LCS 01. 下载插件

> **[yiduobo的每日leetcode LCS 01.下载插件](https://zhuanlan.zhihu.com/p/580783619) · 知乎 · 2022-11-05 · 赞同 0**
> 力扣：[LCS 01. 下载插件](https://leetcode.cn/problems/Ju9Xwi/) · Easy · 灵茶山艾府：[一行写法](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

LCS01.下载插件

[力扣](https://leetcode.cn/problems/Ju9Xwi/)

需要注意本题的带宽是可以大于插件数量的，例如要下载7个插件，那么用8的带宽一次性下载完也是可行的。

首先可以明确的是，如果操作序列中存在 扩容->下载->扩容 这种情况，那么完全可以先进行扩容再下载，这样可以下载更多的东西。那么在这里就只需要讨论最终的带宽2^k，以及使用这个带宽所需的总操作次数。

当n \= 2^k时，可以采用2^(k - 1)带宽下载两次，或者2^k带宽下载一次，但是如果采用更低的带宽进行下载就不行了。

当n \= 2^k + p时，如果采用2^k带宽，则需要k次扩容和两次下载，一共是k + 2次操作。而采用更小的带宽需要的操作次数显然是不会更少的。而另一方面，如果先将带宽扩成2^(k + 1)，那么只需一次下载操作，那么总共也是k + 2次操作。

综合上面两种情况，那么就可以先将带宽扩容到大于等于n的水平，然后执行一次下载操作就行了。

最后附上python代码：

```python
class Solution(object):
    def leastMinutes(self, n):
        """
        :type n: int
        :rtype: int
        """

        res = 1
        now = 1
        while now < n:
            now += now
            res += 1
        
        return res
```
