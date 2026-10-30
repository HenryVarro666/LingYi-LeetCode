---
title: "2300. 咒语和药水的成功对数"
aliases: ["yiduobo的每日leetcode 2300.咒语和药水的成功对数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/prefix-sum", "题单/二分算法", "题单/常用数据结构", "题单/二分算法/一-二分查找", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/554168609"
zhihu_id: "554168609"
zhihu_title: "yiduobo的每日leetcode 2300.咒语和药水的成功对数"
question_id: "2300"
question: "咒语和药水的成功对数"
problem_url: "https://leetcode.cn/problems/successful-pairs-of-spells-and-potions/"
difficulty: "Medium"
rating: 1477
created: "2022-08-16T00:42:33+08:00"
updated: "2022-08-16T00:42:33+08:00"
upvotes: 0
comments: 0
---

# 2300. 咒语和药水的成功对数

> **[yiduobo的每日leetcode 2300.咒语和药水的成功对数](https://zhuanlan.zhihu.com/p/554168609) · 知乎 · 2022-08-16 · 赞同 0**
> 力扣：[2300. 咒语和药水的成功对数](https://leetcode.cn/problems/successful-pairs-of-spells-and-potions/) · Medium · 灵茶山艾府：[两种方法：排序+二分 / 计数+值域后缀和（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2300.咒语和药水的成功对数

[力扣](https://leetcode.cn/problems/successful-pairs-of-spells-and-potions/)

对于咒语s，设最小的能成功发动的药水强度为need，那么题目实际上就是要求potions中有多少个数大于等于need。

首先是关于need的计算。在这里直接用success除以s，然后根据是否能够整除就能得到need了。

接下来是potions中有多少个数大于等于need的求解。这是一个离线的问题，同时potions中的数取值范围并不算大，因此可以使用各式各样的方法求解，例如二分、树状数组等。我在这里使用的是动态规划。令f[i]表示potions中大于等于i的数有多少个，那么对于f[i]就有f[i] \= f[i + 1] + cnt[i]。这里的cnt[i]表示i在potions中出现的次数。边界情况自然是f[max(potions)] \= cnt[max(potions)]。

得到f后，枚举spells中的所有s，计算对应的need。若这个need已经大于potions中的最大值，那么不可能发动成功，因此对应的答案为0，否则这个法术对应的答案就是f[need]。

最后附上python代码：

```python
class Solution(object):
    def successfulPairs(self, spells, potions, success):
        """
        :type spells: List[int]
        :type potions: List[int]
        :type success: int
        :rtype: List[int]
        """

        ma = max(potions)
        f = [0] * (ma + 1)

        cnt_dict = {}
        for p in potions:
            cnt_dict[p] = cnt_dict.get(p, 0) + 1
        
        f[ma] = cnt_dict.get(ma, 0)
        for num in range(ma - 1, -1, -1):
            f[num] = f[num + 1] + cnt_dict.get(num, 0)

        res = []
        for s in spells:
            need = success / s
            if success % s != 0:
                need += 1

            if need > ma:
                res.append(0)
            else:
                res.append(f[need])
        
        return res
```
