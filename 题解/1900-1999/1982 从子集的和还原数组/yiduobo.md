---
title: "1982. 从子集的和还原数组"
aliases: ["yiduobo的每日leetcode 1982.从子集的和还原数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/498177966"
zhihu_id: "498177966"
zhihu_title: "yiduobo的每日leetcode 1982.从子集的和还原数组"
question_id: "1982"
question: "从子集的和还原数组"
problem_url: "https://leetcode.cn/problems/find-array-given-subset-sums/"
created: "2022-04-14T03:46:34+08:00"
updated: "2022-04-14T03:46:34+08:00"
upvotes: 0
comments: 0
---

# 1982. 从子集的和还原数组

> **[yiduobo的每日leetcode 1982.从子集的和还原数组](https://zhuanlan.zhihu.com/p/498177966) · 知乎 · 2022-04-14 · 赞同 0**
> 力扣：[1982. 从子集的和还原数组](https://leetcode.cn/problems/find-array-given-subset-sums/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

1982.从子集的和还原数组

[力扣](https://leetcode-cn.com/problems/find-array-given-subset-sums/)

很有意思的题目，花了一番功夫才想出来。

题目中有用的信息是比较少的，一眼望去只有一个结论，就是数组中必然有0，因为空集就是0。但是仅凭这个是没有任何操作空间的，必须另想办法。

一个很自然的想法就是从最值入手。不妨先考虑最小值。

1、若min(sums) \=\= 0，说明数组中的数全都是非负数，此时只需要找出sums中的次小值，将其减去sums中的最小值，就可以得到数组中的最小元素x了。得到这个最小元素x后，就可以将sums排序，然后sums两两进行分组，每一组都满足其中的较小值加上x恰好等于较大值。此时就可以确定，所有的较大值都是受x影响的，而较小值则不受x影响，因此只需要将所有的较小值收集起来，然后递归求解即可。

2、若min(sums) \< 0，不妨设数组中有m个负数，分别为neg[0], neg[1], ..., neg[m - 1]，那么就有

min(sums) \= neg[0] + neg[1] + ... + neg[m - 1]

此时同样是考虑找出sums中的次小值，记为second_min(sums)，那么此时有两种可能：

2-1）second_min(sums) \= min(sums)，说明此时数组中必然有0，那么此时sums的构成必然是某一种分布原样复制了一份，因此只需要将相同的sums二取其一，然后递归求解即可。

2-2）second_min(sums) > min(sums)，此时的second_min(sums)是在min(sums)的基础上加入了一个正数，或者是min(sums)中去掉了一个负数得到的，即

min(sums) \= neg[0] + neg[1] + ... + neg[m - 1]

那么

second_min(sums) \= neg[0] + neg[1] + ... + neg[m - 1] + pos[p]，表示加入了一个整数pos[p]

second_min(sums) \= neg[0] + neg[1] + ... + neg[q - 1] + neg[q + 1] + ... + neg[m - 1]，表示减去了一个负数neg[q]

此时需要分辨出是哪种情况。做法也可以参照上面的思路，令x \= min(sums) - second_min(sums)，将sums按照差为x进行两两分组。由于此时不知道x的正负，因此无法判断哪一组是受x影响的。此时就用上了最上面的结论，即不受x影响的那一组中必然有0。

那么如果其中只有一组有0，说明该组不受x的影响。若这一组是较小的组，那么说明x是正数，需要将-x加入到答案中，否则说明x是负数，需要将x加入到答案中。接下来则只需要递归求解有0的这一组即可。

另一种情况是两组中都有0，此时就稍微复杂一些。不过可以证明，此时任意求解一组都是可行的。

如果这里任选的恰好选对了，那么无事发生，继续递归求解即可。

如果选错了，那么当前选中的这一组中每一个sums都是在另一组的基础上加上了x。又由于当前选中的组中存在0，那么就有

y[0] + y[1] + ... + y[m] + x \= 0

当然，此时可能还有一些数与x无关，将这些数记为z。

对于当前选中的组中的sums而言，其中所有的sums就可以拆分成三个部分，分别y的组合，z的组合，以及x，即

s \= y\[i\[0\]\] + y\[i\[1\]\] + ... + y\[i\[l_y\]\] + z\[j\[0\]\] + z\[j\[1\]\] + ... + z\[j\[l_z\]\] + x

又由于

y[0] + y[1] + ... + y[m] + x \= 0

那么上下相减，就有

s - 0 \= (y\[i\[0\]\] + y\[i\[1\]\] + ... + y\[i\[l_y\]\] + z\[j\[0\]\] + z\[j\[1\]\] + ... + z\[j\[l_z\]\] + x) - (y\[0\] + y\[1\] + ... + y\[m\] + x)

化简后有

s \= (z\[j\[0\]\] + z\[j\[1\]\] + ... + z\[j\[l_z\]\]) - (y\[k\[0\]\] + y\[k\[1\]\] + ... + y\[k\[l_z\]\])

其中k恰好就是(0, 1, ..., m) - (j[0], j[1], ..., j[l_y])

也就是说，此时只需要将y中的数全部取反，就一定可以构造出所有的sums。虽然当前部分选错了，但是依然存在可行的构造方案，于是继续递归求解即可。

最后附上python代码：

```python
class Solution(object):
    def recoverArray(self, n, sums):
        """
        :type n: int
        :type sums: List[int]
        :rtype: List[int]
        """

        l = 1 << n
        now = sorted(sums)
        res = []

        for _ in range(n):
            x = now[0] - now[1]
            used = set()
            p = 0
            part1 = []
            part2 = []
            for index in range(l):
                if index in used:
                    continue
                
                part1.append(now[index])
                used.add(index)
                while p in used or now[p] != now[index] - x:
                    p += 1
                part2.append(now[p])
                used.add(p)
            
            if 0 in part1:
                res.append(-x)
                now = part1[:]
            else:
                res.append(x)
                now = part2[:]

            l /= 2
        
        return res
```
