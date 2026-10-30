---
title: "3991. 使用前缀反转对数组进行排序"
aliases: ["yiduobo的每日leetcode 3991.使用前缀反转对数组进行排序"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2062283607058731540"
zhihu_id: "2062283607058731540"
zhihu_title: "yiduobo的每日leetcode 3991.使用前缀反转对数组进行排序"
question_id: "3991"
question: "使用前缀反转对数组进行排序"
problem_url: "https://leetcode.cn/problems/sort-array-using-prefix-reversals/"
created: "2026-07-19T21:19:53+08:00"
updated: "2026-07-19T21:19:54+08:00"
upvotes: 0
comments: 0
---

# 3991. 使用前缀反转对数组进行排序

> **[yiduobo的每日leetcode 3991.使用前缀反转对数组进行排序](https://zhuanlan.zhihu.com/p/2062283607058731540) · 知乎 · 2026-07-19 · 赞同 0**
> 力扣：[3991. 使用前缀反转对数组进行排序](https://leetcode.cn/problems/sort-array-using-prefix-reversals/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3991.使用前缀反转对数组进行排序

<https://leetcode.cn/problems/sort-array-using-prefix-reversals/description/>

题目给出一个长度为n的整数数组nums，其中nums是0到n - 1的一个排列，这里的n不超过8。

另外给出一个整数数组pre，其中每个pre[index]都是一个合法的前缀长度，pre中的元素互不相同。

在一次操作中，可以从pre中选择任意一个长度x，并将nums的前x个元素翻转。

问将nums变为升序排列所需的最少操作次数。若无法完成排序，则返回-1。

由于n的长度不超过8，也就意味着总的排列数不会超过8! \= 40320种，因此在这里可以先通过康拓展开将nums转化为其在所有排列中的序，然后基于这个顺序执行bfs。

bfs的每一轮都将当前这一轮的所有序先转化回数组，接下来遍历pre，尝试其中的每种翻转操作，并将翻转后的数组再次转化为序。若当前得到的序没有出现过，则将其加入bfs数组。重复此过程直到出现了第0个序，也就是0到n - 1的升序排列，或者无法继续bfs为止。

最后附上python代码：

```python
class Solution(object):
    def sortArray(self, nums, pre):
        """
        :type nums: List[int]
        :type pre: List[int]
        :rtype: int
        """
        
        n = len(nums)
        fac = [1]
        for v in range(1, n + 1):
            fac.append(fac[-1] * v)

        def cantor(nums):
            used = set()
            st = 0
            for index, v in enumerate(nums):
                cnt = v
                for x in range(v):
                    if x in used:
                        cnt -= 1
                st += cnt * fac[n - index - 1]
                used.add(v)
            return st

        def rev_cantor(st):
            f = []
            used = set()
            for index in range(n):
                v = st // fac[n - index - 1]
                st %= fac[n - index - 1]
                cnt = 0
                for x in range(n):
                    if x in used:
                        continue
                    if v == cnt:
                        f.append(x)
                        used.add(x)
                        break
                    else:
                        cnt += 1

            return f

        st = cantor(nums)
        if st == 0:
            return 0
        vis = set([st])
        print st
        q = [st]
        head, tail = 0, 1
        res = 0
        while head < tail:
            res += 1
            for st in q[head : tail]:
                now = rev_cantor(st)
                for p in pre:
                    left, right = 0, p - 1
                    while left < right:
                        now[left], now[right] = now[right], now[left]
                        left += 1
                        right -= 1
                    
                    nxt_st = cantor(now)
                    if nxt_st == 0:
                        return res
                    if nxt_st not in vis:
                        vis.add(nxt_st)
                        q.append(nxt_st)

                    left, right = 0, p - 1
                    while left < right:
                        now[left], now[right] = now[right], now[left]
                        left += 1
                        right -= 1
            
            head, tail = tail, len(q)
        
        return -1
```
