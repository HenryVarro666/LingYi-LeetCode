---
title: "1654. 到家的最少跳跃次数"
aliases: ["yiduobo的每日leetcode 1654.到家的最少跳跃次数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/441027030"
zhihu_id: "441027030"
zhihu_title: "yiduobo的每日leetcode 1654.到家的最少跳跃次数"
question_id: "1654"
question: "到家的最少跳跃次数"
problem_url: "https://leetcode.cn/problems/minimum-jumps-to-reach-home/"
created: "2021-12-04T00:37:10+08:00"
updated: "2021-12-04T00:37:10+08:00"
upvotes: 2
comments: 0
---

# 1654. 到家的最少跳跃次数

> **[yiduobo的每日leetcode 1654.到家的最少跳跃次数](https://zhuanlan.zhihu.com/p/441027030) · 知乎 · 2021-12-04 · 赞同 2**
> 力扣：[1654. 到家的最少跳跃次数](https://leetcode.cn/problems/minimum-jumps-to-reach-home/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1654.到家的最少跳跃次数

[力扣](https://leetcode-cn.com/problems/minimum-jumps-to-reach-home/)

首先考虑边界情况。当x \= 0时，直接返回0就行了。

接下考虑x > 0的情况。可以明确的一点是，由于是从0开始起跳，那么第一跳只能选择向右跳。又因为不能连续向左跳，那么向右跳的次数必然大于等于向左跳的次数，于是可以将每一次向左跳与一次向右跳组合起来，就可以得到式子

x \= p \* a - q \* (b - a)

其中p >\= 0且q >\= 0

对于这个式子，如果题目中没有forbidden的存在，那么直接使用扩展欧几里得算法求解，但是有了forbidden之后可能会打乱部署，那么只能退而求其次，老老实实用bfs进行求解。对于bfs的左边界已经规定好了不能走到负数位置，而右边界则需要确认。

在这里继续分a>\=b和a\<b两种情况进行讨论。

1、当a>\=b时，考察上面的式子可以发现一定是越跳就越往右走的，因此若当前位置now大于某个right_boundary时，就再也不可能跳到x上来了。很明显，x + b就是一个right_boundary。若now > x + b，即使此时向左跳，最多也只能跳到now - b这个位置上，而now - b是大于x的。而之后再想向左跳，就必须先执行一次向右跳，两次跳跃累计起来反而是继续向右跳了一段，只会离x更远了。

因此对于a >\= b的情况，bfs的右边界right_boundary可以设定为x + b。

2、当a \< b时，由于此时是可以通过a和b的组合形成无数次向左跳的，因此可能会出现先执行多次向右跳操作来到一个较大的位置，然后再逐渐通过a和b的组合跳回到x的情况。对于这种情况而言，如果真的一次性执行很多次向右跳的操作，其右边界必然会十分巨大。一个自然的想法就是在向右跳的期间穿插一些a和b的组合跳跃，从而控制这个右边界的大小。而进行这些穿插的前提则是对于当前位置，必须保证向左跳或向右跳的目的地不是forbidden的格子。

与情况1类似，在这里就只需要保证执行这些操作的位置大于等于max(forbidden) + b + 1，那么即使执行了向左跳，其也不可能跳到forbidden的格子上，向右跳自然就更不可能跳到forbidden的格子上。

为了保证向左跳时当前位置大于等于max(forbidden) + b + 1，那么在当前位置小于这个值时需要执行一些向右跳的操作，极限情况下就是当前处于max(forbidden) + b，还需要执行一次向右跳操作之后来到了max(forbidden) + b + a。

因此对于a \< b的情况，bfs的右边界right_boudary可以设定为max(forbidden) + a + b。

确定了right_boundary之后就可以开始执行bfs了。值得一提的是，在bfs过程中往往需要对已经访问过的位置去重，但是在这里如果是通过向左跳访问过的位置是不需要进入到去重位置集合的。因为对于某个位置now而言，若其是通过向左跳访问到的，那么此时就不能再执行向左跳了，而在后续的操作中可能会通过向右跳再次来到now，而此时的now是可以再向左跳的。另一方面，如果对向右跳的位置做了去重，那么就不可能出现通过向左跳访问到重复的格子，因为在执行向左跳之前必须要先执行一次向右跳，而这个向右跳到达的位置已经做过去重处理了。

最后附上python代码。我在这里的写法不是很规整，简单来说就是设d[0] \= a表示向右跳，而d[1] \= -b表示向左跳。对于当前位置now，根据上一步的方向枚举当前可用的d。若执行的是d[0]，那么下一步可用的就是d[0]和d[1]，也就是d[range(2)]；若执行的是d[1]，那么下一步可用的只有d[0]，也就是d[range(1)]。综合起来就是若这一步执行的是d[index]，那么下一步可选的执行选项就是d[range(2 - index)]：

```python
class Solution(object):
    def minimumJumps(self, forbidden, a, b, x):
        """
        :type forbidden: List[int]
        :type a: int
        :type b: int
        :type x: int
        :rtype: int
        """

        if x == 0:
            return 0

        forbidden_pos = set(forbidden)

        if a >= b:
            right_boundary = x + b
        else:
            right_boundary = max(forbidden) + a + b
        
        q = [[0, 2]]
        d = [a, -b]
        l = 0
        r = 1
        used = set([0])
        step = 0
        while l < r:
            step += 1
            for now_pos, last_direct in q[l : r]:
                for index, delta in enumerate(d[:last_direct]):
                    next_pos = now_pos + delta
                    if next_pos == x:
                        return step
                    if next_pos >= 0 and next_pos <= right_boundary and next_pos not in forbidden_pos and (delta < 0 or next_pos not in used):
                        if index == 0:
                            used.add(next_pos)
                        q.append([next_pos, 2 - index])
            
            l, r = r, len(q)

        return -1
```
