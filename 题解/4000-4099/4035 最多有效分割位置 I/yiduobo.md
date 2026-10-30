---
title: "4035. 最多有效分割位置I & 4037. 最多有效分割位置II"
aliases: ["yiduobo的每日leetcode 4035.最多有效分割位置I && 4037.最多有效分割位置II", "4035. 最多有效分割位置I", "4037. 最多有效分割位置II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/hard", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2078285953400042946"
zhihu_id: "2078285953400042946"
zhihu_title: "yiduobo的每日leetcode 4035.最多有效分割位置I && 4037.最多有效分割位置II"
question_id: ["4035", "4037"]
question: ["最多有效分割位置 I", "最多有效分割位置 II"]
problem_url: ["https://leetcode.cn/problems/maximum-valid-split-positions-i/", "https://leetcode.cn/problems/maximum-valid-split-positions-ii/"]
difficulty: ["Medium", "Hard"]
rating: 2372
created: "2026-09-02T01:47:56+08:00"
updated: "2026-09-02T01:48:00+08:00"
upvotes: 0
comments: 0
---

# 4035. 最多有效分割位置I & 4037. 最多有效分割位置II

> **[yiduobo的每日leetcode 4035.最多有效分割位置I && 4037.最多有效分割位置II](https://zhuanlan.zhihu.com/p/2078285953400042946) · 知乎 · 2026-09-02 · 赞同 0**
> 力扣：[4035. 最多有效分割位置 I](https://leetcode.cn/problems/maximum-valid-split-positions-i/) · Medium · 灵茶山艾府：[非暴力做法（Python/Java/C++/Go）](灵茶山艾府.md)
> 力扣：[4037. 最多有效分割位置 II](https://leetcode.cn/problems/maximum-valid-split-positions-ii/) · Hard · 灵茶山艾府：[证明：至多有一个位置需要考虑删除（Python/Java/C++/Go）](../4037%20最多有效分割位置%20II/灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4035.最多有效分割位置I

<https://leetcode.cn/problems/maximum-valid-split-positions-i/description/>

4037.最多有效分割位置II

<https://leetcode.cn/problems/maximum-valid-split-positions-ii/description/>

题目给出一个整数数组nums，其中元素大小不超过10^9。

现在可以从nums中移除至多一个元素(也可以不移除)，然后令arr为按照原始顺序保留其余元素后得到的数组，记其长度为m。

接下来，若对于某个处于0到m - 2之间的位置index，满足arr[0]到arr[index]这一段中所有元素的最大公约数，恰好等于arr[index + 1]到arr[m - 1]这一段中所有元素的最大公约数，那么就称index是有效的。

更形式化的描述，就是gcd(arr[:index + 1]) \=\= gcd(arr[index + 1:])，其中0 \<\= index \< m -1。

对于一个arr，其得分为有效的index下标数量。问arr的最大可能得分是多少。

两题的题设相同，第二题的数据规模较大，nums的长度可达10^5。

如果没有删除元素的操作，那么本题就很容易了：正反两趟遍历，计算出每个前缀子数组以及每个后缀子数组的最大公约数。方便起见，记pre[index]为nums[:index + 1]这个前缀子数组的最大公约数，而suf[index]则为nums[index:]这个后缀子数组的最大公约数。接下来，只需枚举所有的分割点index，检测pre[index]是否恰好等于suf[index + 1]即可。

实际上，这里其实都没必要枚举分割点index，理由是若pre[index]等于suf[index + 1]，而整个数组的最大公约数又可以写作gcd(pre[index], suf[index + 1])，那么就说明pre[index]与suf[index + 1]都恰好等于整个数组的最大公约数。基于这一点，就可以使用两个哈希表pre_first以及suf_first，记录前缀与后缀中的每种不同最大公约数首次出现的下标位置(注意suf_first记录的是后缀中首次出现的位置，对于整个数组而言实际上就是最后出现的位置)。这两个哈希表可以在正反遍历计算pre和suf时顺便得到。

接下来，不妨设整个数组的最大公约数为g，那么在这里可以先取出pre_first[g]以及suf_first[g]。这意味着如果要让前缀与后缀的最大公约数相等，那么前缀至少需要包含pre_first[g]，后缀至少需要包含suf_first[g]，而合法的分割点index则可以取pre_first[g]到suf_first[g] - 1之间的任意位置，因此最终答案就是max(0, suf_first[g] - pre_first[g])。需要注意这里是有可能出现pre_first[g]在suf_first[g]右侧的情况，因此需要取0作为答案的下界。

接下来对于需要删除一个元素的情况，就需要分情况进行讨论了。

首先可以明确的是，若当前删掉了nums[index]，剩下数组的最大公约数就是g \= gcd(pre[index - 1], suf[index + 1])，在这里很自然想到沿用上面pre_first与suf_first的处理方法，但是由于nums[index]被删去，因此之前的pre_first和suf_first可能失真，因此需要先进行一些额外的判断：

1、若pre[index - 1]与suf[index + 1]都恰好就等于g：

这种情况是最理想的，因为这两个条件就意味着pre_first[g]与suf_first[g]分别位于index的两侧，因此分割点依然可以取pre_first[g]到suf_first[g] - 1中的任意位置。不过此时已经没有index这个位置了，因此需要使用suf_first[g] - pre_first[g] - 1来更新答案。

2、若pre[index - 1]与suf[index + 1]都不等于g：

此时必然不存在合法的分割点。这里有一个隐藏条件就是gcd是越做越小的，也就是说g \= gcd(pre[index - 1], suf[index + 1])必然小于等于其中的任意一方。对于当前这种情况，则是严格小于任意一方。

基于这一点，若最终的分割点位于index的左侧，那么前缀子数组的最大公约数必然大于等于pre[index - 1]，不肯能等于更小的g。反过来，若分割点位于index的右侧，那么后缀子数组的最大公约数必然大于等于suf[index + 1]，也不可能等于g。因此这种情况可以直接跳过。

3、若pre[index - 1]等于g而suf[index + 1]不等于g：

此时的分割点只有可能处于index的左侧。更具体的，在这里需要想办法找出最大的p，满足当前的arr[p:]的最大公约数恰好等于g，那么分割点就可以处于pre_first[g]到p - 1之间。

对于寻找p的问题，可以利用线段树来解决，具体的计算方法也有两种。

第一种是不执行删除操作，而是改为在pre_first[g] + 1到index - 1之间二分，利用线段树计算当前二分到的mid到index - 1这一段的最大公约数，再与suf[index + 1]取最大公约数，就可以得到从nums[mid:]去除掉nums[index]后的最大公约数。这个公约数会随着mid的增大而增大，随着mid的减小而减小，这也是这里二分成立的理由，而符合条件的最大的mid就是要找的p。

第二种则是真的执行删除操作，利用0来占掉nums[index]的位置，然后自底向上重新计算这logn个节点对应区间的最大公约数。接下来从根节点向下，使用一个变量other记录当前后缀已有的最大公约数。若当前节点的右孩子对应的最大公约数等于g，或者这个最大公约数与other取最大公约数后等于g，那么说明右半区间存在合法的p，此时迭代到当前节点的右孩子。反之，则需要迭代到当前节点的左孩子，同时更新other为other与右孩子的最大公约数，因此右孩子表达的子区间也是当前后缀的一部分。通过此法找到p之后，再将nums[index]修改回原样即可。

不论是哪种做法，在确定了p之后，就可以使用p - pre_first[g]来更新答案了。此时需要特别注意，此时的p可能刚好与index重叠，这种需要将p向前移动一位。

4、若suf[index + 1]等于g而pre[index - 1]不等于g：

此时与情况3对称，分割点只能处于index的右侧。此时则只需通过线段树找出最小的符合条件的p，满足当前的arr[:p + 1]的最大公约数恰好等于g，那么分割点就可以处于p到suf_first[g] - 1之间，可以使用suf_first[g] - p来更新答案了。此时同样需要注意处理p与index重叠的情况，需要将p向后移动一位。

最后附上python代码：

```python
class Solution(object):
    def maxValidSplits(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        def gcd(x, y):
            while y > 0:
                x, y = y, x % y
            return x
        
        def generate(start, end, step, g_list, first):
            g = 0
            for index in range(start, end, step):
                v = nums[index]
                g = gcd(g, v)
                if g not in first:
                    first[g] = index
                g_list.append(g)

        n = len(nums)
        pre = []
        pre_first = {}
        suf = []
        suf_first = {}
        generate(0, n, 1, pre, pre_first)
        generate(n - 1, -1, -1, suf, suf_first)
        suf.reverse()

        m = 1
        while m < n:
            m <<= 1
        
        f = [0] * (m << 1)
        for index, v in enumerate(nums):
            f[m + index] = v
        
        length = m >> 1
        while length >= 1:
            for index in range(length):
                p = length + index
                f[p] = gcd(f[p << 1], f[p << 1 | 1])
            length >>= 1

        res = max(0, suf_first[f[1]] - pre_first[f[1]])
        for index, v in enumerate(nums):
            if index == 0:
                pre_g = 0
            else:
                pre_g = pre[index - 1]
            
            if index == n - 1:
                suf_g = 0
            else:
                suf_g = suf[index + 1]
            
            g = gcd(pre_g, suf_g)

            if g == pre_g and g == suf_g:
                res = max(res, suf_first[g] - pre_first[g] - 1)
                continue
            
            if g != pre_g and g != suf_g:
                continue
            
            p = index + m
            f[p] = 0
            while p > 1:
                f[p >> 1] = gcd(f[p], f[p ^ 1])
                p >>= 1

            if g == pre_g:
                p = 1
                other = 0
                while p < m:
                    if f[p << 1 | 1] == g:
                        p <<= 1
                        p |= 1
                    else:
                        x = gcd(other, f[p << 1 | 1])
                        p <<= 1
                        if x == g:
                            p |= 1
                        else:
                            other = x
                p -= m
                if p == index:
                    p -= 1
                score = p - pre_first[g]

            else:
                p = 1
                other = 0
                while p < m:
                    if f[p << 1] == g:
                        p <<= 1
                    else:
                        x = gcd(other, f[p << 1])
                        p <<= 1
                        if x != g:
                            p |= 1
                            other = x
                p -= m
                if index == p:
                    p += 1
                score = suf_first[g] - p

            res = max(res, score)
            p = index + m
            f[p] = v
            while p > 1:
                f[p >> 1] = gcd(f[p], f[p ^ 1])
                p >>= 1

        return res
```
