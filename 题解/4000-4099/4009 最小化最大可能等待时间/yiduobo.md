---
title: "4009. 最小化最大可能等待时间"
aliases: ["yiduobo的每日leetcode 4009.最小化最大可能等待时间"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/memoization", "leetcode/hash-table", "leetcode/binary-search", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2068454799822131362"
zhihu_id: "2068454799822131362"
zhihu_title: "yiduobo的每日leetcode 4009.最小化最大可能等待时间"
question_id: "4009"
question: "最小化最大可能等待时间"
problem_url: "https://leetcode.cn/problems/minimum-possible-maximum-waiting-time/"
difficulty: "Hard"
rating: 2499
created: "2026-08-05T22:23:38+08:00"
updated: "2026-08-05T22:23:38+08:00"
upvotes: 0
comments: 0
---

# 4009. 最小化最大可能等待时间

> **[yiduobo的每日leetcode 4009.最小化最大可能等待时间](https://zhuanlan.zhihu.com/p/2068454799822131362) · 知乎 · 2026-08-05 · 赞同 0**
> 力扣：[4009. 最小化最大可能等待时间](https://leetcode.cn/problems/minimum-possible-maximum-waiting-time/) · Hard · 灵茶山艾府：[两种方法：多维 DP / 二分答案 + DFS 搜索（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4009.最小化最大可能等待时间

<https://leetcode.cn/problems/minimum-possible-maximum-waiting-time/description/>

题目给出一个整数数组demand，长度不超过50。其中demand[index]表示第index辆车所需的燃料量，其大小不超过20。

同时给出一个长度为2的整数数组fuel，表示恰好两个加油机，编号为0和1，其中fuel[index]表示index这一台加油机的初始燃料量，其大小不超过50。

现在要让车辆按照递增的下标顺序开始加油。第0辆车在时间0被允许加油，而对于后续的index > 0，只有当第index - 1开始加油时，第index辆车才被允许加油。

另外，还有一些规则需要遵守：

- 每个加油机一次最多只能给一辆车加油
- 车辆可以在被允许时，或者之后的任意时间开始加油
- 只有当加油机空闲，且剩余的燃料至少为demand[index]时，index这辆车才能开始加油
- 若两台加油机都空闲，则可以选择任意一个
- 给index这辆车加油所需的时间为demand[index]秒，同时加油完成后剩余燃料会减少demand[index]
- 一旦开始加油，就必须加满当前车辆
- 若两个加油机都空闲，但是燃料都不足以给当前车辆加油，那么加油过程中止

车辆的等待时间为这辆车被允许开始加油，到其实际开始加油之间的时间。

问在使得可以加油的车辆最多的情况下，所有车辆等待时间中的最大值，最小可能是多少。若所有车辆都没法被加油，则返回-1。

对于这类调度问题，要么搜索回溯，要么动态规划。基于本题的数据规模，应该就是动态规划。

状态表示也比较直观：

f[index][wait][r0][r1]表示index这辆车在第一台机器加油，且第二台机器还需要wait的时间才能空出来，同时两台机器剩余的燃料分别为r0和r1时，已经加油的车所需等待时间中最大值最小可能是多少。

g[index][wait][r0][r1]则表示index这辆车在第二台机器加油，且第一台机器还需要wait的时间才能空出来，同时两台机器剩余的燃料分别为r0和r1时，已经加油的车所需等待时间中最大值最小可能是多少。

值得一提的是，以上的状态表示隐含了两个信息：首先是index在第一台机器加油，说明第0到第index台车都加了油，也就是说计算完成后，需要找出index最大的可达状态，表示让尽量多的车辆加油，然后取其中的最小值。第二个就是确定了index这辆车加油的机器，也就意味着这台机器将被占用demand[index]的时间，与wait配合使用就可以直到下一辆车在任意一台机器排队加油所需的等待时间。

由于可达的状态应该并不多，因此在这里使用哈希表而不是数组是更好的方案，即将(wait, r0, r1)打包成为哈希表的key，那么对于f和g：

1、首先是边界情况。

若demand[0] \<\= fuel[0]，那么第0台车可以在第一台机器加油，此时就有f[(0, fuel[0] - demand[0], fuel[1])] \= 0，这里的key为(0, fuel[0] - demand[0], fuel[1])，分别表示第二台机器目前不需要等待、第一台机器剩下fuel[0] - demand[0]的燃料、第二台机器剩下fuel[1]的燃料。

同样的，若demand[0] \<\= fuel[1]，那么有g[(0, fuel[0], fuel[1] - demand[0])] \= 0，其含义与f对称。

2、接下来对于index > 0的情况：

2-1）首先考虑上一辆车在第一台机器加油的情况，此时需要枚举f[index - 1]中的所有key，对于当前枚举到的pre，首先从pre中分离出wait、r0、r1，接下来：

2-1-1）若r0 >\= demand[index]，说明当前车辆可以在第一台机器加油。

对于这种情况，需要等待上一辆车加完油，那么接下来第二台机器所需的等待时间wait将过去demand[index - 1]，还剩下max(0, wait - demand[index - 1])，在这里记为nxt_wait。

另外，第一台机器的油量在为当前车辆加油后用掉了demand[index]，因此有下一个状态nxt_key \= (nxt_wait, r0 - demand[index], r1)。

于是就有f[index][nxt_key] \= min(f[index][nxt_key], max(f[index - 1][pre], demand[index - 1]))

2-1-2）若r1 >\= demand[index]，说明当前车辆可以在第二台机器加油。

对于这种情况，需要等待第二台机器中加油的车辆加完，也就是需要等待wait的时间，那么此时在第一台机器中加油的车辆还需要max(0, demand[index - 1] - wait)的时间才能加完油，于是就有nxt_wait \= max(0, demand[index - 1] - wait)。

另外，第二台机器的油量在为当前车辆加油后用掉了demand[index]，因此有下一个状态nxt_key \= (nxt_wait, r0, r1 - demand[index])。

于是就有g[index][nxt_key] \= min(g[index][nxt_key], max(f[index - 1][pre], wait))

2-2）接下来考虑上一辆车在第二台机器加油的情况，此时需要枚举g[index - 1]中的所有key，对于当前枚举到的pre，同样是分离出wait、r0、r1，接下来：

2-2-1）若r0 >\= demand[index]，说明当前车辆可以在第一台机器加油。

这种情况与2-1-2完全对称，有nxt_key \= (max(0, demand[index - 1] - wait), r0 - d, r1)

以及f[index][nxt_key] \= min(f[index][nxt_key], max(g[index - 1][pre], wait))

2-2-2）若r1 >\= demand[index]，说明当前车辆可以在第二台机器加油。

这种情况与2-1-1完全对称，有nxt_key \= (max(0, wait - demand[index - 1]), r0, r1 - d)

以及g[index][nxt_key] \= min(g[index][nxt_key], max(g[index - 1][pre], demand[index - 1]))

若某一轮计算时不存在合法的f[index][nxt_key]以及g[index][nxt_key]，说明index这辆车是无法被加油的，此时取f[index - 1]以及g[index - 1]中所有key对应的最小值即为最终答案。

另外注意到每一轮的状态只与上一轮有关，因此在这里可以通过滚动哈希表省去index这一维。

最后附上python代码：

```python
class Solution(object):
    def minMaxWaitingTime(self, demand, fuel):
        """
        :type demand: List[int]
        :type fuel: List[int]
        :rtype: int
        """
        
        ma = max(demand)
        f = {}
        g = {}
        if demand[0] <= fuel[0]:
            f[(0, fuel[0] - demand[0], fuel[1])] = 0

        if demand[0] <= fuel[1]:
            g[(0, fuel[0], fuel[1] - demand[0])] = 0

        for index in range(1, len(demand)):
            d = demand[index]
            nxt_f = {}
            nxt_g = {}
            for pre in f:
                wait, r0, r1 = pre
                if r0 >= d:
                    nxt_wait = max(0, wait - demand[index - 1])
                    nxt_key = (nxt_wait, r0 - d, r1)
                    if nxt_key not in nxt_f or nxt_f[nxt_key] > max(f[pre], demand[index - 1]):
                        nxt_f[nxt_key] = max(f[pre], demand[index - 1])

                if r1 >= d:
                    nxt_wait = max(0, demand[index - 1] - wait)
                    nxt_key = (nxt_wait, r0, r1 - d)
                    if nxt_key not in nxt_g or nxt_g[nxt_key] > max(f[pre], wait):
                        nxt_g[nxt_key] = max(f[pre], wait)
            
            for pre in g:
                wait, r0, r1 = pre
                if r0 >= d:
                    nxt_wait = max(0, demand[index - 1] - wait)
                    nxt_key = (nxt_wait, r0 - d, r1)
                    if nxt_key not in nxt_f or nxt_f[nxt_key] > max(g[pre], wait):
                        nxt_f[nxt_key] = max(g[pre], wait)
                
                if r1 >= d:
                    nxt_wait = max(0, wait - demand[index - 1])
                    nxt_key = (nxt_wait, r0, r1 - d)
                    if nxt_key not in nxt_g or nxt_g[nxt_key] > max(g[pre], demand[index - 1]):
                        nxt_g[nxt_key] = max(g[pre], demand[index - 1])
            
            if not nxt_f and not nxt_g:
                break
            f = copy.deepcopy(nxt_f)
            g = copy.deepcopy(nxt_g)
    
        res = -1
        if f:
            res = min(f.values())
        if g:
            mi_g = min(g.values())
            if res == -1 or res > mi_g:
                res = mi_g
        
        return res
```
