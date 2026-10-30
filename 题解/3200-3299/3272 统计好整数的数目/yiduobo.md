---
title: "3272. 统计好整数的数目"
aliases: ["yiduobo的每日leetcode 3272.统计好整数的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/math", "leetcode/combinatorics", "leetcode/enumeration", "leetcode/sorting", "题单/数学算法", "题单/数学算法/二-组合数学", "题单/数学算法/七-杂项"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/784233462"
zhihu_id: "784233462"
zhihu_title: "yiduobo的每日leetcode 3272.统计好整数的数目"
question_id: "3272"
question: "统计好整数的数目"
problem_url: "https://leetcode.cn/problems/find-the-count-of-good-integers/"
difficulty: "Hard"
rating: 2382
created: "2024-10-01T01:46:11+08:00"
updated: "2024-10-01T01:46:11+08:00"
upvotes: 1
comments: 0
---

# 3272. 统计好整数的数目

> **[yiduobo的每日leetcode 3272.统计好整数的数目](https://zhuanlan.zhihu.com/p/784233462) · 知乎 · 2024-10-01 · 赞同 1**
> 力扣：[3272. 统计好整数的数目](https://leetcode.cn/problems/find-the-count-of-good-integers/) · Hard · 灵茶山艾府：[枚举所有回文数+组合数学（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3272.统计好整数的数目

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-count-of-good-integers/description/)

题目给出两个正整数n和k。如果一个整数x既是回文数，又是k的倍数，那么就称x为一个k回文整数。若某个整数y的数位在重新排列后可以变为一个k回文整数，那么就称y是一个好整数。注意这里y不能有前导0，同时y在重新排列后也不能有前导0。

现在要求计算n位好整数的数目，这里的n不超过10。

题目要求计算n位好整数的数目，而好整数是某个k回文整数数位重组后的结果，那么在这里不妨反过来，先找出n位的k回文整数，然后计算这些k回文整数在打乱数位后可以形成多少个不同的整数。

由于n的规模较小，且k回文整数具有回文的性质，那么在这里就可以直接暴力枚举这些回文整数的前半部分，然后翻转后拼接得到整个回文整数，再判断这个回文整数是否为k的倍数，如果是，去重后再计算在打乱数位后可以形成多少个不同的整数即可。

具体来说，对于一个长度为n的k回文整数，其前半部分的长度为n // 2，当n为奇数时还需要额外带上正中间这一位，也就是说需要枚举所有的m \= (n + 1) // 2位数。由于不允许出现前导0，因此枚举的范围就是10^(m - 1)到10^m，对于本题在10^5这个量级，是完全没有问题的。

接下来根据n的奇偶完成回文整数的拼接，不妨记为v，那么接下来需要先判断v是否为k的倍数，如果是，还需要先对v进行去重。例如515515和551155，都是5回文整数，而在计算515515打乱数位后可以形成的整数后就不应该再计算551155打乱数位后可以形成的整数了。

我在这里采用的去重手法是将v按照各数位的大小从小到大进行排序，然后利用排序后得到的这个最小的数来作为v的哈希值来去重。

去重完成后，最后还需要计算v在打乱数位后可以形成多少个不同的整数。

这里的v是一个n位数，那么最高位就有n种可行的选择，次高位有n - 1种，以此类推，因此在不考虑重复的情况下可以形成n!个整数。不过注意到题目要求整数不能包含前导0，因此最高位实际可用的选择就是n - cnt[0]种，其中cnt[0]表示v各个数位中0出现的次数，而次高位以及更低的位置上不受影响，因此一共是(n - cnt[0]) \* (n - 1)!个整数。

这些整数中可能有重复的整数出现，重复的原因是某些数位上的数相同，在计算时产生了重复的计算。例如v中出现了cnt[x]个x，那么在固定了这些x所在的数位后，通过互相之间的交换这些cnt[x]个x将被计算cnt[x]!次，因此在这里就应该将最终答案除以cnt[x]!。

根据上面的结论，就只需要先使用哈希表cnt统计v中每种数字出现的次数，然后初始化答案为(n - cnt[0]) \* (n - 1)!，然后再遍历cnt，用答案除以cnt中每个数字出现次数的阶乘即可。

最后附上python代码：

```python
class Solution(object):
    def countGoodIntegers(self, n, k):
        """
        :type n: int
        :type k: int
        :rtype: int
        """

        m = (n + 1) // 2
        start = 10 ** (m - 1)
        end = 10 ** m
        vis = set()
        fact = [1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
        res = 0
        for left in range(start, end):

            digits = list(str(left))
            right_digits = digits[::-1]
            if n % 2 == 0:
                digits.extend(right_digits)
            else:
                digits.extend(right_digits[1:])
            
            v = int(''.join(digits))

            if v % k == 0:
                h = int(''.join(sorted(digits, reverse=True)))
                if h in vis:
                    continue
                vis.add(h)

                
                cnt = {}
                for char in digits:
                    cnt[char] = cnt.get(char, 0) + 1

                if '0' in cnt:
                    x = fact[n - 1] * (n - cnt['0'])
                else:
                    x = fact[n]

                for c in cnt.values():
                    x //= fact[c]
                
                res += x
    
        return res
```
