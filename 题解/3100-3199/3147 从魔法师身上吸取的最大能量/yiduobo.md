---
title: "3147. 从魔法师身上吸取的最大能量"
aliases: ["yiduobo的每日leetcode 3147.从魔法师身上吸取的最大能量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "题单/动态规划", "题单/贪心算法", "题单/动态规划/七-其他线性-DP", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703624243"
zhihu_id: "703624243"
zhihu_title: "yiduobo的每日leetcode 3147.从魔法师身上吸取的最大能量"
question_id: "3147"
question: "从魔法师身上吸取的最大能量"
problem_url: "https://leetcode.cn/problems/taking-maximum-energy-from-the-mystic-dungeon/"
difficulty: "Medium"
rating: 1460
created: "2024-06-16T01:23:11+08:00"
updated: "2024-06-16T01:23:11+08:00"
upvotes: 1
comments: 0
---

# 3147. 从魔法师身上吸取的最大能量

> **[yiduobo的每日leetcode 3147.从魔法师身上吸取的最大能量](https://zhuanlan.zhihu.com/p/703624243) · 知乎 · 2024-06-16 · 赞同 1**
> 力扣：[3147. 从魔法师身上吸取的最大能量](https://leetcode.cn/problems/taking-maximum-energy-from-the-mystic-dungeon/) · Medium · 灵茶山艾府：[从特殊到一般，教你如何思考本题，两种写法（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3147.从魔法师身上吸取的最大能量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/taking-maximum-energy-from-the-mystic-dungeon/description/)

题目给出一个整数数组energy，其中的元素可正可负。另外给出一个正整数k，要求从数组中找出一个起点p，从p开始按k为步长向数组末尾迭代，将过程中经过的元素累加起来。问这个累加和最大可以是多少。

题目要求计算的是最大的后缀和，于是可以先将数组反转过来，这样一来问题就变成了求数组中以k位步长分岔的最大前缀和。接下来只需从0到k - 1枚举前缀的起点，接下来以k位步长向后迭代，计算当前的前缀和并更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def maximumEnergy(self, energy, k):
        """
        :type energy: List[int]
        :type k: int
        :rtype: int
        """

        res = -1000
        energy.reverse()
        for start in range(k):
            now = 0
            for index in range(start, len(energy), k):
                now += energy[index]
                res = max(now, res)
        
        return res
```
