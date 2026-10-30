---
title: "3953. 互质元素的最大得分"
aliases: ["yiduobo的每日leetcode 3953.互质元素的最大得分"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2047802427588588932"
zhihu_id: "2047802427588588932"
zhihu_title: "yiduobo的每日leetcode 3953.互质元素的最大得分"
question_id: "3953"
question: "互质元素的最大得分"
problem_url: "https://leetcode.cn/problems/maximum-score-with-co-prime-element/"
difficulty: "Hard"
rating: 2390
created: "2026-06-09T23:11:15+08:00"
updated: "2026-06-09T23:11:20+08:00"
upvotes: 1
comments: 0
---

# 3953. 互质元素的最大得分

> **[yiduobo的每日leetcode 3953.互质元素的最大得分](https://zhuanlan.zhihu.com/p/2047802427588588932) · 知乎 · 2026-06-09 · 赞同 1**
> 力扣：[3953. 互质元素的最大得分](https://leetcode.cn/problems/maximum-score-with-co-prime-element/) · Hard · 灵茶山艾府：[容斥 + 分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3953.互质元素的最大得分

<https://leetcode.cn/problems/maximum-score-with-co-prime-element/description/>

题目给出一个长度为n的正整数数组nums，以及一个整数maxVal。其中n、nums中的元素大小、maxVal均不超过10^5。

现在可以将nums中任意元素修改为小于等于maxVal的任意正整数，每次修改的代价为1。

在进行完所有的修改之后，需要选择一个下标index，满足nums[index]与其他元素都互质。

令：

- selectedValue为修改后的nums[index]的最终值
- modificationCost为修改的元素总数

得分定义为score \= selectedValue - modificationCost

问最大可能的得分是多少。

由于nums中的元素大小以及maxVal都不超过10^5，因此最终的selectedValue必然落在1到10^5之间，那么在这里就可以尝试枚举这个selectedValue，然后计算对应的得分。

需要注意的是，基于题目中的修改规则，最终的selectedValue要么在1到maxVal之间，要么本来就在nums中出现过，因为题目不支持将元素修改为大于maxVal的数，因此selectedValue如果大于maxVal，其必须原本就是nums中的一员。

基于这一点，可以分成两段进行讨论。

对于1到maxVal之间的选定的selectedValue，现在需要知道nums中与其不互质的元素数量，在这里不妨使用一个数组f，其中f[v]表示nums中与v不互质的元素数量，那么：

- 若f[selectedValue]为0：这种情况下，说明nums中既没有selectedValue，也没有与selectedValue互质的元素。此时必须选择任意一个元素，将其变为selectedValue，最终的score就是selectedValue - 1。
- 若f[selectedValue]非0，且nums中存在selectedValue：这种情况下，可以选择任意一个初始值恰好等于selectedValue不变，然后将其他与selectedValue不互质的元素都修改成1，总的修改次数为f[selectedValue] - 1。这里选择修改成1最简洁，因为1与任意正整数互质。此时的score就是selectedValue - (f[selectedValue] - 1)。
- 若f[selectedValue]非0，且nums中不存在selectedValue：此时则可以从所有与selectedValue不互质的元素中选择一个，将其修改为selectedValue，然后将其他元素修改为1，总的修改次数为f[selectedValue]。此时的score就是selectedValue - f[selectedValue]。

而对于大于maxVal的selectedValue，其必须在nums中出现过，因此此时的score与上面的情况2对应，即selectedValue - (f[selectedValue] - 1)。

到了这里，问题就变成了如何计算nums中与特定值不互质的元素数量v。

对于任意两个不互质的元素x和y，至少存在一个质因子p，满足x和y同时为p的倍数。基于这一点，在这里就可以尝试枚举所有质数p，以p作为桥梁连接起所有p的倍数。

具体来说，先使用一个哈希表cnt记录nums中每种元素出现的次数，另外记ma为max(max(nums)， maxVal)，接下来使用类似筛法的方法，枚举所有小于等于ma的质数p。

对于当前的p，从p开始，以p为步长枚举不超过ma的2p、3p、...、kp，并使用一个变量tot统计cnt[p]、cnt[2p]、...、cnt[kp]之和。那么对于任意一个p的倍数mp而言，数组中一共有tot个p的倍数，除去mp自身之外，还有其他tot - 1个元素同样是p的倍数，也就是说在讨论p的语境下，有tot - 1个元素与mp不互质，也就是说此时应该将tot - 1累加到f[p]、f[2p]、...、f[kp]当中。

但是需要注意的是，以上的计算方法可能产生重复，例如[2, 3, 6, 12]，按以上的计算方法最终会得到f[6] \= 4，理由是在计算p \= 2时，6会计算与2和12不互质，而计算p \= 3时，6会计算与3和12不互质，可以发现，这里12被计算了两次。

为了处理这种问题，则需要用到容斥原理。具体来说，在这里除了通过质数p计算f数组之外，还需要计算所有由不重复的质因子之积构成的元素v的倍数。若这个v等于偶数个质因子之积，那么就需要从f中减去其对应的tot - 1，反之则应该加回来。

与容斥原理有关的详细内容可以参考之前的3757题，这里就不展开了。

[yiduobo的每日leetcode 3757.有效子序列的数量](https://zhuanlan.zhihu.com/p/1976053960189161764)

值得一提的是，在这里仅需要对由不同质因子之积构成的元素进行计算，理由是最初始的计算是基于单个质数的，也就是说像4、9这种元素是没有执行过计算的，因此也无需计算12、18这种元素来消除重复的影响。

在具体实现上，可以使用一个数组g来帮助计算，其中g[v]的初始值为v。接下来从2到ma枚举v：

1、若当前的g[v]就等于v，说明v是质数，直接计算。在从2v枚举到kv的过程中，对于当前枚举到的x，需要将对应的g[x]除以-v。

2、若当前的g[v]等于1，说明v是由偶数个质因子之积构成的，这样一来才会在之前枚举各个质因子的过程中对g[v]不断修正，最终变为1。这种情况下，需要将本次统计的tot - 1从f[2v]、f[3v]、...、f[kv]当中减去。需要注意，此时不需要修正g[2v]、g[3v]、...、g[kv]。

3、若当前的g[v]等于-1，说明v是由奇数个质因子之积构成的，此时与情况2反过来操作就行了。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, nums, maxVal):
        """
        :type nums: List[int]
        :type maxVal: int
        :rtype: int
        """
        
        ma = maxVal
        cnt = {}
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            ma = max(ma, v)
        
        f = [0] * (ma + 1)
        g = [v for v in range(ma + 1)]

        for v in range(2, ma + 1):
            if g[v] == v:
                tot = 0
                for x in range(v, ma + 1, v):
                    tot += cnt.get(x, 0)
                    g[x] //= -v
                
                for x in range(v, ma + 1, v):
                    f[x] += tot
            
            elif abs(g[v]) == 1:
                tot = 0
                for x in range(v, ma + 1, v):
                    tot += cnt.get(x, 0)
                
                for x in range(v, ma + 1, v):
                    f[x] -= g[v] * tot
        
        if 1 in cnt:
            res = 1
        else:
            res = 0

        for v in range(2, maxVal + 1):
            if v in cnt:
                res = max(res, v - (f[v] - 1))
            elif f[v] == 0:
                res = max(res, v - 1)
            else:
                res = max(res, v - f[v])

        for v in range(maxVal + 1, ma + 1):
            if v in cnt:
                res = max(res, v - (f[v] - 1))
        
        return res
```
