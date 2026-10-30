---
title: "2305. 公平分发饼干"
aliases: ["yiduobo的每日leetcode 2305.公平分发饼干"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/555393928"
zhihu_id: "555393928"
zhihu_title: "yiduobo的每日leetcode 2305.公平分发饼干"
question_id: "2305"
question: "公平分发饼干"
problem_url: "https://leetcode.cn/problems/fair-distribution-of-cookies/"
difficulty: "Medium"
rating: 1887
created: "2022-08-19T00:21:11+08:00"
updated: "2022-08-19T00:21:11+08:00"
upvotes: 0
comments: 0
---

# 2305. 公平分发饼干

> **[yiduobo的每日leetcode 2305.公平分发饼干](https://zhuanlan.zhihu.com/p/555393928) · 知乎 · 2022-08-19 · 赞同 0**
> 力扣：[2305. 公平分发饼干](https://leetcode.cn/problems/fair-distribution-of-cookies/) · Medium · 灵茶山艾府：[子集状压 DP（Python/Java/C++/Go/JS）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2305.公平分发饼干

[力扣](https://leetcode.cn/problems/fair-distribution-of-cookies/)

由于每个小朋友分到的饼干数目不确定，所以在这里不再适合适用网络流和匹配相关的算法，只能老老实实用状态压缩动态规划。

令f[i][state]表示第0到第i个小朋友分走了状态值为state的饼干时的最小不公平程度，那么对于f[i][state]：

1、首先是边界情况。当i \= 0时，只有1个小朋友来分饼干，所以state中的所有饼干都分给了这个小朋友，对应的f[i][state] \= base[state]。这里的base[state]表示状态state代表的饼干总和

2、当i > 0时，则可以枚举上一轮的状态last_state。当state & last_state \= last_state时，就可以认为当前这一轮第i个小朋友是在f[i - 1][last_state]的基础上分到了状态值为state ^ last_state的饼干，此时就有

f[i][state] \= min(f[i][state], max(f[i - 1][last_state], base[state ^ last_state])

全部计算完成后，f[-1][-1]就是最终答案了。

注意到每一轮的f只与上一轮有关，因此可以利用滚动数组省略i这一维。另外，在枚举last_state时也可以通过对state进行位运算来进行枚举，效率比直接枚举所有last_state然后判断其是否为state的子状态要高。我在这里偷懒，只采用了朴素的写法。

最后附上python代码：

```python
class Solution(object):
    def distributeCookies(self, cookies, k):
        """
        :type cookies: List[int]
        :type k: int
        :rtype: int
        """

        n = len(cookies)
        value_dict = {}
        for index, c in enumerate(cookies):
            value_dict[1 << index] = c

        max_state = (1 << n)
        base = [0] * max_state
        for state in range(1, max_state):
            tmp = state & -state
            base[state] = base[state ^ tmp] + value_dict[tmp]
        
        f = base[:]
        for i in range(1, k):
            g = f[:]
            f = [8 * 100000] * max_state
            for state in range(1, max_state):
                for last_state in range(state):
                    if state & last_state == last_state:
                        f[state] = min(f[state], max(g[last_state], base[state ^ last_state]))
            
        return f[-1]
```
