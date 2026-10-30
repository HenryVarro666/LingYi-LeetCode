---
title: "3714. 最长的平衡子串II"
aliases: ["yiduobo的每日leetcode 3714.最长的平衡子串II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "leetcode/prefix-sum", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1961929251902166618"
zhihu_id: "1961929251902166618"
zhihu_title: "yiduobo的每日leetcode 3714.最长的平衡子串II"
question_id: "3714"
question: "最长的平衡子串 II"
problem_url: "https://leetcode.cn/problems/longest-balanced-substring-ii/"
difficulty: "Medium"
rating: 2202
created: "2025-10-15T23:13:59+08:00"
updated: "2025-10-15T23:14:03+08:00"
upvotes: 2
comments: 0
---

# 3714. 最长的平衡子串II

> **[yiduobo的每日leetcode 3714.最长的平衡子串II](https://zhuanlan.zhihu.com/p/1961929251902166618) · 知乎 · 2025-10-15 · 赞同 2**
> 力扣：[3714. 最长的平衡子串 II](https://leetcode.cn/problems/longest-balanced-substring-ii/) · Medium · 灵茶山艾府：[式子变形 + 枚举右维护左（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3714.最长的平衡子串II

[3714. 最长的平衡子串 II - 力扣（LeetCode）](https://leetcode.cn/problems/longest-balanced-substring-ii/description/)

题目给出一个仅包含'a'、'b'、'c'的字符串s，s的长度可达10^5。

对于一个子串，若子串中所有不同子串出现的次数都相同，那么就称其为平衡子串。

要求找出s中最长平衡子串的长度。

本题的题设与上一题类似，不过本题的数据规模较大，无法再使用之前的暴力法。由于s仅由三种字符组成，因此可以想其他的办法来进行处理。

可以明确的是，最终答案必然属于以下三种情况之一：

1、仅由一种字符组成

2、由两种不同的字符组成

3、由全部三种字符组成

对于第一种情况，只需一趟遍历，分离出由相同字符组成的子段，然后取其中最长的子段长度更新答案即可。

对于第二种情况，则可以分别计算由('a', 'b')、('a', 'c')、('b', 'c')组成的最长平衡子串长度。不妨设当前处理的是c1和c2，那么在这里就可以将所有的c1都视为-1、所有的c2都视为1，问题就转化成了找出s中的一个字段，其中仅包含-1和1，且子段之和恰好为0。

对于子段和相关的问题，则可以转化为前缀和之差来解决，那么问题就变成了对于每个下标index，设当前的前缀和为s，那么就需要找到最靠前的，且满足对应前缀和也为s的下标p，然后从p + 1到index这一段的子段和就必然为0。也就是说，在这里只需一趟遍历，使用一个哈希表记录每种前缀和出现的最早下标即可。需要特别注意的是，由于子串中只能出现c1和c2，那么当出现除c1和c2之外的另一个字符时，之前的部分就不能再使用了，此时应该重置前缀和哈希表以及前缀和。

最后对于第三种情况，则可以继续沿用上面前缀和的思路，在这里由于有三种字符，就不能再使用之前-1和1的转化方式。事实上，以上-1和1的转化实际上就是对应了两种字符数量之差，因此在这里可以采用更直接的方式，改为使用(cnt_a - cnt_b, cnt_a - cnt_c)的二元组作为哈希表的key，其中cnt_a、cnt_b、cnt_c分别表示当前前缀中'a'、'b'、'c'出现的次数。这样一来，同样只需要一趟遍历，对于当前遍历到的位置，先更新当前字符对应的cnt，然后计算当前位置对应的key，最后从检测哈希表中是否存在这个key。若存在，则更新答案，否则更新哈希表即可。

最后附上python代码：

```python
class Solution(object):
    def longestBalanced(self, s):
        """
        :type s: str
        :rtype: int
        """
        
        res = 0
        p = 0
        while p < len(s):
            q = p
            while q < len(s) and s[p] == s[q]:
                q += 1
            
            res = max(res, q - p)
            p = q
        

        def check_pair(c1, c2):
            f = {0: -1}
            cnt1, cnt2 = 0, 0
            res = 0
            for index, c in enumerate(s):
                if c != c1 and c != c2:
                    f = {0: index}
                    cnt1, cnt2 = 0, 0
                else:
                    if c == c1:
                        cnt1 += 1
                    else:
                        cnt2 += 1
                
                    if cnt1 - cnt2 in f:
                        res = max(res, index - f[cnt1 - cnt2])
                    else:
                        f[cnt1 - cnt2] = index
            return res
        
        res = max(res, check_pair('a', 'b'), check_pair('a', 'c'), check_pair('b', 'c'))

        f = {(0, 0): -1}
        cnt_a, cnt_b, cnt_c = 0, 0, 0
        for index, c in enumerate(s):
            if c == 'a':
                cnt_a += 1
            elif c == 'b':
                cnt_b += 1
            else:
                cnt_c += 1
            
            key = (cnt_a - cnt_b, cnt_a - cnt_c)
            if key in f:
                res = max(res, index - f[key])
            else:
                f[key] = index
        
        return res
```
