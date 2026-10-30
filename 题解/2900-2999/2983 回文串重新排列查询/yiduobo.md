---
title: "2983. 回文串重新排列查询"
aliases: ["yiduobo的每日leetcode 2983.回文串重新排列查询"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/一-前缀和", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/692469389"
zhihu_id: "692469389"
zhihu_title: "yiduobo的每日leetcode 2983.回文串重新排列查询"
question_id: "2983"
question: "回文串重新排列查询"
problem_url: "https://leetcode.cn/problems/palindrome-rearrangement-queries/"
difficulty: "Hard"
rating: 2780
created: "2024-04-15T02:41:26+08:00"
updated: "2024-04-15T02:41:26+08:00"
upvotes: 1
comments: 0
---

# 2983. 回文串重新排列查询

> **[yiduobo的每日leetcode 2983.回文串重新排列查询](https://zhuanlan.zhihu.com/p/692469389) · 知乎 · 2024-04-15 · 赞同 1**
> 力扣：[2983. 回文串重新排列查询](https://leetcode.cn/problems/palindrome-rearrangement-queries/) · Hard · 灵茶山艾府：[分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2983.回文串重新排列查询

[. - 力扣（LeetCode）](https://leetcode.cn/problems/palindrome-rearrangement-queries/description/)

由于题目保证了字符串的长度为偶数，那么就可以将原字符串从中间切开，然后将后半部分翻转过去，问题就变成了给出两个字符串以及若干询问，每个询问给出两个区间，问能否通过调整区间内的字符使得两个字符串相等。需要特别注意的是，对于后半部分的询问需要将询问的区间也倒转过去。

对于可调整的部分，需要两个字符串在特定区间内每种字符出现的次数都一样；对于不可以调整的部分，则要求完全相同。可以发现，两个部分都是区间问题，那么按照一般的处理方法，在这里通通可以转化成前缀问题来解决。在这里需要三个前缀数组char_s，char_t以及same，分别储存两个字符串中每个前缀中每种字符出现的次数，以及两个字符串前缀中具有相同字符的数量。那么对于一个区间[x, y]，可以通过char_s[y][char] - char_s[x - 1][char]来得到s的区间[x, y]中char出现的次数，也可以通过same[y] - same[x - 1]计算s的区间[x, y]在不调整的状态下相等的字符数量，若这个数量等于区间长度y - x + 1，说明s和t在[x, y]这一段是完全相同的。

另外，由于两个字符串是完全等价的，因此在这里可以假设区间[a, b]在区间[c, d]的左侧，即a \<\= c。若不满足，那么将两个字符串交换一下再求解就行了。

接下来对于给出的区间[a, b]，[c, d]，有三种可能得情况：

1、两个区间不想交，即b \< c：

此时字符串将被划分成5个部分，分别是[0, a - 1]，[a, b]，[b + 1, c - 1]，[c, d]，[d + 1, n - 1]。其中第1、3、5个部分是不能调整的，需要通过same判断是否相同。而对于第2、4个部分则是可以调整的，此时只需通过char_s和char_t判断区间内包含的字符出现次数是否完全相同。

2、两个区间相互包含，即d \<\= b：

此时字符串将被划分成3个部分，分别是[0, a - 1]，[a, b]，[b + 1, n - 1]。其中第1、3个部分是不能调整的，需要通过same判断是否相同。第2个部分可以调整，同样是根据char_s和char_t来进行判断。

3、两个区间部分重叠，即a \<\= c \<\= b \< d：

此时字符串将被划分成5个部分，分别是[0, a - 1]，[a, c - 1]，[c, b]，[b + 1, d]，[d + 1, n - 1]。其中第1、5个部分是不能调整的，需要通过same判断是否相同。

需要特别注意，这里的[a, c - 1]以及[b + 1, d]这两个部分与上面两种情况不同，在这里是通过第一个字符串的[a, b]中的字符来适配第二字符串的[a, c - 1]，通过第二个字符串的[c, d]中的字符来适配第一个字符串的[b + 1, d]。如果可以适配，那么剩下的字符需要填充到第三个区间中，此时可以通过判断整个大区间[a, d]中的字符出现次数是否相同，若相同且[a, c - 1]和[b + 1, d]可以适配，那么[c, b]必然也可以适配。

最后附上python代码：

```python
class Solution(object):
    def canMakePalindromeQueries(self, s, queries):
        """
        :type s: str
        :type queries: List[List[int]]
        :rtype: List[bool]
        """

        n = len(s) // 2
        t = s[len(s) : n - 1 : -1]
        s = s[:n]

        char_s = [Counter()]
        char_t = [Counter()]
        same = [0]

        for index in range(n):
            char_s.append(char_s[-1].copy())
            char_s[-1][s[index]] += 1

            char_t.append(char_t[-1].copy())
            char_t[-1][t[index]] += 1

            same.append(same[-1])
            if s[index] == t[index]:
                same[-1] += 1

        def check_same(x, y):
            if x > y:
                return True
            return same[y] == same[x - 1] + y - x + 1
        
        def check_char(x, y):
            for char in char_s[y]:
                if char_s[y][char] - char_s[x - 1][char] != char_t[y][char] - char_t[x - 1][char]:
                    return False
            return True

        def check(s, t, sx, sy, tx, ty, char_s, char_t):
            if sy < tx:
                return check_same(1, sx - 1) and check_char(sx, sy) and \
                        check_same(sy + 1, tx - 1) and check_char(tx, ty) and check_same(ty + 1, n)

            elif ty <= sy:
                return check_same(1, sx - 1) and check_char(sx, sy) and check_same(sy + 1, n)
            
            else:
                if not check_same(1, sx - 1) or not check_same(ty + 1, n):
                    return False

                char_subs = Counter()
                for char in char_s[sy]:
                    char_subs[char] = char_s[sy][char] - char_s[sx - 1][char]

                char_subt = Counter()
                for char in char_t[ty]:
                    char_subt[char] = char_t[ty][char] - char_t[tx - 1][char]

                for char in char_t[tx - 1]:
                    cnt = char_t[tx - 1][char] - char_t[sx - 1][char]
                    if cnt > char_subs[char]:
                        return False
                    char_subs[char] -= cnt

                for char in char_s[ty]:
                    cnt = char_s[ty][char] - char_s[sy][char]
                    if cnt > char_subt[char]:
                        return False
                    char_subt[char] -= cnt
                
                for char in char_s[ty]:
                    if char_s[ty][char] - char_s[sx - 1][char] != char_t[ty][char] - char_t[sx - 1][char]:
                        return False

                return True

        res = []
        for sx, sy, tx, ty in queries:
            sx += 1
            sy += 1
            tx, ty = n + n - ty, n + n - tx

            if sx > tx:
                res.append(check(t, s, tx, ty, sx, sy, char_t, char_s))
            else:
                res.append(check(s, t, sx, sy, tx, ty, char_s, char_t))

        return res
```
