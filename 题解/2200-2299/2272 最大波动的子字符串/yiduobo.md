---
title: "2272. 最大波动的子字符串"
aliases: ["yiduobo的每日leetcode 2272.最大波动的子字符串"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/六-状态机-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/550038601"
zhihu_id: "550038601"
zhihu_title: "yiduobo的每日leetcode 2272.最大波动的子字符串"
question_id: "2272"
question: "最大波动的子字符串"
problem_url: "https://leetcode.cn/problems/substring-with-largest-variance/"
difficulty: "Hard"
rating: 2516
created: "2022-08-05T00:36:04+08:00"
updated: "2022-08-05T00:36:04+08:00"
upvotes: 0
comments: 0
---

# 2272. 最大波动的子字符串

> **[yiduobo的每日leetcode 2272.最大波动的子字符串](https://zhuanlan.zhihu.com/p/550038601) · 知乎 · 2022-08-05 · 赞同 0**
> 力扣：[2272. 最大波动的子字符串](https://leetcode.cn/problems/substring-with-largest-variance/) · Hard · 灵茶山艾府：[最大子数组和 + 状态机 DP（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2272.最大波动的子字符串

[力扣](https://leetcode.cn/problems/substring-with-largest-variance/)

题目的数据范围比较微妙，使用O(n^2)的算法枚举所有的字符串后，即使是利用前缀和也需要枚举所有的字符，时间上是比较吃紧的，因此需要另想办法。

受到朴素算法中枚举字符的启发，在这里也可以先枚举最终答案中出现次数最多的字符ma_char以及出现次数最少的字符mi_char，那么现在的问题就变成了寻找一个子串，使得子串中ma_char的数量减去mi_char的数量最大。这是一个典型的字符串动态规划问题，令f[i]表示以s[i]结尾的子串中，ma_char的数量减去mi_char数量的最大值，那么对于f[i]：

1、若s[i]既不是ma_char也不是mi_char，那么就有f[i] \= f[i - 1]

2、若s[i]是ma_char，那么在f[i - 1]的基础上加入s[i]显然是赚的。另外，若此前的f[i - 1]小于0，那么可以舍弃s[i]前面的部分，综合起来就是f[i] \= max(f[i - 1], 0) + 1

3、若s[i]是mi_char，与情况2相反，就有f[i] \= max(f[i - 1], 0) - 1

但是上面这个状态表示有一个问题，就是可能出现一个子串中全都是ma_char的情况。此时确实是ma_char的数量减去mi_char的数量最大，但是并不符合题目的要求，因此需要额外加入新的状态。令g[i]表示以s[i]结尾的子串中，至少存在一个mi_char，且ma_char的数量减mi_char的数量的最大值，那么对于g[i]：

1、若s[i]既不是ma_char也不是mi_char，那么就有g[i] \= g[i - 1]

2、若s[i]是ma_char，那么同样的，在g[i - 1]的基础上加入s[i]总是赚的。此时需要注意的是，即使此前的g[i - 1]小于0，在这里也不能舍弃掉s[i]前面的部分。因此此时就有g[i] \= g[i - 1] + 1

3、若s[i]是mi_char，与情况2不同，此时就可以根据g[i - 1]的大小选择是否舍弃掉s[i]之前的部分，因此即使全部舍弃掉，新加入的s[i]本身就是mi_char，此时的g[i]也是符合定义的。另一方面，此时的g[i]也可以通过f[i - 1]更新得到，同样是因为新加入的s[i]本身就是mi_char，因此并不要求s[i]之前的部分存在mi_char。综合起来，就是g[i] \= max(f[i - 1], g[i - 1], 0) - 1

到了这里，就可以一趟遍历，求出每一位f和g，然后取max(g)作为最终的答案。

上面算法的时间复杂度为O(26^2 \* n)，这里的26^2是枚举ma_char和mi_char的复杂度。不过实际上，在状态转移时会遇到很多s[i]既不是ma_char也不是mi_char的情况，这些情况下f和g都是不变的，那么如果想办法跳过这些字符，最终时间复杂度就是优化到O(26n)。至于跳过的方法，则可以先将每个字符出现的位置都收集起来，接下来在进行动态规划时则利用类似二路归并的做法，每次使用当前未使用过的ma_char以及未使用过的mi_char中最左侧的那一个来更新f和g，然后继续向后考虑剩下的ma_char和mi_char。

最后，由于f和g都只依赖于上一轮的状态，因此可以使用两个遍历迭代来节省f和g的数组空间。

最后附上python代码：

```python
class Solution(object):
    def largestVariance(self, s):
        """
        :type s: str
        :rtype: int
        """

        pos_dict = {}
        for index, char in enumerate(s):
            if char not in pos_dict:
                pos_dict[char] = []
            pos_dict[char].append(index)
        
        res = 0
        for ma_char, ma_pos in pos_dict.items():
            for mi_char, mi_pos in pos_dict.items():
                if ma_char == mi_char:
                    continue
                
                i = j = 0
                f = 0
                g = -len(s) - 1
                while i < len(ma_pos) and j < len(mi_pos):
                    if ma_pos[i] < mi_pos[j]:
                        f = max(f, 0) + 1
                        g += 1
                        i += 1
                    else:
                        g = max(f, g, 0) - 1
                        f = max(f, 0) - 1
                        j += 1
                
                    res = max(res, g)
                
                if i < len(ma_pos):
                    for index in range(i, len(ma_pos)):
                        f = max(f, 0) + 1
                        g += 1
                        res = max(res, g)
                else:
                    res = max(res, max(f, g, 0) - 1)
                    
        return res
```
