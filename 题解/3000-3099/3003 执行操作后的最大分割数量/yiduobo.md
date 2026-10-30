---
title: "3003. 执行操作后的最大分割数"
aliases: ["yiduobo的每日leetcode 3003.执行操作后的最大分割数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/bitmask", "题单/动态规划", "题单/动态规划/七-其他线性-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/693278330"
zhihu_id: "693278330"
zhihu_title: "yiduobo的每日leetcode 3003.执行操作后的最大分割数"
question_id: "3003"
question: "执行操作后的最大分割数量"
problem_url: "https://leetcode.cn/problems/maximize-the-number-of-partitions-after-operations/"
difficulty: "Hard"
rating: 3039
created: "2024-04-19T02:56:00+08:00"
updated: "2024-04-19T02:56:00+08:00"
upvotes: 0
comments: 0
---

# 3003. 执行操作后的最大分割数

> **[yiduobo的每日leetcode 3003.执行操作后的最大分割数](https://zhuanlan.zhihu.com/p/693278330) · 知乎 · 2024-04-19 · 赞同 0**
> 力扣：[3003. 执行操作后的最大分割数量](https://leetcode.cn/problems/maximize-the-number-of-partitions-after-operations/) · Hard · 灵茶山艾府：[两种方法：记忆化搜索 / O(n) 前后缀分解（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3003.执行操作后的最大分割数

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-the-number-of-partitions-after-operations/description/)

首先考虑边界情况。当k为26时，是不可能分割字符串的，因此最终答案必然为1。

接下来是一般情况。

如果不执行任何操作，从任意下标开始的原始分割字符串的终点就可以通过滑动窗口来求解。具体来说，使用一个滑动窗口从左向右滑动，在保持窗口内出现的不同字符数量不超过k个前提下尽量向右扩展窗口的右边界，这个右边界就是以当前窗口左边界开始进行分割的字符串终点。在这里使用数组max_k记录每个下标开始的原始分割字符串对应的终点，即max_k[index]表示从index开始的字符串的终点。

---

如果要执行变更操作，那么就需要先考虑执行变更操作的时机与最佳下标位置。

令f[index]表示以下标index开头的后缀，在不进行任何变更操作的情况下可以得到的最大分割数，而g[index]则表示以下标index开头的后缀，在最多执行一次变更操作的情况下可以得到的最大分割数。

需要注意的是，由于题目执行的分割是分割掉前缀，因此在这里需要从后向前进行状态转移。

其中，f[index]的状态转移是比较简单的，因为对于index而言，其分割字符串的终点已经定死在max_k[index]了，于是就有f[index] \= f[max_k[index] + 1] + 1，表示将index到max_k[index]这一段分割出去。

而对于g[index]，则多出了分割点需要考虑。

---

第一种情况：不执行变更操作也是没有问题的，因此也可以用相同的方法来初始化g[index]，即g[index] \= g[max_k[index] + 1] + 1

---

第二种情况：观察样例一，可以发现一种可行的变更位置选择是在以index开头的字符串中刚好有k个不同字符时，对下一个重复字符进行变更。样例中的accca，其中以0开头的字符串，ac已经有两个不同字符，那么对于其下一个字符，如果是之前重复出现的c，就可以考虑对其进行变更。选择最左侧的c变更是因为这样一来留给后续的字符数量最多，可能分割的字符串也最多，是最优的选择之一。

为了方便描述，在这里记以index开头的字符中，首次出现第k种不同字符的下标为k_point。对于k_point的计算，实际上就是寻找以每个下标开始的字符串中首次出现k个不同字符的下标位置，同样可以使用滑动窗口求解。在这里可以与max_k的求解一起进行，使用数组min_k来记录每个位置对应的k_point，即min_k[index]表示以index开头的字符串中首次出现第k中不同字符的下标。

回到g的状态转移。记变更的下标为change_point，那么就有change_point \= k_point + 1。当然，在这里也不是一定就值得进行变更操作。

首先，如果k_point已经来到了字符串的末位，那么change_point本身就不存在。另一方面，如果k_point等于max_k[index]，则说明change_point原来对应的字符本来就没有在以index开头的原始分割字符串中出现过，此时也就没有通过变更change_point对应的字符来将以index开头的字符串划分出去的必要了。

对于上面两种情况，不考虑变更change_point的字符。

而对于其他情况，则需要考虑变更后的状态是什么样子。

首先还是边界情况。如果change_point来到了字符串的末位，那么在这里将其变更后可以得到一个单个字符形成的字符串，那么从index开始的分割就是index到k_point，以及change_point这两个字符串，于是可以用2来更新g[index]。

如果change_point并不是字符串的末位，就需要考虑将change_point变更后的字符串分割是什么样的。

需要特别注意的是，在这里由于对change_point进行了变更，因此之前的min_k\[change_point\]以及max_k\[change_point\]都将失效，在这里不能再利用这两个数组来进行状态转移。但是值得庆幸的是，change_point的下一个位置，记为nxt_point，其min_k是依然有效的。如果min_k\[nxt_point\]是从nxt_point开始的字符串中第k个不同字符首次出现的下标，那么将change_point变成nxt_point到min_k\[nxt_point\]中不存在的字符，那么min_k\[nxt_point\]就会变成从change_point开始的字符串中第k + 1个不同字符，而变更后的max_k\[change_point\]恰好就是min_k\[nxt_point\] - 1，于是就有g\[index\] \= max(g\[index\], f\[min_k\[nxt_point\]\] + 2)。

简单的形象表示：

index, index + 1, ...., min_k[index], change_point, nxt_point, nxt_point + 1, ..., min_k[nxt_point + 1]，...

划分后得到的是

（index, index + 1, ...., min_k[index]）,（change_point, nxt_point, nxt_point + 1, ...,)，min_k[nxt_point + 1]，...

需要特别注意的是，在这里能够变更change_point有两个前提。

第一个是有变更的空间。因为change_point变更后的字符不能与index到min_k[index]之间的字符相同，也不能与nxt_point到min_k[nxt_point]之间的字符相同，因此在这里还需要维护一个数组char_state，用来表示每个下标index开始的原始字符串中包含的不同字符，在这里可以用一个26为的二进制来表示，可以在滑动窗口计算min_k时一并计算。那么这里的条件就可以写成char_state[index] | char_state[nxt_point] !\= 1\<\<26 - 1，即前后两段覆盖的字符不是全体字符。

第二个就是有变更的必要。如果从nxt_point开始的原始划分字符串中包含的字符总数不足k种时，此时修改change_point的字符后，从change_point开始的划分字符串中包含的字符总数也不会超过k种，对于这种情况，只有当min_k[nxt_point]为n - 1，即从nxt_point开始的字符串是最后一个字符串时才有划分的意义，此时相当于通过change_point将最后这个字符串从index开始的字符串中切分出去了，这种情况下应该用2来更新g[index]；反之，如果从nxt_point开始的原始划分字符串中包含了k种不同的字符，那么说明在这里有必要进行划分，可以使用上面的转移方程。到了这里，又需要维护另一个数组full_k，用来保存每个下标开始的原始划分字符串中是否包括k种字符，full_k同样是在滑动窗口计算min_k时一并计算。

---

除了上面的第二种情况外，实际上还存在另外的变更方案。我一开始也没有考虑到，提交看到了错误的case才发现。例如字符串aabca，当k等于3时，是不存在情况2中的nxt_point的，但是在这里如果将第二个a变成e，字符串变成了aebca，就可以得到aeb和ca两段划分。即，划分的位置处于index到k_point之间。

更具体的：

1、若k_point之前存在重复的字符，那么将其中某个重复字符替换掉，从index到k_point - 1之间就可以得到k种不同字符形成一个划分，此时就有g[index] \= max(g[index], f[k_point] + 1)。

在这里判断有重复字符可以通过鸽笼原理，即一个长度大于k的字符串中，如果只出现了k种字符，那么就必然有重复的字符。在这里只需要检测index到k_point的长度，即k_point - index + 1是否大于k即可。

另一方面，在这里也要求index开始的字符串中包含的字符种类数等于k种，要不然修改其中的重复字符也没有任何作用，即full_k[index]为true。

2、通过1中的重复字符检测可以联想到，如果index到k_point中刚好出现了k种字符的话是否还可以修改index到k_point之间的字符？答案是肯定的。在这里可以通过修改其中的某个字符从而隔断k_point与k_point + 1，使得k_point不仅是min_k[index]，也变成max_k[index]，此时就有g[index] \= max(g[index], f[k_point + 1] + 1)。

这种情况下修改是一定成立的，只需将index到k_point之间原来等于k_point + 1位置的字符修改成其他字符就行了。另一方面，这种情况还要求min_k[index]小于max_k[index]，因为若一开始的min_k[index]就等于max_k[index]，不修改时下一个划分点也在k_point + 1，也就没有修改的必要了。

---

到了这里，就得到了最终的算法。

1、首先进行预处理，利用两个滑动窗口计算上面的min_k、max_k、char_state、full_k

2、接下来进行动态规划。使用上面定义的f和g数组，f数组的转移直接进行，g数组的转移在直接进行的基础上，还需要分别讨论变更index到k_point之间的字符以及变更k_point + 1位置上的字符，具体的方式与上面情况2和情况3中讨论的相同。

最后附上python代码：

```python
class Solution(object):
    def maxPartitionsAfterOperations(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """

        if k == 26:
            return 1

        n = len(s)
        p = q = 0
        min_k = []
        max_k = []
        char_state = []
        full_k = []

        min_freq = {}
        max_freq = {}
        
        state = 0
        for index in range(n):
            while p < n and len(min_freq) < k:
                min_freq[s[p]] = min_freq.get(s[p], 0) + 1
                state |= (1 << (ord(s[p]) - 97))
                p += 1
            min_k.append(p - 1)
            char_state.append(state)
            full_k.append(len(min_freq) == k)

            min_freq[s[index]] -= 1
            if min_freq[s[index]] == 0:
                min_freq.pop(s[index])
                state ^= (1 << (ord(s[index]) - 97))

            while q < n and (len(max_freq) < k or (len(max_freq) == k and s[q] in max_freq)):
                max_freq[s[q]] = max_freq.get(s[q], 0) + 1
                q += 1
            max_k.append(q - 1)

            max_freq[s[index]] -= 1
            if max_freq[s[index]] == 0:
                max_freq.pop(s[index])
    

        f = [0] * (n + 1)
        g = [0] * (n + 1)
        for index in range(n - 1, -1, -1):
            f[index] = f[max_k[index] + 1] + 1
            g[index] = g[max_k[index] + 1] + 1

            k_point = min_k[index]

            if k_point - index + 1 > k and full_k[index]:
                g[index] = max(g[index], f[k_point] + 1)

            if k_point - index + 1 == k:
                g[index] = max(g[index], f[k_point + 1] + 1)

            if k_point < n - 1 and min_k[index] != max_k[index]:
                change_point = k_point + 1
                if change_point + 1 == n:
                    g[index] = max(g[index], 2)
                else:
                    nxt_point = change_point + 1
                    if (char_state[index] | char_state[nxt_point]) != (1 << 26) - 1:
                        if full_k[nxt_point]:
                            g[index] = max(g[index], f[min_k[nxt_point]] + 2)
                        elif min_k[nxt_point] == n - 1:
                            g[index] = max(g[index], 2)

        print f, g

        return g[0]
```
