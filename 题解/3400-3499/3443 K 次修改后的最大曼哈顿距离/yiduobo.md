---
title: "3443. K次修改后的最大曼哈顿距离"
aliases: ["yiduobo的每日leetcode 3443.K次修改后的最大曼哈顿距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/math", "题单/数学算法", "题单/贪心算法", "题单/数学算法/七-杂项", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1891942514895873748"
zhihu_id: "1891942514895873748"
zhihu_title: "yiduobo的每日leetcode 3443.K次修改后的最大曼哈顿距离"
question_id: "3443"
question: "K 次修改后的最大曼哈顿距离"
problem_url: "https://leetcode.cn/problems/maximum-manhattan-distance-after-k-changes/"
difficulty: "Medium"
rating: 1856
created: "2025-04-05T20:12:15+08:00"
updated: "2025-04-05T20:12:15+08:00"
upvotes: 0
comments: 0
---

# 3443. K次修改后的最大曼哈顿距离

> **[yiduobo的每日leetcode 3443.K次修改后的最大曼哈顿距离](https://zhuanlan.zhihu.com/p/1891942514895873748) · 知乎 · 2025-04-05 · 赞同 0**
> 力扣：[3443. K 次修改后的最大曼哈顿距离](https://leetcode.cn/problems/maximum-manhattan-distance-after-k-changes/) · Medium · 灵茶山艾府：[两种方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3443.K次修改后的最大曼哈顿距离

[3443. K 次修改后的最大曼哈顿距离 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-manhattan-distance-after-k-changes/description/)

题目给出一个由'N'、'S'、'E'、'W'组成的字符串s，这些字符分别表示向北、南、东、西移动一个单位。一开始，所在的位置为原点(0, 0)，另外还可以修改s中的最多k个字符。

现在要求按顺序执行所有的移动操作，问在移动的过程中距离远点的最大曼哈顿距离为多少。

由于题目计算的是曼哈顿距离，那么就意味着水平方向和竖直方向上的移动是互不相关的，也就是说在这里只需尽量减少'N'和'S'同时出现的次数，以及尽量减少'W'和'E'同时出现的次数，就能使得与原点的距离尽量的远。

另一方面，题目需要计算的是整个移动过程中与远点距离的最大值，因此需要计算修改每种前缀可能得到的最远距离，于是可以对s进行一趟遍历，使用四个变量north、south、east、west分别统计当前前缀中'N'、'S'、'E'、'W'出现的次数，那么在不进行任何修改的情况下，与远点的距离为

abs(north - south) + abs(east - west)

接下来，由于修改的次数有限，因此在这里就应该将N和S中出现次数较少的那个尽量修改成另一个，对于'E'和'W'也是同样的处理方式。这样一来，一共需要的修改次数就是min(north, south) + min(east, west)，又由于存在修改次数的上限k，因此实际上执行的修改次数为

min(min(north, south) + min(east, west), k)

每次修改都可以抵消掉一次反向移动，同时新增一次通向移动，也就是说可以让当前位置与原点的距离增加2，因此修改后与远点的距离就是

abs(north - south) + abs(east - west) + min(min(north, south) + min(east, west), k) \* 2

使用这个值更新即可。

最后附上python代码：

```python
class Solution(object):
    def maxDistance(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        
        north, south, east, west = 0, 0, 0, 0
        res = 0
        for c in s:
            if c == 'N':
                north += 1
            elif c == 'S':
                south += 1
            elif c == 'E':
                east += 1
            else:
                west += 1
            
            res = max(res, abs(north - south) + abs(east - west) + min(min(north, south) + min(east, west), k) * 2)
            
        return res
```
