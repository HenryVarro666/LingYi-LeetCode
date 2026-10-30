---
title: "1900. 最佳运动员的比拼回合"
aliases: ["yiduobo的每日leetcode 1900.最佳运动员的比拼回合"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/贪心算法", "题单/动态规划/七-其他线性-DP", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/480361954"
zhihu_id: "480361954"
zhihu_title: "yiduobo的每日leetcode 1900.最佳运动员的比拼回合"
question_id: "1900"
question: "最佳运动员的比拼回合"
problem_url: "https://leetcode.cn/problems/the-earliest-and-latest-rounds-where-players-compete/"
difficulty: "Hard"
rating: 2455
created: "2022-03-13T22:00:42+08:00"
updated: "2022-03-13T22:00:42+08:00"
upvotes: 0
comments: 0
---

# 1900. 最佳运动员的比拼回合

> **[yiduobo的每日leetcode 1900.最佳运动员的比拼回合](https://zhuanlan.zhihu.com/p/480361954) · 知乎 · 2022-03-13 · 赞同 0**
> 力扣：[1900. 最佳运动员的比拼回合](https://leetcode.cn/problems/the-earliest-and-latest-rounds-where-players-compete/) · Hard · 灵茶山艾府：[【图解】从 O(n^4) 到 O(1)：动态规划 / 贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1900.最佳运动员的比拼回合

[力扣](https://leetcode-cn.com/problems/the-earliest-and-latest-rounds-where-players-compete/)

很有意思题目。当然，如果是在当年比赛中碰到的话，我一定会选择对于每个n，first和second，都随机生成十万组运动员的实力数组，然后模拟比赛情况，根据收集到的数据通过打表的方式提交最后的答案。这样的话就可以把时间留给其他题目了。

回到本体，感觉应该有构造的方法，但是没有想得太清楚，只能老老实实用动态规划求解。

状态表示是比较直观的，令f[n][left][right]表示现在还有n个运动员，其中最强的两个运动员分别在从左往右数的第left和right的位置上时，二人遭遇需要的最少轮次，g表示同样位置状况下二人遭遇需要的最多轮次。那么：

1、f[n][left][right] \= f[n][right][left]

这个结论很直观，因为在这两个运动员碰上之前没人可以打过这两个人，那么这两个人其实是完全等价的，因此就有了上面的结论。根据这一点，在计算f的时候就可以只计算left \< right的部分

2、f[n][left][right] \= f[n][n - right + 1][n - left +1]

由于比赛是按头尾对称安排的，因此在这里从左向右的第left和第right个人与从右向左的第left和第right个人是一样的，对应起来的话从左向右的第left个人对应到从右向左的第left个人，也就是从左往右数的第n - left + 1个人。同样的，第right个人对应到从左往右数的第n - right + 1个人。那么就有

f[n][left][right] \= f[n][n - left + 1][n - right + 1]

再根据结论1，在这里还是将较小的位置放在前面方便计算，那么就有

f[n][left][right] \= f[n][n - right + 1][n - left + 1]

当然，g也满足上面的结论。

以上是根据对称性的一些结论，接下来要具体计算f和g。方便起见，在这里采用记忆化搜索来实现：

1、若f[n][left][right]或者f[n][n - right + 1][n - left + 1]被计算过，那么直接返回

2、若left + right \= n + 1：

那么说明这一轮二人就遭遇了，于是就有f[n][left][right] \= g[n][left][right] \= 1。在这里不要忘了将f[n][right][left]以及g[n][right][left]也赋值为1。

另外，在这里无需处理f[n][n - right + 1][n - left + 1]，因为n - right + 1就是left自己

3、其他一般情况：

首先检测left与终点n / 2的大小。若left > n / 2，那么说明left在中间点的右侧，同时也意味着right也在中间点的右侧。为了方便计算，在这里先将left和right变为n - right + 1以及n - left + 1再进行后面的计算。

此时可能有三种情况：

3-1）left和right都在中间点的左侧：

此时在left左侧有1到left - 1个人，枚举其中进入下一轮的人数i。

同样的，在left到right之间的一共有right - left - 1个人，枚举其中进入下一轮的人数j。

那么对于i和j的每一种组合，就有

left进入下一轮后左侧还有i个人，因此left在下一轮中的位置next_left是i +1

right进入下一轮后左侧有i + 1（表示left的位置）+ j个人，因此right在下一轮中的位置next_right是i + j + 2

于是就有f[n][left][right] \= min(f[n][left][right], f[(n + 1) / 2][next_left][next_right] + 1)

对于g也是同样的，g[n][left][right] \= max(g[n][left][right], g[(n +1) / 2][next_left][next_right] + 1)

3-2）left在中间点的左侧，right就是中间点：

此时与3-1)完全一样，直接按同样方式处理即可

3-3）left在中间点的左侧，right在中间点的右侧：

这种情况稍微复杂一点，需要考虑到right的对手在left的哪一侧。不过根据最上面的结论，可以通过对称变换强行让right的对手处于left的右侧。具体来说，就是right的对手为mirror_right \= n - right +1，若其在left的左侧，那么就有

mirror_right \< left，即n - right + 1 \< left，移项后就有left + right > n + 1

当出现这种情况时，可以利用f[n][left][right] \= f[n][n - right + 1][n - left + 1]来调换left和right。也就是说新的left'位于原来mirror_right的位置，而新的right'的对手的位置恰好是老的left的位置，从而就有

left' \= mirro_right \< left \= mirror_right'

即保证了当前right'对手的位置在left'位置的右侧。

接下来以right的对手位于left的右侧进行讨论。

此时在left左侧有1到left - 1个人，枚举其中进入下一轮的人数i。

在left到mirror_right之间有mirror_right - left个人，枚举其中进入下一轮的人数j。

接下来mirror_right这个人一定被right淘汰掉，不用考虑。

再往后是mirror_right到right之间，一共有n - mirror_right \* 2个人，无论如何这些人会被淘汰掉一半，剩下的人数就是mid_rest \= (n - mirror_right \* 2 + 1) / 2

接下来就是right

那么对于i和j的每一种组合，就有

left进入下一轮后左侧还有i个人，因此left在下一轮中的位置next_left是i +1

right进入下一轮后左侧有i + 1（表示left的位置）+ j + 0（表示mirror right）+ (n - mirror_right \* 2 + 1) / 2个人，因此right在下一轮中的位置next_right是i + j + mid_rest + 2

接下来与3-1)中一样，还是根据next_left以及next_right对于f和g进行递归求解

无论此时是3-1)、3-2）、3-3）中的那种情况，在计算完f[n][left][right]以及g[n][left][right]之后，不要忘了把结果原样赋值给f[n][n - right + 1][n - left + 1]以及g[n][n - right + 1][n - left +1]

最后附上python代码：

```python
class Solution(object):
    def earliestAndLatest(self, n, firstPlayer, secondPlayer):
        """
        :type n: int
        :type firstPlayer: int
        :type secondPlayer: int
        :rtype: List[int]
        """

        f = [[[None] * (n + 1) for _ in range(n + 1)] for _ in range(n + 1)]
        g = [[[None] * (n + 1) for _ in range(n + 1)] for _ in range(n + 1)]

        self.dfs(n, firstPlayer, secondPlayer, f, g)
        return [f[n][firstPlayer][secondPlayer], g[n][firstPlayer][secondPlayer]]
    
    def dfs(self, n, left, right, f, g):
        if f[n][left][right] is not None:
            return
        if f[n][n - right + 1][n - left + 1] is not None:
            return
        if left + right == n + 1:
            f[n][left][right] = g[n][left][right] = 1
            f[n][right][left] = g[n][right][left] = 1
            return

        next_n = (n + 1) / 2

        if left > n / 2:
            left, right = n - right + 1, n - left + 1

        if right <= next_n:
            for i in range(left):
                for j in range(right - left):
                    next_left = i + 1
                    next_right = i + j + 2
                    self.dfs(next_n, next_left, next_right, f, g)
                    if f[n][left][right] is None or f[n][left][right] > f[next_n][next_left][next_right] + 1:
                        f[n][left][right] = f[next_n][next_left][next_right] + 1
                    if g[n][left][right] is None or g[n][left][right] < g[next_n][next_left][next_right] + 1:
                        g[n][left][right] = g[next_n][next_left][next_right] + 1
        
        else:
            if left + right > n + 1:
                left, right = n - right + 1, n - left + 1
            
            mirror_right = n - right + 1
            mid_rest = (n - mirror_right * 2 + 1) / 2

            for i in range(left):
                for j in range(mirror_right - left):
                    next_left = i + 1
                    next_right = i + j + 1 + mid_rest + 1
                    self.dfs(next_n, next_left, next_right, f, g)
                    if f[n][left][right] is None or f[n][left][right] > f[next_n][next_left][next_right] + 1:
                        f[n][left][right] = f[next_n][next_left][next_right] + 1
                    if g[n][left][right] is None or g[n][left][right] < g[next_n][next_left][next_right] + 1:
                        g[n][left][right] = g[next_n][next_left][next_right] + 1
        
        f[n][n - right + 1][n - left + 1] = f[n][left][right]
        g[n][n - right + 1][n - left + 1] = g[n][left][right]
```
