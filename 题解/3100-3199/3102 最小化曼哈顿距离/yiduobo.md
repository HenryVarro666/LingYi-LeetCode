---
title: "3102. 最小化曼哈顿距离"
aliases: ["yiduobo的每日leetcode 3102.最小化曼哈顿距离"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/geometry", "leetcode/math", "leetcode/ordered-set", "leetcode/bian-li", "题单/数学算法", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/699972873"
zhihu_id: "699972873"
zhihu_title: "yiduobo的每日leetcode 3102.最小化曼哈顿距离"
question_id: "3102"
question: "最小化曼哈顿距离"
problem_url: "https://leetcode.cn/problems/minimize-manhattan-distances/"
difficulty: "Hard"
rating: 2216
created: "2024-05-27T00:21:55+08:00"
updated: "2024-05-27T00:21:55+08:00"
upvotes: 1
comments: 0
---

# 3102. 最小化曼哈顿距离

> **[yiduobo的每日leetcode 3102.最小化曼哈顿距离](https://zhuanlan.zhihu.com/p/699972873) · 知乎 · 2024-05-27 · 赞同 1**
> 力扣：[3102. 最小化曼哈顿距离](https://leetcode.cn/problems/minimize-manhattan-distances/) · Hard · 灵茶山艾府：[【图解】曼哈顿距离转切比雪夫距离（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3102.最小化曼哈顿距离

[. - 力扣（LeetCode）](https://leetcode.cn/problems/minimize-manhattan-distances/description/)

题目给出一些点，要求从中删去一个，使得剩下点两两之间的距离的最大值最小。

对于曼哈顿距离相关的问题，一种常见的处理方法就是开绝对值。不妨设两个点i和j的坐标分别为(x[i], x[j])，(y[i], y[j])，那么二者距离就是

| x[i] - x[j] | + | y[i] - y[j] |

把绝对值打开一共有四种情况，分别是

x[i] - x[j] + y[i] - y[j]

x[i] - x[j] - y[i] + y[j]

-x[i] + x[j] + y[i] - y[j]

-x[i] + x[j] - y[i] + y[j]

把i和j的项放到一起，就有

(x[i] + y[i]) - (x[j] + y[j])

(x[i] - y[i]) - (x[j] - y[j])

-(x[i] - y[j]) + (x[j] - y[j])

-(x[i] + y[i]) + (x[j] + y[j])

可以发现，上面式子中的项要么是x与y的和，要么是x与y的差，那么不妨设d[i] \= x[i] - y[i]，s[i] \= x[i] + y[i]，那么就有

s[i] - s[j]

d[i] - d[j]

-(d[i] - d[j])

-(s[i] - s[j])

即最大的曼哈顿距离一定是某两个s之差或者某两个d之差。于是可以先计算出s数组和d数组，然后分别排序，那么取最大的s与最小的s作差，以及最大的d与最小的d作差，就可以得到原始的最大曼哈顿距离。

接下来，遍历每个点，计算删除该点后剩余点的最大曼哈顿距离。

若当前点的x与y之和与最大的s或者最小的s相同，那么就需要选取次大的s或者次小的s重新计算s之差的部分，否则s之差的部分保持不变。

同样的，若x与y之差与最大的d或者最小的d相同，那么也需要选择次大的d或者次小的d重新计算d之差的部分，否则d之差的部分保持不变。

最后取s之差和d之差中的较大值即为当前的最大距离，取这些最大距离中最小的那个作为最终答案即可。

最后附上python代码：

```python
class Solution(object):
    def minimumDistance(self, points):
        """
        :type points: List[List[int]]
        :rtype: int
        """

        s = sorted([x + y for x, y in points])
        d = sorted([x - y for x, y in points])
        
        res = max(s[-1] - s[0], d[-1] - d[0])
        for x, y in points:
            if x + y == s[0]:
                sv = s[-1] - s[1]
            elif x + y == s[-1]:
                sv = s[-2] - s[0]
            else:
                sv = s[-1] - s[0]
            
            if x - y == d[0]:
                dv = d[-1] - d[1]
            elif x - y == d[-1]:
                dv = d[-2] - d[0]
            else:
                dv = d[-1] - d[0]
            
            res = min(res, max(sv, dv))

        return res
```
