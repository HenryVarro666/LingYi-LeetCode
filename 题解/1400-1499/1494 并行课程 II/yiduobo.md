---
title: "1494. 并行课程II"
aliases: ["yiduobo的每日leetcode 1494.并行课程II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/416792464"
zhihu_id: "416792464"
zhihu_title: "yiduobo的每日leetcode 1494.并行课程II"
question_id: "1494"
question: "并行课程 II"
problem_url: "https://leetcode.cn/problems/parallel-courses-ii/"
difficulty: "Hard"
created: "2021-10-05T22:08:41+08:00"
updated: "2021-10-05T22:08:41+08:00"
upvotes: 2
comments: 1
---

# 1494. 并行课程II

> **[yiduobo的每日leetcode 1494.并行课程II](https://zhuanlan.zhihu.com/p/416792464) · 知乎 · 2021-10-05 · 赞同 2**
> 力扣：[1494. 并行课程 II](https://leetcode.cn/problems/parallel-courses-ii/) · Hard · 灵茶山艾府：[子集状压 DP：从记忆化搜索到递推（附题单！）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1494.并行课程II

[力扣](https://leetcode-cn.com/problems/parallel-courses-ii/)

相当有难度的题目。

首先很自然想到的是拓扑排序，按往常的情况来说，肯定是选择拓扑序最深的课程开始，但是在这里有一个隐含条件是k并行度，例如有很多门课程都有两门同样的前置课程，且此时的并行度k \= 2，那么若不能一次性学习完这两门前置课程，就相当于这些课程都将会往后延一个学期。换言之，这里需要考量的除了传统拓扑问题中的深度，还多出了一个并行度。如何权衡二者得到一个贪心的方案，我试了若干种全都有反例存在。

当然，后来我还特意去查了一些资料，发现这个问题确实是没有贪心解的。

另外，就是注意到题目这里的课程数目只有15门，那么也可以使用状态压缩动态规划去做。即令f[state]表示学习state表示的这些课程所需的最少时间。

对于f[state]而言，首先需要找出剩余课程中当前可以学习的课程。

这里剩余课程的定义自然是对于课程index，其二进制编码1 \<\< index没有在state中出现，即state & (1 \<\< index) \= 0。另一方面，所谓的可以学习的课程则要求index的所有前置课程全部在state中出现，那么可以先对于所有课程进行预处理，得到其前置课程的二进制编码prev[index]，然后判断其是否在state中出现，也就是state & prev[index] \= prev[index]。

对于满足这两点的课程，将这些课程收集起来得到一个数组candidate。

接下来，需要从candidate中选出k个课程。这里的所有方案数都需要枚举出来，并将这些方案保存在集合choose中。

最后，枚举choose中的所有方案，即从state学习了choose中的某种方案，来到了next_state，此时就有

f[next_state] \= min(f[next_state], f[state] + 1)

动态规划完成后，f[max_state]即为最终答案。

需要注意的是，由于这里的课程选择受拓扑序的影响，因此不能传统的从0到max_state来枚举状态。我在这里采用的是类bfs的做法，首先从状态0开始选择本学期的课程，对于得到的所有next_state，若其没有被访问过，那么将其加入到队列末尾。

这种做法的时间复杂度看上去应该是O(2^n \* 2^n)。第一个2^n表示状态总数，第二个2^n则表示方案选择数目的上限。不过实际上可以发现，在每次选择方案时，candidate的大小并不一定是k。更确切的说，当前已经选择了m门课程的状态数一共有C(n, m)种，而这些状态所需的方案数则为2^m，于是最终方案数的选择上复杂度位

O(C(n, 0) \* 2^0 + C(n, 1) \* 2^1 + ... + C(n, n) \* 2^n)

符合二项式定理的形式，也就是说实际上时间复杂度为O(3^n)

除此之外，这种一次选择k门课程的做法可能并不是最优的。按常规理解，一般是一门一门课程进行选择的。如果每次新添加一门课程，那么应该将状态写成f[i][j][state]表示前i门课程，当前学期选择了j们课程，且所有课程编码后为state时所需的最少时间，然后对于当前是否选择第i们课程进行讨论。这样一来理论上的时间复杂度应该是O(2^n \* nk)，相比与上面的应该要好很多。

不过这样的做法有一个问题就是，若当前第i门课程的前置课程p已经被选择了，即p是f[i][j][state]里面j中的一门课程，那么这个学期是不能再选择i这门课程的，不过就这个做法而言似乎无法很好的规避这个问题。当然，可能也可以利用拓扑序来做做文章，不过我这里没有继续深入探讨了。

最后附上python代码：

```python
class Solution(object):
    def minNumberOfSemesters(self, n, relations, k):
        """
        :type n: int
        :type relations: List[List[int]]
        :type k: int
        :rtype: int
        """

        max_state = (1 << n) - 1
        prev_state = [0] * n
        for x, y in relations:
            x -= 1
            y -= 1
            prev_state[y] |= 1 << x
        
        f = [None] * (max_state + 1)
        f[0] = 0
        q = [0]
        l = 0
        r = 1
        while l < r:
            now_state = q[l]
            l += 1

            candidate = []
            for index in range(n):
                if (now_state & (1 << index) == 0) and (now_state & prev_state[index] == prev_state[index]):
                    candidate.append(1 << index)
            
            choose = set([0])
            for index in range(k):
                tmp = set()
                for x in choose:
                    for y in candidate:
                        if x & y == 0:
                            tmp.add(x | y)
                
                if len(tmp) == 0:
                    break

                choose = tmp
            
            for choose_state in choose:
                next_state = now_state | choose_state
                if f[next_state] is None or f[next_state] > f[now_state] + 1:
                    f[next_state] = f[now_state] + 1
                    if next_state not in q:
                        q.append(next_state)
                        r += 1

        return f[-1]
```
