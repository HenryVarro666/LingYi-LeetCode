---
title: "3234. 统计1显著的字符串的数量"
aliases: ["yiduobo的每日leetcode 3234.统计1显著的字符串的数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/enumeration", "题单/常用数据结构", "题单/常用数据结构/十一-根号算法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/720468821"
zhihu_id: "720468821"
zhihu_title: "yiduobo的每日leetcode 3234.统计1显著的字符串的数量"
question_id: "3234"
question: "统计 1 显著的字符串的数量"
problem_url: "https://leetcode.cn/problems/count-the-number-of-substrings-with-dominant-ones/"
difficulty: "Medium"
rating: 2557
created: "2024-09-16T22:36:46+08:00"
updated: "2024-09-16T22:36:46+08:00"
upvotes: 0
comments: 0
---

# 3234. 统计1显著的字符串的数量

> **[yiduobo的每日leetcode 3234.统计1显著的字符串的数量](https://zhuanlan.zhihu.com/p/720468821) · 知乎 · 2024-09-16 · 赞同 0**
> 力扣：[3234. 统计 1 显著的字符串的数量](https://leetcode.cn/problems/count-the-number-of-substrings-with-dominant-ones/) · Medium · 灵茶山艾府：[枚举子串中的 0 的个数（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3234.统计1显著的字符串的数量

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-the-number-of-substrings-with-dominant-ones/)

给出一个由0和1组成的字符串s，要求统计其中1显著子串的数量。1显著子串指的是某个子串中1的数量大于等于0的数量的平方。

首先考虑特殊情况。当子串全为1，也就是没有0时，该子串一定是显著的，而一个长度为k的全1子串一共可以提供(k + 1) \* k / 2个显著子串。对于这种情况只需一趟遍历，一边记录每个子串中每个0的下标，一边计算相邻的0之间1的数量并更新答案。

接下来对于字符串中包含0的情况，由于1的数量必然要大于等于0的数量的平方，因此0的数量是根号级的，规模是很小的。也就是说，在这里可以枚举0的数量zero，然后一趟遍历，利用滑动窗口找出以每个下标为起点且恰好包含zero个0的子串，判断有多少个显著子串。

更具体的，不妨设以下标index开头的子串中第zero个0的下标为p，那么其最边界最多可以延伸到p右侧最近的0的左侧。令next_zero[index]表示index右侧最近的0的下标，那么在这里就是next[p] - 1，即以index为左边界，以p到next[p] - 1任意下标为右边界的子串都恰好包含zero个0。对于next数组的计算，则可以在处理特殊情况的时候反向遍历来得到。

另一方面，由于显著子串中1的数量必须大于0的数量的平方，因此对于一个包含zero个0的子串，其必须包含至少zero \* zero个1，也就是说这个子串的长度至少是min_length \= zero + zero \* zero，因此对于以index为左边界的子串，其右边界必须要大于等于index + min_length - 1。

综合以上两点，可以发现以index为左边界的子串，其合法右边界的取值范围在max(p, index + min_length - 1)到next[p] - 1之间，而这个区间的长度就是以index为左边界的显著子串的长度。

在处理完index后，若s[index]为0，那么p必须向右移动到next[p]保证子串中0的数量为zero，反之则无需移动。

最后附上python代码：

```python
class Solution(object):
    def numberOfSubstrings(self, s):
        """
        :type s: str
        :rtype: int
        """

        n = len(s)
        
        next_zero = []
        p = n
        tot_zero = 0
        res = 0
        for index in range(n - 1, -1, -1):
            next_zero.append(p)
            if s[index] == '0':
                res += (p - index) * (p - index - 1) // 2
                tot_zero += 1
                p = index
        next_zero.reverse()

        res += p * (p + 1) // 2

        zero = 1
        for zero in range(1, tot_zero + 1):
            min_length = zero * zero + zero
            if min_length > n:
                break

            p = 0
            zero_cnt = 0

            if s[0] == '0':
                zero_cnt = 1

            while p < n and zero_cnt < zero:
                p = next_zero[p]
                zero_cnt += 1

            for index in range(n):
                rightest = next_zero[p] - 1
                leftest = max(p, index + min_length - 1)
                res += max(0, rightest - leftest + 1)

                if s[index] == '0':
                    p = next_zero[p]
                    if p == n:
                        break

        return res
```
