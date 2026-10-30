---
title: "2830. 销售利润最大化"
aliases: ["yiduobo的每日leetcode 2830.销售利润最大化"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/659277268"
zhihu_id: "659277268"
zhihu_title: "yiduobo的每日leetcode 2830.销售利润最大化"
question_id: "2830"
question: "销售利润最大化"
problem_url: "https://leetcode.cn/problems/maximize-the-profit-as-the-salesman/"
difficulty: "Medium"
rating: 1851
created: "2023-10-02T01:52:02+08:00"
updated: "2023-10-02T01:52:03+08:00"
upvotes: 0
comments: 0
---

# 2830. 销售利润最大化

> **[yiduobo的每日leetcode 2830.销售利润最大化](https://zhuanlan.zhihu.com/p/659277268) · 知乎 · 2023-10-02 · 赞同 0**
> 力扣：[2830. 销售利润最大化](https://leetcode.cn/problems/maximize-the-profit-as-the-salesman/) · Medium · 灵茶山艾府：[线性 DP，附相似题目（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2830.销售利润最大化

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/maximize-the-profit-as-the-salesman/)

注意到本题中房屋的坐标都处于10^5内，那么就可以利用这一点建立动态规划的状态。令f[i]表示下标位置0到i的所有房屋可以卖出的最大价格。对于f[i]，首先可以无视位于下标i的房屋，那么就可以初始化f[i] \= f[i - 1]。另外，也可以选择end为i的某个offer，也就是对于任意满足end[j] \= i的offer(start[j], end[j], gold[j])，都有f[i] \= max(f[i], f[start[j] - 1] + gold[j])。在这里需要注意边界情况的处理，主要是0的情况。

另外需要注意的是，状态转移时显然不能每次都遍历所有offer，我在这里采用的做法是使用一个哈希表end_dict将所有offer按照end收集起来，当计算到f[i]时，只需便利end_dict[i]中的offer就行了。

最后附上python代码：

```python
class Solution(object):
    def maximizeTheProfit(self, n, offers):
        """
        :type n: int
        :type offers: List[List[int]]
        :rtype: int
        """

        end_dict = {}
        for start, end, gold in offers:
            if end not in end_dict:
                end_dict[end] = []
            end_dict[end].append([start, gold])
        
        f = []
        for index in range(n):
            if index > 0:
                f.append(f[-1])
            else:
                f.append(0)

            for start, gold in end_dict.get(index, []):
                if start == 0:
                    v = gold
                else:
                    v = gold + f[start - 1]

                f[-1] = max(f[-1], v)
        
        return f[-1]
```
