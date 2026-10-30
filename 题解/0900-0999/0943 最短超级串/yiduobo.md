---
title: "943. 最短超级串"
aliases: ["yiduobo的每日leetcode 943.最短超级串"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/358641242"
zhihu_id: "358641242"
zhihu_title: "yiduobo的每日leetcode 943.最短超级串"
question_id: "943"
question: "最短超级串"
problem_url: "https://leetcode.cn/problems/find-the-shortest-superstring/"
created: "2021-03-20T20:58:28+08:00"
updated: "2021-03-20T20:58:28+08:00"
upvotes: 0
comments: 0
---

# 943. 最短超级串

> **[yiduobo的每日leetcode 943.最短超级串](https://zhuanlan.zhihu.com/p/358641242) · 知乎 · 2021-03-20 · 赞同 0**
> 力扣：[943. 最短超级串](https://leetcode.cn/problems/find-the-shortest-superstring/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

943.最短超级串

[力扣](https://leetcode-cn.com/problems/find-the-shortest-superstring/)

由于题目保证没有一个串是另一个串的子串，那么所有共用字符的情况就只可能是某个串的后缀能匹配上另一个串的前缀。当然，一个串可能与另外的多个串出现匹配，那么此时不能使用贪心法。

注意到这里串的个数比较少，最多只有12个，那么可以使用状态压缩来表示当前使用了哪些串。此时如果要新加入一个串，那么我们还需要知道目前构成结果的最后一个串是什么，因此可以得到一个状态f[state][i]，表示当前使用了state里面的串，以第i个串作为结尾的最短超级串的长度。

那么对于f[state][i]，我们可以先解析出state中有哪些串。若此时只有i这一个串，那么就有

f[state][i] \= len(words[i])

否则状态state必然是从state - (1 \<\< i)这个状态加上串i得来的。此时就可以枚举state中除了i之外的串，设为last，那么就有

f[state][i] \= min(f[state - (1 \<\< i)][last] + len(words[i]) - common[last][i]

其中common[last][i]表示last的后缀和i的前缀能匹配多少个字符，可以事先两两枚举预处理出来。

根据上面的做法，只需要枚举每个串x，然后计算f[1 \<\< n - 1][x]就能知道以x为结尾的最短超级串的长度，而答案就是里面最短的那一个。

此时，就有了一种得到最短超级串长度的做法了。为了得到具体的最短超级串，我们可以引入数组prev，其中prev[state][i]表示当前使用了state里面的串，以第i个串作为结尾的最短超级串的倒数第二个串是什么。

通过prev，我们就可以知道f\[state\]\[i\]是从f\[state - (1 \<\< i)\]\[prev\[state\]\[i\]\]转移过来的，从而逐步倒推构造出最终的答案。

```python
class Solution(object):
    def shortestSuperstring(self, words):
        """
        :type words: List[str]
        :rtype: str
        """

        n = len(words)

        suffix_set_list = []
        for i in range(n):
            suffix_set_list.append(set())
            for j in range(len(words[i]) - 1, 0, -1):
                suffix_set_list[-1].add(words[i][j:])

        common = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    for p in range(len(words[j]) - 1, 0, -1):
                        if words[j][:p] in suffix_set_list[i]:
                            common[i][j] = p
                            break
            common[i][i] = len(words[i])

        f = [[None] * n for _ in range(1 << n)]
        prev = [[None] * n for _ in range(1 << n)]

        min_len, last_word = None, None
        state = (1 << n) - 1

        for i in range(n):
            if min_len is None or self.dfs(state, i, n, f, common, prev) < min_len:
                min_len = self.dfs(state, i, n, f, common, prev)
                last_word = i
        
        res = ''
        while last_word is not None:
            prev_word = prev[state][last_word]
            if prev_word is None:
                common_len = 0
            else:
                common_len = common[prev_word][last_word]
            res = words[last_word][common_len:] + res
            state -= (1 << last_word)
            last_word = prev_word
        
        return res

    def dfs(self, state, last_word, n, f, common, prev):
        if f[state][last_word] is None:
            used = set()
            for i in range(n):
                if state & (1 << i):
                    used.add(i)

            if len(used) == 1:
                f[state][last_word] = common[last_word][last_word]
            else:
                prev_state = state - (1 << last_word)
                for i in used:
                    if i != last_word and (f[state][last_word] is None or f[state][last_word] > self.dfs(prev_state, i, n, f, common, prev) + common[last_word][last_word] - common[i][last_word]):
                        f[state][last_word] = self.dfs(prev_state, i, n, f, common, prev) + common[last_word][last_word] - common[i][last_word]
                        prev[state][last_word] = i
            
        return f[state][last_word]
```
