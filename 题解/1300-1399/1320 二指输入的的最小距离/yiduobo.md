---
title: "1320. 二指输入的最小距离"
aliases: ["yiduobo的每日leetcode 1320.二指输入的最小距离"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/393754110"
zhihu_id: "393754110"
zhihu_title: "yiduobo的每日leetcode 1320.二指输入的最小距离"
question_id: "1320"
question: "二指输入的的最小距离"
problem_url: "https://leetcode.cn/problems/minimum-distance-to-type-a-word-using-two-fingers/"
difficulty: "Hard"
rating: 2028
created: "2021-07-27T22:50:25+08:00"
updated: "2021-07-27T22:50:25+08:00"
upvotes: 0
comments: 0
---

# 1320. 二指输入的最小距离

> **[yiduobo的每日leetcode 1320.二指输入的最小距离](https://zhuanlan.zhihu.com/p/393754110) · 知乎 · 2021-07-27 · 赞同 0**
> 力扣：[1320. 二指输入的的最小距离](https://leetcode.cn/problems/minimum-distance-to-type-a-word-using-two-fingers/) · Hard · 灵茶山艾府：[教你一步步思考 DP：记忆化搜索 -> 递推 -> 空间优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1320.二指输入的最小距离

[力扣](https://leetcode-cn.com/problems/minimum-distance-to-type-a-word-using-two-fingers/)

动态规划的题目，令f[i][first][second]表示前i步，第一个手指在first上，第二个手指在second上所需的最小移动步数，那么这里一共有27 \* 27 \= 729中可能性。这里的27表示的是26个字母，再加上还没有使用过手指这种情况。

初始情况下，除了f[0][0][0]之外都为空，f[0][0][0]为0。

接下来我们一趟扫描，枚举word中的每个字符。

对于当前字符char，再枚举上一轮所有不为空的状态，设为f[i - 1][first][second]，那么我们可以将第一个手指从first移动到char，于是就有

f[i][char][second] \= min(f[i][char][second], f[i - 1][first][second] + dis(first, char))

同样地，也可以将第二个手指从first移动到second，于是就有

f[i][first][char] \= min(f[i][first][char], f[i - 1][first][second] + dis(char, second))

我们可以一开始先将dis数组计算出来，就可以在O(729 \* n)的时间复杂度内完成计算了。至于具体的计算方式，首先有0到任何字符的距离都是0，而对于不为0的两个字符，可以将a到z编码为1到26，那么每个字符对应的下标就是分别除以6和模6。得到坐标之后计算曼哈顿距离就是字母在表格中的距离了。

另外，由于每一轮的状态都只与上一轮有关，因此可以使用滚动数组来优化空间。

最后附上python代码：

```python
class Solution(object):
    def minimumDistance(self, word):
        """
        :type word: str
        :rtype: int
        """

        dis = [[0] * 27 for _ in range(27)]
        x = [index / 6 for index in range(26)]
        y = [index % 6 for index in range(26)]
        for i in range(1, 27):
            for j in range(1, 27):
                dis[i][j] = abs(x[i - 1] - x[j - 1]) + abs(y[i - 1] - y[j - 1])
        
        f = [[None] * 27 for _ in range(27)]
        f[0][0] = 0
        for char in word:
            num = ord(char) - 64
            g = [[None] * 27 for _ in range(27)]
            for first in range(27):
                for second in range(27):
                    if f[first][second] is not None:
                        if g[num][second] is None or g[num][second] > f[first][second] + dis[first][num]:
                            g[num][second] = f[first][second] + dis[first][num]
                        if g[first][num] is None or g[first][num] > f[first][second] + dis[second][num]:
                            g[first][num] = f[first][second] + dis[second][num]
            
            f = g[:]
        
        res = None
        for first in range(27):
            for second in range(27):
                if f[first][second] is not None and (res is None or res > f[first][second]):
                    res = f[first][second]
        
        return res
```
