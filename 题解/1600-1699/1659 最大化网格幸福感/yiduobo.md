---
title: "1659. 最大化网格幸福感"
aliases: ["yiduobo的每日leetcode 1659.最大化网格幸福感"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/442044187"
zhihu_id: "442044187"
zhihu_title: "yiduobo的每日leetcode 1659.最大化网格幸福感"
question_id: "1659"
question: "最大化网格幸福感"
problem_url: "https://leetcode.cn/problems/maximize-grid-happiness/"
created: "2021-12-07T00:45:04+08:00"
updated: "2021-12-07T00:45:04+08:00"
upvotes: 0
comments: 0
---

# 1659. 最大化网格幸福感

> **[yiduobo的每日leetcode 1659.最大化网格幸福感](https://zhuanlan.zhihu.com/p/442044187) · 知乎 · 2021-12-07 · 赞同 0**
> 力扣：[1659. 最大化网格幸福感](https://leetcode.cn/problems/maximize-grid-happiness/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1659.最大化网格幸福感

[力扣](https://leetcode-cn.com/problems/maximize-grid-happiness/)

看到题目之后可以先确认有没有贪心的解法。看上去尽量让内向的人与世隔绝，让外向的人抱团取暖肯定是正确的，但是问题是现在要将这些人安排在二维的网格当中，这样一来格子与格子之间的临接关系就复杂起来了。简单想了一下应该是不存在可用的贪心策略。

注意到题目中各个数值的规模都很小，那么另一个思路就是尝试使用状态压缩动态规划来解决。按往常的动态规划思路，对于这类问题通常有两种状态表示。一种是f[i][j][state]表示从[0, 0]开始到[i, j]这些格子为state时是什么样的，另一种则是f[i][j][k][l][state]表示以(i, j)为左上角，(k, l)为右下角且这个矩阵中格子为state时是什么样的。

对于第一种状态表示的方法而言，转移时需要考察[i, j]这个格子如何使用。在本题中是比较好处理的，因为对于[i, j]而言：

1、当i大于0时需要考察[i - 1, j]

2、当j大于0时需要考察[i, j - 1]

也就是每次状态转移时仅需要考察之前的两个格子

对于第二种状态表示的方法而言，转移时则需要需要一条分割线。但在本题中并不好处理，因为枚举分割线的同时还需要枚举分割线两侧格子的所有情况组合，处理起来是非常困难的。

那么很明显，在这里就应该选择第一种状态表示。当然，考虑到本题中处理位置之外还有内向人数和外向人数这两个值的存在，因此需要更复杂的状态表示：f[i][j][k][l][state]表示从[0, 0]到[i, j]这些格子中居住了k个内向的人以及l个外向的人，且具体居住的情况为state时的最大幸福感。这里state的构成是从上到下从左至右的每个格子表示3进制数中从高到低的每一位，其中0表示没有住人，1表示住了内向的人，2表示住了外向的人。

不过这个状态表示是不行的。由于这里的网格最多可达5 \* 5，且每个格子有3种状态表示，即无人居住，内向的人居住以及外向的人居住，那么这里state的规模可以达到3^25，显然无法储存。

回到上面的状态转移，对于[i, j]这个格子而言，实际上可能用到的格子只有[i - 1, j]以及[i, j - 1]，那么在这里完全可以让state滚动起来，即state并不需要储存所有格子的状态，而是只需要储存从[i - 1, j]到[i, j - 1]这些格子的状态就好了。这样一来state的规模里面就缩减到了3^n，上限最多就是3^5了。

那么此时的状态表示就改成了f[i][j][k][l][state]表示从[0, 0]到[i, j]这些格子中居住了k个内向的人以及l个外向的人，且从[i - 1, j]到[i, j - 1]这些格子居住情况为state时的最大幸福感。

确定了状态表示之后，接下来就要处理状态转移了。初始化所有状态值为0。

1、首先考察边界情况。当i和j都等于0时，此时可以在格子[0, 0]上安排一个人居住。

如果不安排人居住的话，那么就是f[0][0][0][0][0] \= 0。当然由于初始化的状态值就是0，也可以直接忽略这种情况。

当introvertsCount大于0时，可以在这个格子上安排一个内向的人，此时就有f[0][0][1][0][1] \= 120。

当extrovertsCount大于0时，可以在这个格子上安排一个外线过的人，此时就有f[0][0][0][1][2] \= 40。

2、接下来考察一般情况。

首先可以明确的是对于[i, j]这个格子上的所有状态而言，必然是从[last_i, last_j]这个格子的某个状态转移而来的。这里的[last_i, last_j]表示前一个格子。一般来说[i, j]的前一个格子是[i, j - 1]，而当j \= 0时，[i, j]的前一个格子则应该是上一行的最后一个格子，也就是[i - 1, n - 1]。

确定了[last_i, last_j]之后，接下需要枚举k和l的各种组合，对于当前的k和l，首先需要考察k + l是否大于i \* n + j + 1。若大于，那么即使让每个格子都住人，也不够这k + l个人住。由于初始化的状态值已经是0，因此可以忽略掉这种情况。

接下来考察可以安排这些人住的情况。此时需要再枚举上一轮所有可能的state。

对于枚举到的state来说，可能用到的值是表示当前格子上面那个格子的最高位，以及表示当前格子左边那个格子的最低位。这两个位上的值可以分别用state除以3^(n - 1)以及state模3得到，分别记为upper_state以及left_state。

除此之外state还需要滚动起来，即需要移除最高位，将后面的位向左移动，然后根据当前格子的状态填充新来的最低位。这些操作综合起来就是先让state对3^(n - 1)取模，然后将取模的结果乘以3，再将当前位置上的状态添加到最低位。由于目前还不知道当前位置上的装填，那么可以先完成前面两步的计算，得到新的base_state，然后在确定当前格子的状态之后再将这个状态直接累加到base_state上就好了。

对于当前格子而言，又可以分成三种情况讨论：

2-1）当前格子不安排人住。那么此时新的state需要在老state的基础上去掉最高位上的值，然后乘以3，再在最后一位上填充上0。具体操作起来就是state先对3^(n - 1)取模，然后将取模后的结果乘以3。将这个值即为base_state，那么就有

f[i][j][k][l][base_state] \= max(f[i][j][k][l][base_state], f[last_i][last_j][k][l][state])

2-2）尝试安排一个内向的人住在[i, j]这个位置，因此上一轮的状态就是f[last_i][last_j][k - 1][l][state]，那么就必须要满足k > 0，且f[last_i][last_j][k - 1][j][state]非负。

接下来需要考察安排内向的人住在[i, j]这个位置的影响。这个影响分成两个部分，分别是安排在[i, j]这个位置上的内向的人自己的幸福感，以及可能受到这个位置住人影响的[i - 1, j]以及[i, j - 1]这两个位置上人的幸福感。

对于当前位置上的人而言，其基础幸福感是120，记为tmp。

若i > 0且upper_state大于0，说明上面的格子住了人，因此这里tmp需要减去30。若upper_state等于1，说明上面住的也是内向的人，那么受当前格子的影响tmp还要再减去30；若upper_state等于2，说明上面住的是外向的人，那么受当前格子的影响幸福感tmp需要加上20。

若j > 0且left_state大于0，说明左边的格子住了人，因此这里tmp需要减去30。与上面的情况类似，若left_state等于1，tmp还需要再减去30；若left_state等于2，tmp则需要加上20。

得到最终的tmp之后，总的幸福感就是f[last_i][last_j][k - 1][l][state] + tmp。由于此时在[i, j]这个格子上安排了内向的人，因此state的最低位应该填充1，那么此时新的state就是base_state + 1。综合起来就有

f[i][j][k][l][base_state + 1] \= max(f[i][j][k][l][base_state + 1], f[last_i][last_j][k - 1][l][state] + tmp)

2-3）尝试安排一个外向的人住在[i, j]这个位置。与情况2-2类似，此时考察的上一轮状态为f[last_i][last_j][k][l - 1][state]，因此需要满足l > 0，且f[last_i][last_j][k][l - 1][state]非负。

接下来需要考察安排外向的人住在[i, j]这个位置的影响，同样是分成两个部分，处理方法也类似，只有tmp以及state的计算有些许差异。

对于tmp而言，其初始值应该是40。

若i > 0且upper_state大于0，说明上面的格子住了人，因此这里tmp需要加上20。若upper_state等于1，说明上面住的是内向的人，那么受当前格子的影响tmp再减去30；若upper_state等于2，说明上面住的也是外向的人，那么受当前格子的影响幸福感tmp需要加上20。

若j > 0且left_state大于0，说明左边的格子住了人，因此这里tmp需要加上30。与上面的情况类似，若left_state等于1，tmp需要再减去30；若left_state等于2，tmp则需要加上20。

可以发现，实际上当一个state确定之后，在[i, j]这个位置安排一个人来住的话对[i - 1, j]以及[i, j - 1]这两个位置上的人的影响，以及[i, j]自身的幸福感变化完全是可以通过分析所有state以及i和j是否大于0的情况全部预处理出来的。不过在这里状态转移的复杂度本身就是O(1)的，那么这个预处理只能让代码更简洁，但不会对时间复杂度产生影响，因此我在这里就没有做这个预处理了。

得到tmp之后，此时新的state应该是在base_state的基础上加上2，综合起来就有

f[i][j][k][l][base_state + 2] \= max(f[i][j][k][l][base_state + 2], f[last_i][last_j][k][l - 1][state] + tmp)

至此转移方程就已经的出来了。执行完动态规划后，枚举所有格子的每种住户情况以及所有的状态，取其中的最大值作为答案返回即可。

这一题应该是我做这个题解系列一来写的最长的一次了。。

最后附上python代码：

```python
class Solution(object):
    def getMaxGridHappiness(self, m, n, introvertsCount, extrovertsCount):
        """
        :type m: int
        :type n: int
        :type introvertsCount: int
        :type extrovertsCount: int
        :rtype: int
        """

        max_state = 3 ** n
        upper_divisor = max_state / 3
        f = [[[[[-1] * max_state for _ in range(extrovertsCount + 1)] for _ in range(introvertsCount + 1)] for _ in range(n + 1)] for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                if i == 0 and j == 0:
                    f[i][j][0][0][0] = 0
                    if introvertsCount > 0:
                        f[i][j][1][0][1] = 120
                    if extrovertsCount > 0:
                        f[i][j][0][1][2] = 40
                else:
                    if j == 0:
                        last_i, last_j = i - 1, n - 1
                    else:
                        last_i, last_j = i, j - 1

                    for intro in range(introvertsCount + 1):
                        if intro > i * n + j + 1:
                            break
                        for extro in range(extrovertsCount + 1):
                            if intro + extro > i * n + j + 1:
                                break

                            for state in range(max_state):
                                upper_state = state / upper_divisor
                                left_state = state % 3
                                base_state = (state % upper_divisor) * 3
                                f[i][j][intro][extro][base_state] = max(f[i][j][intro][extro][base_state], f[last_i][last_j][intro][extro][state])
                                if intro >= 1 and f[last_i][last_j][intro - 1][extro][state] >= 0:
                                    tmp = 120
                                    if i > 0 and upper_state > 0:
                                        tmp -= 30
                                        if upper_state == 1:
                                            tmp -= 30
                                        else:
                                            tmp += 20

                                    if j > 0 and left_state > 0:
                                        tmp -= 30
                                        if left_state == 1:
                                            tmp -= 30
                                        else:
                                            tmp += 20

                                    f[i][j][intro][extro][base_state + 1] = max(f[i][j][intro][extro][base_state + 1], f[last_i][last_j][intro - 1][extro][state] + tmp)
                                
                                if extro >= 1 and f[last_i][last_j][intro][extro - 1][state] >= 0:
                                    tmp = 40
                                    if i > 0 and upper_state > 0:
                                        tmp += 20
                                        if upper_state == 1:
                                            tmp -= 30
                                        else:
                                            tmp += 20

                                    if j > 0 and left_state > 0:
                                        tmp += 20
                                        if left_state == 1:
                                            tmp -= 30
                                        else:
                                            tmp += 20

                                    f[i][j][intro][extro][base_state + 2] = max(f[i][j][intro][extro][base_state + 2], f[last_i][last_j][intro][extro - 1][state] + tmp)
        
        res = 0
        for i in range(m):
            for j in range(n):
                for intro in range(introvertsCount + 1):
                    for extro in range(extrovertsCount + 1):
                        for state in range(max_state):
                            res = max(res, f[i][j][intro][extro][state])

        return res
```
