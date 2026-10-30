---
title: "514. 自由之路"
aliases: ["yiduobo的每日leetcode 514.自由之路"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/graph", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/shortest-path", "题单/动态规划", "题单/图论算法", "题单/字符串", "题单/动态规划/七-其他线性-DP", "题单/图论算法/一-图的遍历", "题单/字符串/九-子序列自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/259889323"
zhihu_id: "259889323"
zhihu_title: "yiduobo的每日leetcode 514.自由之路"
question_id: "514"
question: "自由之路"
problem_url: "https://leetcode.cn/problems/freedom-trail/"
difficulty: "Hard"
rating: 2400
created: "2020-09-27T23:07:54+08:00"
updated: "2020-09-27T23:07:54+08:00"
upvotes: 0
comments: 0
---

# 514. 自由之路

> **[yiduobo的每日leetcode 514.自由之路](https://zhuanlan.zhihu.com/p/259889323) · 知乎 · 2020-09-27 · 赞同 0**
> 力扣：[514. 自由之路](https://leetcode.cn/problems/freedom-trail/) · Hard · 灵茶山艾府：[两种 O(nm) 做法：DP / BFS（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

514.自由之路<https://leetcode-cn.com/problems/freedom-trail/>

动态规划的题目，题目要求一位一位输入密码，天然就给分好了状态。由于同一个字母可能出现多次，因此需要使用二维状态f[i][j]表示完成前i位，当前密码盘朝上转到第j个字符时需要的最少步数。

首先，使用一个pos_dict维护每个字符在表盘中的位置列表，然后对于每个f[i][j]：

1、若i为0，说明此时需要输入第一个字符，那么此时的起始位置时0，而目标位置是pos_dict\[key\[0\]\]中的某一个，因此对于pos_dict\[key\[0\]\]中的每个pos，都有

f[i][pos] \= dis(0, pos) + 1

其中dis(x, y)表示x选择到y所需的步数，由于有顺时针和逆时针两种转法，因此要取二者中较小的那一项。最后额外的加一代表的是按下按钮。

2、若i不为0，此时必然是从key\[i - 1\]开始进行旋转的，即当前状态为f\[i - 1\]\[last_pos\]，其中last_pos为pos_dict\[key\[i - 1\]\]中的任意一项。而此时的目标状态则是f\[i\]\[pos\]，pos为pos_dict\[key\[i\]\]中的任意一项，那么就需要枚举每个last_pos，得到

f[i][pos] \= f[i - 1][last_pos] + min(dis(last_pos, pos)) + 1

计算完所有的步骤之后，答案就是f\[len(key) - 1\]\[pos_dict\[key\[-1\]\]中的最小值。

最后附上python代码，其中j为上面的pos，k为上面的last_pos：

```python
class Solution(object):
    def findRotateSteps(self, ring, key):
        """
        :type ring: str
        :type key: str
        :rtype: int
        """

        pos_dict = {}
        for index, char in enumerate(ring):
            if char not in pos_dict:
                pos_dict[char] = []
            pos_dict[char].append(index)

        f = [[None] * len(ring) for _ in range(len(key))]

        for i in range(len(key)):
            if i == 0:
                pos_list = [0]
            else:
                pos_list = pos_dict[key[i - 1]]
            for j in pos_dict[key[i]]:
                for k in pos_list:
                    dis = min((j - k + len(ring)) % len(ring) , (k - j + len(ring)) % len(ring))
                    if i == 0:
                        f[i][j] = dis + 1
                    elif f[i][j] is None or f[i][j] > f[i - 1][k] + dis + 1:
                        f[i][j] = f[i - 1][k] + dis + 1
        
        res = None
        for pos in pos_dict[key[-1]]:
            if res is None or res > f[-1][pos]:
                res = f[-1][pos]
        return res
```
