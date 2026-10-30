---
title: "1655. 分配重复整数"
aliases: ["yiduobo的每日leetcode 1655.分配重复整数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/441253126"
zhihu_id: "441253126"
zhihu_title: "yiduobo的每日leetcode 1655.分配重复整数"
question_id: "1655"
question: "分配重复整数"
problem_url: "https://leetcode.cn/problems/distribute-repeating-integers/"
difficulty: "Hard"
rating: 2307
created: "2021-12-04T19:42:45+08:00"
updated: "2021-12-04T19:42:46+08:00"
upvotes: 0
comments: 0
---

# 1655. 分配重复整数

> **[yiduobo的每日leetcode 1655.分配重复整数](https://zhuanlan.zhihu.com/p/441253126) · 知乎 · 2021-12-04 · 赞同 0**
> 力扣：[1655. 分配重复整数](https://leetcode.cn/problems/distribute-repeating-integers/) · Hard · 灵茶山艾府：[Go 子集状压 DP](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1655.分配重复整数

[力扣](https://leetcode-cn.com/problems/distribute-repeating-integers/)

题目中m的规模非常小，那么状态压缩动态规划甚至暴力dfs应该都是可行的，不过还是先想想能不能找出多项式复杂度的算法。

题目与经典的圆桌问题很像，但是有一处不同的地方是圆桌问题要求每个订单由不同的数字组成，而这里则要求每个订单由同一种数组组成，这就为建图带来了困难。

而如果使用贪心，那么自然的想法就是优先使用出现次数较少的数字，但是在使用过程中无法给出一种正确的分配规则。例如某个出现5次的数字需要分配给1、2、3、4这几个订单，那么根本就无法确定是应该选择1和4还是选择2和3，无论哪种方法都可以找出反例。

到了最后还是只能老老实实用状态压缩动态规划来做。

首先对nums进行一趟遍历，统计出每种数字出现的个数，记为cnt_list。

令f[i][state]表示用前i种数字是否能够满足state表示的客户订单，那么对于f[i][state]，可以先初始化为f[i - 1][state]，表示直接使用前i - 1种数字是否能满足state表示的客户订单。接下来可以枚举state的所有子集sub_state，通过前i - 1中数字满足sub_state表示的客户订单，而state ^ sub_state这些客户的订单则全部通过第i种数字完成。此时需要满足的条件就是f[i - 1][sub_state]为true，且state ^ sub_state这些客户的订单总数小于等于第i种数字出现的次数。

为了方便计算，可以先预处理出每种state所需的数字总数，记为s，那么state ^ sub_state这些客户所需的订单总数就是s[state] - s[sub_state]。

于是就有转移方程

f[i][state] \= f[i - 1][state] or

(f\[i - 1\]\[sub_state\[0\]\] and s\[state\] - s\[sub_state\[0\]\] \<\= cnt) or

(f\[i - 1\]\[sub_state\[1\]\] and s\[state\] - s\[sub_state\[1\]\] \<\= cnt) or

...

(f\[i - 1\]\[sub_state\[-1\]\] and s\[state\] - s\[sub_state\[-1\]\] \<\= cnt)

动态规划完成后，f[-1][-1]就是最终答案了。

注意到这里每一轮的状态只与上一轮有关，且f的初始化结果就是上一轮的结果，那么可以调整state的枚举顺序从大到小进行枚举，从而达到省去i这一维的目的。

最后附上python代码：

```python
class Solution(object):
    def canDistribute(self, nums, quantity):
        """
        :type nums: List[int]
        :type quantity: List[int]
        :rtype: bool
        """

        cnt_dict = {}
        for num in nums:
            cnt_dict[num] = cnt_dict.get(num, 0) + 1
        
        cnt_list = cnt_dict.values()
        n = len(cnt_list)
        
        m = len(quantity)
        max_state = 1 << m
        s = [0] * max_state
        for state in range(1, max_state):
            for index in range(m):
                if state & (1 << index):
                    s[state] = s[state ^ (1 << index)] + quantity[index]
                    break
        
        f = [False] * max_state
        for state in range(max_state):
            if s[state] <= cnt_list[0]:
                f[state] = True

        for cnt in cnt_list[1:]:
            for state in range(max_state - 1, 0, -1):
                if f[state]:
                    continue
                sub_set = set([0])
                for index in range(m):
                    if state & (1 << index):
                        sub_set.update(set([x | (1 << index) for x in sub_set]))

                for sub_state in sub_set:
                    if f[sub_state] and s[state] - s[sub_state] <= cnt:
                        f[state] = True
                        break
        
        return f[-1]
```
