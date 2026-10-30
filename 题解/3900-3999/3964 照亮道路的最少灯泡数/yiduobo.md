---
title: "3964. 照亮道路的最少灯泡数"
aliases: ["yiduobo的每日leetcode 3964.照亮道路的最少灯泡数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/二-差分", "题单/贪心算法/二-区间贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2052154994594525421"
zhihu_id: "2052154994594525421"
zhihu_title: "yiduobo的每日leetcode 3964.照亮道路的最少灯泡数"
question_id: "3964"
question: "照亮道路的最少灯泡数"
problem_url: "https://leetcode.cn/problems/minimum-lights-to-illuminate-a-road/"
difficulty: "Medium"
rating: 1572
created: "2026-06-22T22:43:46+08:00"
updated: "2026-06-22T22:44:01+08:00"
upvotes: 0
comments: 0
---

# 3964. 照亮道路的最少灯泡数

> **[yiduobo的每日leetcode 3964.照亮道路的最少灯泡数](https://zhuanlan.zhihu.com/p/2052154994594525421) · 知乎 · 2026-06-22 · 赞同 0**
> 力扣：[3964. 照亮道路的最少灯泡数](https://leetcode.cn/problems/minimum-lights-to-illuminate-a-road/) · Medium · 灵茶山艾府：[差分数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3964.照亮道路的最少灯泡数

<https://leetcode.cn/problems/minimum-lights-to-illuminate-a-road/description/>

题目给出一个长度为n的整数数组lights，表示一条路上从0到n - 1有n个位置。

对于每个位置index，记lights[index]为v：

- 若v > 0，那么index这里有一个正常工作的灯泡，其可以照亮从max(0, i - v)到min(n - 1, i + v)的每个位置，包含边界。
- 若v \= 0，那么index这里没有灯泡。

若一个位置被至少一个正常工作的灯泡照亮，那么该位置是可见的。

现在可以在任意位置安装额外的灯泡，每个安装在j的灯泡将照亮从max(0, j - 1)到min(n - 1, j + 1)的位置，包含边界。

问使得路上每个位置都可见所需安装的最少额外灯泡数量。

首先，如果不考虑额外灯泡，仅考虑如何计算被照亮的位置数目的话，使用差分数组可以很方便的解决。

具体来说，对于处在index的灯泡，记lights[index]为v，那么当v > 0时，其照明的起点为max(0, v - index)，因此需要将f[max(0, v - index)]加上1。另一方面，其将在min(n - 1, v + index) + 1失效，因此需要将f[min(n - 1, v + index) + 1]减去1。

使用所有灯泡更新完f后，只需对f进行一趟遍历，并使用一个变量now记录当前生效的灯泡数量。那么对于当前遍历到的index，先将now加上f[index]，若当前的now大于0，说明有灯泡可以照到index这个位置，否则说明当前位置没有灯泡照明。

接下来考虑如何添加额外的灯泡。

对于最左侧没被找到的位置p，如果想要为其提供照明，只能在p - 1、p、p + 1三个位置中选择一个安装额外灯泡。为了使得额外安装的灯泡数量最少，在这里显然应该在p + 1安装额外灯泡，因为左侧没有更多的照明需求，而右侧的p + 1以及p + 2则可以顺便被p + 1处的额外灯泡照亮。

基于这一点，只需对上面的遍历过程略加修改，就可以将新增额外灯泡的方案也计算进去了。具体来说，对于当前遍历到的index，依然是先将now加上f[index]，若now大于0，那么无事发生；若now等于0，那么就应该在index + 1处安装额外灯泡，此时应该将答案以及now都加上1，而这个灯泡将在index + 3处失效，因此还需要将f[min(n - 1, index + 2) + 1]减去1。

最后附上python代码：

```python
class Solution(object):
    def minLights(self, lights):
        """
        :type lights: List[int]
        :rtype: int
        """
        
        n = len(lights)
        f = [0] * (n + 1)
        for index, v in enumerate(lights):
            if v > 0:
                f[max(0, index - v)] += 1
                f[min(n - 1, index + v) + 1] -= 1

        res = 0
        now = 0
        for index in range(n):
            now += f[index]
            if now == 0:
                res += 1
                now += 1
                f[min(n - 1, index + 2) + 1] -= 1
        
        return res
```
