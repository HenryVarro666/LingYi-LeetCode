---
title: "3213. 最小代价构造字符串"
aliases: ["yiduobo的每日leetcode 3213.最小代价构造字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/ordered-set", "leetcode/sorting", "leetcode/string-matching", "leetcode/suffix-array", "leetcode/hash-function", "题单/动态规划", "题单/字符串", "题单/动态规划/十一-优化-DP", "题单/字符串/四-字符串哈希", "题单/字符串/七-AC-自动机", "题单/字符串/八-后缀数组/后缀自动机"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/708371163"
zhihu_id: "708371163"
zhihu_title: "yiduobo的每日leetcode 3213.最小代价构造字符串"
question_id: "3213"
question: "最小代价构造字符串"
problem_url: "https://leetcode.cn/problems/construct-string-with-minimum-cost/"
difficulty: "Hard"
rating: 2171
created: "2024-07-12T03:51:33+08:00"
updated: "2024-07-12T03:51:33+08:00"
upvotes: 1
comments: 0
---

# 3213. 最小代价构造字符串

> **[yiduobo的每日leetcode 3213.最小代价构造字符串](https://zhuanlan.zhihu.com/p/708371163) · 知乎 · 2024-07-12 · 赞同 1**
> 力扣：[3213. 最小代价构造字符串](https://leetcode.cn/problems/construct-string-with-minimum-cost/) · Hard · 灵茶山艾府：[三种方法：字符串哈希（单模+双模）/ 后缀数组 / AC 自动机（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3213.最小代价构造字符串

[. - 力扣（LeetCode）](https://leetcode.cn/problems/construct-string-with-minimum-cost/description/)

题目给出一个字符串target以及一个字符串数组words和代价数组costs，现在需要从words中选出若干单词拼接起来形成target，每个单词words[i]可以使用多次，使用的代价为costs[i]。问得到target的最小代价是多少。如果无法得到target，则返回-1。

非常标准的字符串分割问题，可以用动态规划求解。令f[index]表示得到target中的前index个字符需要的最小代价，那么初始状态下有f[0] \= 0，表示得到空字符串的代价为0，而对于index > 0的f[index]，则有

f[index] \= min(f[index], f[index - length(words[p])] + costs[p]

其中length(words[p])表示words[p]的长度，且需要满足target[index - length(words[p]) : index]这个子串与words[p]一致。

由于题目中target的长度n可达50000以及单词的数量以及总长度也都可达50000，即使不考虑字符串匹配的复杂度，上面算法的复杂度依然是O(n^2)的，需要进行优化。

对于这类一对多的字符串匹配问题，使用trie图是比较好的选择。trie图可以简单理解成kmp算法的多字符串版本，是在trie树中通过建立匹配失败时的跳转边得到的，但是我很久没写了半天写不对，只好退而求其次。就像rk算法之于kmp一样，使用分组rk的方法也可以得到与trie图类似的效果。

关于rk算法的细节可以参考之前的2156题

[yiduobo：yiduobo的每日leetcode 2156.查找给定哈希值的子串](https://zhuanlan.zhihu.com/p/531523744)

对于本题，则可以将words中的单词先按长度进行分组，那么对于同一个组内的单词，不妨设这些单词的长度为length，此时就只需要考察target中的所有长度为length的子串是否能与这些单词匹配，使用rk算法分别计算这些单词的哈希值以及target中所有长度为length的子串的哈希值，就可以得到target中有哪些子串可以匹配哪些单词。即使所有单词的长度都各不相同，不同length的数量也不会超过sqrt(sum(length))。另外字符串匹配在这里变成了哈希值匹配，通过哈希表就是O(1)的，因此最终的时间复杂度就优化到了O(n \* sqrt(sum(length)))，对于本题完全够用了。

另外如果使用上面的算法，常数方面会比较吃紧。由于本题需要计算多次哈希值，因此在rk算法的具体实现上使用前缀哈希值之差相比直接计算窗口内的哈希值会更好一点，可以省去不同长度窗口移动时重复的乘法操作。具体的差别通过对比本题的代码以及2156题的代码就一目了然了。

最后附上python代码：

```python
class Solution(object):
    def minimumCost(self, target, words, costs):
        """
        :type target: str
        :type words: List[str]
        :type costs: List[int]
        :rtype: int
        """

        rank = [index for index in range(len(words))]
        rank.sort(key=lambda d:len(words[d]))
        n = len(target)

        hit = [[] for _ in range(n)]
        p = 0
        mod = 10 ** 9 + 7
        base = 26
        asc_a = ord('a')
        cost_dict = {}
        while p < len(rank):
            q = p
            while q < len(rank) and len(words[rank[p]]) == len(words[rank[q]]):
                q += 1

            length = len(words[rank[p]])
            if length > len(target):
                break

            r = 1
            for index in range(length):
                r = r * base % mod
            cost_dict[length] = [r, {}]
                
            for index in range(p, q):
                w = words[rank[index]]
                v = 0
                for c in w:
                    v = (v * base + ord(c) - asc_a) % mod
                
                if v not in cost_dict[length][1]:
                    cost_dict[length][1][v] = costs[rank[index]]
                else:
                    cost_dict[length][1][v] = min(cost_dict[length][1][v], costs[rank[index]])

            p = q

        f = [0]
        p = [1]
        v = [0]
        for index, c in enumerate(target):
            f.append(-1)
            p.append(p[-1] * base % mod)
            v.append((v[-1] * base + ord(c) - asc_a) % mod)

            for length in cost_dict:
                if index + 1 < length:
                    continue
                else:
                    r, cost_info = cost_dict[length]
                    key = (v[-1] - v[-length - 1] * p[length] % mod + mod) % mod
                    if key in cost_info and f[-length - 1] != -1 and (f[-1] == -1 or f[-1] > f[-length - 1] + cost_info[key]):
                        f[-1] = f[-length - 1] + cost_info[key]

        return f[-1]
```
