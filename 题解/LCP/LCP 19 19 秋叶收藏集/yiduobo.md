---
title: "LCP 19. 秋叶收藏集"
aliases: ["yiduobo的每日leetcode LCP19.秋叶收藏集"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/572335485"
zhihu_id: "572335485"
zhihu_title: "yiduobo的每日leetcode LCP19.秋叶收藏集"
question_id: "LCP 19"
question: "秋叶收藏集"
created: "2022-10-11T00:48:19+08:00"
updated: "2022-10-11T00:48:19+08:00"
upvotes: 0
comments: 0
---

# LCP 19. 秋叶收藏集

> **[yiduobo的每日leetcode LCP19.秋叶收藏集](https://zhuanlan.zhihu.com/p/572335485) · 知乎 · 2022-10-11 · 赞同 0**
> 力扣：LCP 19. 秋叶收藏集

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

LCP19.秋叶收藏集

[力扣](https://leetcode.cn/problems/UlBDOe/)

题目给出一个由r和y组成的字符串，并且可以任意修改其中的字符，问最少需要多少次修改可以使得字符串变为r...ry...yr...r的形式，这里的三个部分长度均大于等于1。

最直观的做法自然是枚举两个分界点p1和p2，即在最终的字符串中，0到p1 - 1这一段都是r，p1到p2这一段都是y，p2 + 1到n - 1这一段都是r。

由于字符串的长度比较长，因此枚举两个分界点的时间复杂度太高了，只能想办法枚举其中一个，然后在这个前提下找到另一个的最优位置。

对于一组分界点p1、p2，可以先计算出这种分割情况下需要进行调整操作的次数。设数组r为字符串中关于字符'r'的前缀和数组，即r[i]表示字符串中第0到第i个字符串中'r'的数目，那么：

1、在0到p1 - 1这一段当中，一共有r[p1 - 1]个'r'，那么需要替换的数目就是区间长度p1减去'r'的数目，即p1 - r[p1 - 1]

2、在p1到p2这一段中，一共有r[p2] - r[p1 - 1]个'r'，这些'r'都需要被替换掉，因此需要r[p2] - r[p1 - 1]次操作

3、在最后的p2 + 1到n - 1这一段中，一共有r[n - 1] - r[p2]个'r'，那么需要替换的数目就是区间长度(n - 1) - (p2 + 1) + 1 \= n - p2 - 1，再减去'r'的数目，即n - p2 - 1 - (r[n - 1] - r[p2])

综合上面三个式子，就可以得到最终需要的操作次数

tot \= p1 - r[p1 - 1] + r[p2] - r[p1 - 1] + n - p2 - 1 - r[n - 1] + r[p2]

将上面式子按常数、p1和p2归类后，就有

tot \= n - 1 - r[n - 1] + p1 - 2 \* r[p1 - 1] - (p2 - 2 \* r[p2])

对于这个式子，可以枚举p2的位置，然后找到1到p2之间，满足p1 - 2 \* r[p1 - 1]最小的p1。对于这个p1，可以在枚举的过程中使用一个变量min_left记录最优的p1 - 2 \* r[p1 - 1]，然后在使用min_left以及当前的p2计算当前操作数更新答案之后，再使用当前的p2来更新min_left。这样一来就成功将时间复杂度降到了O(n)。

最后附上python代码：

```python
class Solution(object):
    def minimumOperations(self, leaves):
        """
        :type leaves: str
        :rtype: int
        """

        r = []
        for index, char in enumerate(leaves):
            if index > 0:
                r.append(r[-1])
            else:
                r.append(0)
            if char == 'r':
                r[-1] += 1

        n = len(leaves)
        res = n
        min_left = 1 - r[0] - r[0]
        for index in range(1, n - 1):
            res = min(res, min_left - index + r[index] + r[index])
            min_left = min(min_left, index - r[index - 1] - r[index - 1])

        
        return res + n - 1 - r[-1]
```
