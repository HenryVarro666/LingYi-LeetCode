---
title: "1402. 做菜顺序"
aliases: ["yiduobo的每日leetcode 1402.做菜顺序"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/sorting", "leetcode/di-tui", "题单/贪心算法", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/405193492"
zhihu_id: "405193492"
zhihu_title: "yiduobo的每日leetcode 1402.做菜顺序"
question_id: "1402"
question: "做菜顺序"
problem_url: "https://leetcode.cn/problems/reducing-dishes/"
difficulty: "Hard"
rating: 1679
created: "2021-08-30T23:25:01+08:00"
updated: "2021-08-30T23:25:01+08:00"
upvotes: 3
comments: 0
---

# 1402. 做菜顺序

> **[yiduobo的每日leetcode 1402.做菜顺序](https://zhuanlan.zhihu.com/p/405193492) · 知乎 · 2021-08-30 · 赞同 3**
> 力扣：[1402. 做菜顺序](https://leetcode.cn/problems/reducing-dishes/) · Hard · 灵茶山艾府：[枚举做几道菜+贪心（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1402.做菜顺序

[力扣](https://leetcode-cn.com/problems/reducing-dishes/)

首先可以明确的是，若我们从中间选择k道菜，那么一定是选择满意度最高的k道菜。接下来还有一点就是，对于喜爱度越高的菜应该放到越后面来做，证明也很简单，不妨设现在的做菜顺序中有两道菜a[i]和a[j]，满足i \< j且a[i] > a[j]，那么这两道菜产生的收益就是

a[i] \* i + a[j] \* j \= (a[i] + a[j]) \* i + a[j] \* (j - i)

若我们将二者顺序调换，那么就有

a[i] \* j + a[j] \* i \= (a[i] + a[j]) \* i + a[i] \* (j - i)

可以发现，由于a[i] > a[j]，因此后面这种顺序的收益是更大的，也就是说当确定了要做的菜之后，应该按照喜爱度从小到大的顺序来做。

这样一来，当确定了最后要做的菜的数目之后，具体做菜的方案其实就已经定下来了。不妨将这些菜按照喜爱程度从大到小进行排序，那么：

1、只做一道菜时，收益就是a[0]

2、做两道菜时，收益为a[0] \* 2 + a[1]

3、做三道菜时，收益为a[0] \* 3 + a[1] \* 2 + a[2]

以此类推

那么做k道菜时，收益就是

v[k] \= a[0] \* k + a[1] \* (k - 1) + a[2] \* (k - 2) + ... + a[k - 1]

而做k + 1到菜的收益为

v[k + 1] \= a[0] \* (k + 1) + a[1] \* k + a[2] \* (k - 1) + ... + a[k]

二者相减，就有

v[k + 1] - v[k] \= a[0] + a[1] + ... + a[k]

也就转化成了一个前缀和的问题

于是我们可以将这些菜按喜爱程度从大到小进行排序，然后一趟扫描，一边计算前缀和，一边使用前缀和来更新答案。

最后附上python代码：

```python
class Solution(object):
    def maxSatisfaction(self, satisfaction):
        """
        :type satisfaction: List[int]
        :rtype: int
        """

        now = 0
        res = 0
        s = 0
        for index, num in enumerate(sorted(satisfaction, reverse = True)):
            s += num
            now += s
            res = max(res, now)
        
        return res
```
