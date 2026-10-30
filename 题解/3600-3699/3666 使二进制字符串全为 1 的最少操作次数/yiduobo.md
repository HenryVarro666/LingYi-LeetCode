---
title: "3666. 使二进制字符串全为1的最少操作次数"
aliases: ["yiduobo的每日leetcode 3666.使二进制字符串全为1的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/breadth-first-search", "leetcode/math", "leetcode/ordered-set", "leetcode/shortest-path", "题单/常用数据结构", "题单/图论算法", "题单/数学算法", "题单/常用数据结构/七-并查集", "题单/图论算法/九-其他", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1950319913530000455"
zhihu_id: "1950319913530000455"
zhihu_title: "yiduobo的每日leetcode 3666.使二进制字符串全为1的最少操作次数"
question_id: "3666"
question: "使二进制字符串全为 1 的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-equalize-binary-string/"
difficulty: "Hard"
rating: 2477
created: "2025-09-18T02:16:37+08:00"
updated: "2025-09-18T02:16:39+08:00"
upvotes: 0
comments: 0
---

# 3666. 使二进制字符串全为1的最少操作次数

> **[yiduobo的每日leetcode 3666.使二进制字符串全为1的最少操作次数](https://zhuanlan.zhihu.com/p/1950319913530000455) · 知乎 · 2025-09-18 · 赞同 0**
> 力扣：[3666. 使二进制字符串全为 1 的最少操作次数](https://leetcode.cn/problems/minimum-operations-to-equalize-binary-string/) · Hard · 灵茶山艾府：[两种方法：BFS / 数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3666.使二进制字符串全为1的最少操作次数

[3666. 使二进制字符串全为 1 的最少操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-equalize-binary-string/description/)

题目给出一个二进制字符串s以及一个整数k。在一次操作中，可以从s中选择恰好k个不同的下标并将这些下标对应的值进行翻转。问使得s中所有字符都变为1的最少操作次数，若不可能，则返回-1。

本题与之前的2612题非常类似，可以直接照搬2612的思路，但是具体代码实现上略有差别。

[yiduobo的每日leetcode 2612.最少翻转操作数](https://zhuanlan.zhihu.com/p/645685369)

在本题中，若当前有now个0，考虑一次翻转后0的数量：

若翻转了0个0，k个1，那么0的数量将变为now + k

若翻转了1个0，k - 1个1，那么0的数量将变为now + k - 2

...

若翻转了k个0，0个1，那么0的数量将变为now - k

也就是说，在理想情况下，now可以扩展到步长为2的区间[now - k, now + k]。然而需要注意的是，可能存在1的数量不够或者0的数量不够的问题，使得扩展无法进行。更具体的，若now小于k，那么反正k个0显然是不行的，最多也就是反正now个0，因此此时0的下界应该从now - k调整为k - now，因此可以用max(now - k, k - now)来表示now扩展的下界。同理，扩展的上界则为min(now + k, n - k + n - now)，其中n - now为初始情况下1的数量，若这个数小于k，那么将其全部变为0之后，还有k - (n - now)个位置将从0变为1，因此0的数量就是n - (k - (n - now))，也就是n - k + n - now。

基于这一点，一个直观的思路就是从扩展出来的这些位置再次扩展，通过类似bfs的方式计算扩展到每种zero所需的最少步数。很明显，这样做的时间复杂度很高，因为每次都需要遍历当前扩展出去的区间，并从中选出之前从没扩展到的位置。

注意到每次的扩展得到的都是一个步长为2的连续区间，因此随着扩展的进行，必然是中间的部分先得到扩展，然后逐渐向两侧进行扩展。因此在这里可以记录下之前向两侧最远扩展到过哪里，然后对于一个新扩展出的区间，只需要将区间下界到之前最远扩展到的下界，以及最远扩展到的上界，到区间上界这两段区间中没有处理过的位置加入到bfs队列中就行了。

需要特别注意的是，k为偶数时，从zero扩展出去的区间边界与zero是同奇偶的，但是当k为奇数时，从zero扩展出去的区间边界与zero是不同奇偶的，因此在这里需要分奇偶记录两组最远扩展到的区间边界，然后通过异或k模2的结果来选取上一轮的边界是什么。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        n = len(s)        
        zero = 0
        for c in s:
            if c == '0':
                zero += 1

        step = 0
        q = [zero]
        head, tail = 0, 1
        pre_left = [None, None]
        pre_right = [None, None]
        r = zero % 2
        t = k % 2
        pre_left[r] = zero
        pre_right[r] = zero
        vis = set()
        vis.add(zero)
        while head < tail and 0 not in vis:
            step += 1
            min_left = max_right = None
            for now in q[head : tail]:
                now_left = max(now - k, k - now)
                now_right = min(now + k, (n - k) + n - now)
                if min_left is None or min_left > now_left:
                    min_left = now_left
                if max_right is None or max_right < now_right:
                    max_right = now_right

            new_left = new_right = None
            if pre_left[t ^ r] is None:
                for zero in range(min_left, max_right + 1, 2):
                    if zero not in vis:
                        vis.add(zero)
                        q.append(zero)
                        if new_left is None:
                            new_left = zero
                        new_right = zero
            else:
                for zero in range(min_left, max_right + 1, 2):
                    if zero >= pre_left[t ^ r]:
                        break
                    if zero not in vis:
                        vis.add(zero)
                        q.append(zero)
                        if new_left is None:
                            new_left = zero
                
                for zero in range(max_right, min_left - 1, -2):
                    if zero <= pre_right[t ^ r]:
                        break
                    if zero not in vis:
                        vis.add(zero)
                        q.append(zero)
                        if new_right is None:
                            new_right = zero
                
            pre_left[t ^ r] = new_left
            pre_right[t ^ r] = new_right

            r ^= t
            head, tail = tail, len(q)

        if 0 in vis:
            return step
        return -1
```
