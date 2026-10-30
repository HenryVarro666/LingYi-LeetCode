---
title: "4008. 击败所有怪物的最小初始强度"
aliases: ["yiduobo的每日leetcode 4008.击败所有怪物的最小初始强度"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/二分算法", "题单/动态规划", "题单/二分算法/二-二分答案", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2068447850946617622"
zhihu_id: "2068447850946617622"
zhihu_title: "yiduobo的每日leetcode 4008.击败所有怪物的最小初始强度"
question_id: "4008"
question: "击败所有怪物的最小初始强度"
problem_url: "https://leetcode.cn/problems/minimum-initial-strength-to-defeat-all-monsters/"
difficulty: "Medium"
rating: 1776
created: "2026-08-05T21:54:00+08:00"
updated: "2026-08-05T21:54:04+08:00"
upvotes: 1
comments: 0
---

# 4008. 击败所有怪物的最小初始强度

> **[yiduobo的每日leetcode 4008.击败所有怪物的最小初始强度](https://zhuanlan.zhihu.com/p/2068447850946617622) · 知乎 · 2026-08-05 · 赞同 1**
> 力扣：[4008. 击败所有怪物的最小初始强度](https://leetcode.cn/problems/minimum-initial-strength-to-defeat-all-monsters/) · Medium · 灵茶山艾府：[两种方法：二分答案 / 逆向思维，附思考题（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4008.击败所有怪物的最小初始强度

<https://leetcode.cn/problems/minimum-initial-strength-to-defeat-all-monsters/description/>

题目给出一个整数数组monsters，其中monsters[index]表示第index个怪物的强度。

另外给出一个二维整数数组boosts，其中boosts\[index\] \= \[l\[index\], r\[index\], v\[index\]\]，表示与下标在\[l\[index\], r\[index\]\]范围内任意怪物战斗时，可以获得v\[index\]的临时加成。临时加成可以叠加。

现在要求以一个非负的初始强度开始，从左到右依次与怪物战斗。

对于下标为index的每个怪物：

- 令bonus表示与该怪物战斗时的所有加成值之和
- 只有当前的强度加上bonus至少为monsters[index]时，才能击败该怪物
- 击败该怪物后，当前的强度将减少monsters[index]。若强度此时变为负数，则将其重置为0。

问击败所有怪物所需的最小初始强度。

首先，题目中的加成是若干个值相同的子数组，那么在这里就可以先利用差分数组计算出每个位置的总加成，不妨记为bouns数组。

接下来，对于某个位置index，若bonus[index] >\= monsters[index]，那么可以在强度0时到达该位置，否则到达该位置所需的最小强度为monsters[index] - bonus[index]。

更进一步的，对于当前位置index：

- 若bonus足够大使得没有初始的强度需求，那么通过当前关卡所需的最小初始强度就与能通过上一关所需的最小初始强度相同，因为只要通过了上一关，就能通过这一关。
- 反过来，若bonus不够大，那么为了使得到达该位置时的初始至少为monsters[index] - bonus[index]，其初始强度必须大于等于monsters[0] + monsters[1] + ... + monsters[index - 1] + monsters[index] - bonus[index]，这样一来在通过前面的关卡到达index时，初始强度才能大于等于monsters[index] - bonus[index]。

基于以上的结论，在这里就只需要考虑所有bonus[index] \< monsters[index]的位置。若不存在这样的位置，说明所有关卡都可以通过bonus通过，此时对应的答案为0。反之，则需要取这些位置中所需的初始强度的最大值。

更进一步的，其中最大值显然就是最靠后的那一个：对于两个bonus不够大的位置p和q，方便期间，记s[index]为monsters[0] + monsters[1] + ... + monsters[index]，那么p所需的最小初始强度为

s[p] - bonus[p] \<\= s[p]

而q所需的最小初始强度为

s[q] - bonus[q] \= s[q - 1] + (monsters[q] - bonus[q]) > s[q - 1]

又由于p \< q，而s单调递增，因此必然有s[q - 1] >\= s[p]，因此对于所有bonus不够大的位置，其中初始所需强度最大的位置必然是最靠后的那个。

这样一来，只需要从后往前一趟遍历，找出最后一个bonus不够大的位置index，然后计算s[index] - bonus[index]即为最终答案。若不存在这样的index，则说明答案为0。

最后附上python代码：

```python
class Solution(object):
    def minInitialStrength(self, monsters, boosts):
        """
        :type monsters: List[int]
        :type boosts: List[List[int]]
        :rtype: int
        """
        
        n = len(monsters)
        f = [0] * n
        for left, right, v in boosts:
            f[left] += v
            if right + 1 < n:
                f[right + 1] -= v
        
        bonus = [f[0]]
        for index in range(1, n):
            bonus.append(bonus[-1] + f[index])
        
        for index in range(n - 1, -1, -1):
            if bonus[index] < monsters[index]:
                return sum(monsters[:index + 1]) - bonus[index]
        
        return 0
```
