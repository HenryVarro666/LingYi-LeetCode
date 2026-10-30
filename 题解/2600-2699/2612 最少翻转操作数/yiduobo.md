---
title: "2612. 最少翻转操作数"
aliases: ["yiduobo的每日leetcode 2612.最少翻转操作数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/union-find", "leetcode/graph", "leetcode/ordered-set", "leetcode/shortest-path", "题单/常用数据结构", "题单/图论算法", "题单/常用数据结构/七-并查集", "题单/图论算法/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/645685369"
zhihu_id: "645685369"
zhihu_title: "yiduobo的每日leetcode 2612.最少翻转操作数"
question_id: "2612"
question: "最少翻转操作数"
problem_url: "https://leetcode.cn/problems/minimum-reverse-operations/"
difficulty: "Hard"
rating: 2824
created: "2023-07-25T04:37:09+08:00"
updated: "2023-07-25T04:37:09+08:00"
upvotes: 0
comments: 0
---

# 2612. 最少翻转操作数

> **[yiduobo的每日leetcode 2612.最少翻转操作数](https://zhuanlan.zhihu.com/p/645685369) · 知乎 · 2023-07-25 · 赞同 0**
> 力扣：[2612. 最少翻转操作数](https://leetcode.cn/problems/minimum-reverse-operations/) · Hard · 灵茶山艾府：[两种做法：BFS+有序集合/并查集（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2612.最少翻转操作数

[力扣](https://leetcode.cn/problems/minimum-reverse-operations/)

手动模拟一下题目中的翻转操作可以发现，如果不考虑被ban掉的位置，每次翻转可以到达的位置都将是一个由相同奇偶性的下标组成的连续子序列。

对于下标now，翻转长度为k，那么其向左翻转的最远处就应该是now - k + 1。在这里有一种可能是now不够大，因此这个now - k + 1也不成立。也就是说在now - k + 1小于0时，now翻转前可以认为是从0向后数now位，那么翻转后就应该是从k - 1向前数now位，因此在这种情况下翻转后的最左侧下标就是k - now - 1。对于右侧也可以如法炮制，得到翻转后的最右侧下标为(now + k - 1, (n + k) + (n + 1) - now)。

得到下班后，一个自然的想法就是从p开始进行bfs，每一轮都将可扩展序列中所有未扩展过的位置加入到队列中，从而计算出扩展到所有位置需要的步数。不过需要注意的是，由于每个位置最多可以扩展出2k规模的序列，那么如果不进行优化，本题的时间复杂度就可以达到O(nk)，在给出的数据规模下显然是不行的，需要进行优化。

可以发现，对于一个位置A，不妨设其向左和向右最远扩展到L和R，那么下一轮从L和R也可以扩展回到A，也就是说如果综合之前轮次的扩展考虑的话，可以认为每一轮的扩展，而不仅仅是单个位置的扩展，最终都会得到一个由相同奇偶性的下标组成的连续子序列。另一方面，对于之前轮次扩展到的位置是没有必要再次扩展的，因此可以记录之前轮次扩展到的最左侧位置以及最右侧位置，在本轮扩展时就只需要扩展上一轮最左侧位置更左边以及上一轮最右侧位置更右边的下标了。

不过在这里需要注意的是，当翻转长度k为奇数时，得到的目标位置序列的奇偶性与起点位置相同，而但当k为偶数时，得到的目标位置序列的奇偶性则与起点位置相反，关于这一点，可以利用一个变量r来表示当前这一轮起点位置下标的奇偶性，然后对于每一轮扩展操作，则可以事先计算出t \= k % 2，然后利用1^t^r来计算r的变化。这样做的理由是当k为奇数时，t等于1，此时的1^t^r不会改变r的奇偶性；反过来，当k为偶数时，t为0，那么1^t^r就会翻转r。

由于需要分奇偶，那么在这里可以使用两个长度为2的数组pre_left和pre_right分别记录之前奇偶轮次扩展到的最左侧位置以及最右侧位置。对于奇偶性为r的扩展，扩展出来的位置的奇偶性为1^t^r。

更具体的，每一轮都遍历当前队列中的所有下标，计算可以翻转得到的最左侧和最右侧的下标，然后先从左向右进行同奇偶性的遍历，直到遍历的位置越过了上一轮的左边界pre_left为止，遍历期间将所有没有被ban的位置加入到下一轮的队列中。同样的，还需要从右向左进行同奇偶性的遍历，直到遍历的位置越过了上一轮的右边界pre_right为止，遍历起见同样需要将所有没有被ban的位置加入到下一轮的队列中。

遍历完成后，需要更新pre_left和pre_right，那么在这里就需要在之前遍历时记录下新扩展的位置中最左侧和最右侧的没有被ban掉的位置，使用这两个位置作为新的pre_left和pre_right。需要注意的是，r这一轮使用和更新的pre_left和pre_right都应该是1^t^r这一轮的。

对于时间复杂度方面，每个下标只会被加入到bfs队列一次，同时由于pre_left和pre_right的存在，在扩展时每个位置也不会被重复遍历到，因此最终的时间复杂度就是O(n)。

bfs完成后，还有些位置可能是翻转不到的，那么对于这些位置就需要将对应的答案置为-1。

最后附上python代码：

```python
class Solution(object):
    def minReverseOperations(self, n, p, banned, k):
        """
        :type n: int
        :type p: int
        :type banned: List[int]
        :type k: int
        :rtype: List[int]
        """

        res = [None] * n
        res[p] = 0
        for b in banned:
            res[b] = -1
        
        ban_set = set(banned)

        step = 0
        q = [p]
        head, tail = 0, 1
        pre_left = [None, None]
        pre_right = [None, None]
        r = p % 2
        t = k % 2
        pre_left[r] = p
        pre_right[r] = p
        while head < tail:
            step += 1
            min_left = max_right = None
            for now in q[head : tail]:
                now_left = max(now - k + 1, k - now - 1)
                now_right = min(now + k - 1, (n - k) + (n - 1) - now)
                if min_left is None or min_left > now_left:
                    min_left = now_left
                if max_right is None or max_right < now_right:
                    max_right = now_right

            new_left = new_right = None
            if pre_left[1 ^ t ^ r] is None:
                for i in range(min_left, max_right + 1, 2):
                    if res[i] is None:
                        res[i] = step
                        q.append(i)
                        if new_left is None:
                            new_left = i
                        new_right = i
            else:
                for i in range(min_left, max_right + 1, 2):
                    if i >= pre_left[1 ^ t ^ r]:
                        break
                    if res[i] is None:
                        res[i] = step
                        q.append(i)
                        if new_left is None:
                            new_left = i
                
                for i in range(max_right, min_left - 1, -2):
                    if i <= pre_right[1 ^ t ^ r]:
                        break
                    if res[i] is None:
                        res[i] = step
                        q.append(i)
                        if new_right is None:
                            new_right = i
                
            pre_left[1 ^ t ^ r] = new_left
            pre_right[1 ^ t ^ r] = new_right

            r ^= (1 ^ t)
            head, tail = tail, len(q)
        
        for i in range(n):
            if res[i] is None:
                res[i] = -1
            
        return res
```
