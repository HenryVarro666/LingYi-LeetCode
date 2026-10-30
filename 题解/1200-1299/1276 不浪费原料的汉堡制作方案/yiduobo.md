---
title: "1276. 不浪费原料的汉堡制作方案"
aliases: ["yiduobo的每日leetcode 1276.不浪费原料的汉堡制作方案"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/387969891"
zhihu_id: "387969891"
zhihu_title: "yiduobo的每日leetcode 1276.不浪费原料的汉堡制作方案"
question_id: "1276"
question: "不浪费原料的汉堡制作方案"
problem_url: "https://leetcode.cn/problems/number-of-burgers-with-no-waste-of-ingredients/"
created: "2021-07-09T00:00:25+08:00"
updated: "2021-07-09T00:00:25+08:00"
upvotes: 0
comments: 0
---

# 1276. 不浪费原料的汉堡制作方案

> **[yiduobo的每日leetcode 1276.不浪费原料的汉堡制作方案](https://zhuanlan.zhihu.com/p/387969891) · 知乎 · 2021-07-09 · 赞同 0**
> 力扣：[1276. 不浪费原料的汉堡制作方案](https://leetcode.cn/problems/number-of-burgers-with-no-waste-of-ingredients/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1276.不浪费原料的汉堡制作方案

[力扣](https://leetcode-cn.com/problems/number-of-burgers-with-no-waste-of-ingredients/)

居然还会有鸡兔同笼问题。。由与每个汉堡都要用掉一片奶酪，因此如果题目有解，那么奶酪的数目cheeseSlices就等于最终汉堡的数目。假设我们都做小皇堡，那么将用掉的番茄片数量就是cheeseSlices \* 2。

一个巨无霸和一个小皇堡需要的番茄片之差为2，那么计算出cheeseSlices \* 2与实际拥有番茄片tomatoSlices的差值diff，若这个diff非负，且为2的倍数，那么我们就应该做diff / 2个巨无霸。当然，由于巨无霸的总数必须小于等于汉堡的总数，因此这里还需要满足diff / 2必须小于等于cheeseSlices。若满足以上条件，那么巨无霸的数量就是diff / 2，而小皇堡的数量则为cheeseSlices - diff / 2，否则无解。

最后附上python代码：

```python
class Solution(object):
    def numOfBurgers(self, tomatoSlices, cheeseSlices):
        """
        :type tomatoSlices: int
        :type cheeseSlices: int
        :rtype: List[int]
        """

        diff = tomatoSlices - 2 * cheeseSlices
        if diff < 0 or diff % 2 == 1 or cheeseSlices < diff / 2:
            return []
        
        return [diff / 2, cheeseSlices - diff / 2]
```
