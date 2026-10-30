---
title: "3995. 转换字符串的最小成本III"
aliases: ["yiduobo的每日leetcode 3995.转换字符串的最小成本III"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/七-其他线性-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2063034613350638255"
zhihu_id: "2063034613350638255"
zhihu_title: "yiduobo的每日leetcode 3995.转换字符串的最小成本III"
question_id: "3995"
question: "转换字符串的最小成本 III"
problem_url: "https://leetcode.cn/problems/minimum-cost-to-convert-string-iii/"
difficulty: "Hard"
rating: 2101
created: "2026-07-21T23:15:43+08:00"
updated: "2026-07-21T23:15:44+08:00"
upvotes: 0
comments: 0
---

# 3995. 转换字符串的最小成本III

> **[yiduobo的每日leetcode 3995.转换字符串的最小成本III](https://zhuanlan.zhihu.com/p/2063034613350638255) · 知乎 · 2026-07-21 · 赞同 0**
> 力扣：[3995. 转换字符串的最小成本 III](https://leetcode.cn/problems/minimum-cost-to-convert-string-iii/) · Hard · 灵茶山艾府：[动态规划 + 暴力枚举（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3995.转换字符串的最小成本III

<https://leetcode.cn/problems/minimum-cost-to-convert-string-iii/description/>

题目给出两个字符串source和target，长度均不超过5000。

另外给出一个二维字符串数组rules，其长度不超过200。其中rules\[index\] \= \[pattern\[index\], replacement\[index\]\]，以及一个整数数组costs，其中costs\[index\]是应用rules\[index\]的基础成本。两个数组的长度相同。另外，每一组pattern\[index\]和replacement\[index\]的长度相同，且不超过20。

现在可以任意次数地应用任意规则。每次应用规则rules[index]的过程如下：

- 选择当前字符串的一个下标p，要求满足p到p + pattern[index].length - 1这下下标都位于当前字符串中，同时这些下标在之前没有被使用过
- 对于pattern[index]中的每个下标，其要么是'\*'，要么必须等于当前字符串中从p开始，长度为pattern[index].length的子串中的对应字符
- 将这个从p开始，长度为pattern[index].length的子串替换为replacement[index]
- 这次替换的成本为costs[index]加上pattern[index]中'\*'的数量

问通过使用规则，将source转换为target的最小成本。若不可行，则返回-1。

经典的动态规划题目。令f[index]表示将source的前index个字符转换为target的前index个字符所需的最小成本，一开始有f[0] \= 0表示空字符串一开始就相同。接下来对于每个f[index]：

1、先考虑不使用规则的情况：

若source[index - 1] \= target[index - 1]，那么就有f[index] \= f[index - 1]；反之，则需要将f[index]置为-1，表示目前没有找到操作的方案

2、接下来遍历每一组规则：

首先，若当前的pattern长度大于index，或者f[index - len(pattern)]为-1，那么就无法将当前规则运用在以index结束的子串上。

接下来，可以先检测target[index - len(pattern): index]是否恰好等于replacement，因为这里无需处理'\*'的情况，因此可以直接通过字符串之间的比较进行判断。若不等于，说明当前规则无法使用。

最后，再从index - len(pattern)到index - 1遍历source，检测pattern中的每个字符是否满足要么是'\*'，要么等于source中的对应字符。若至少有一个位置不满足，则说明当前规则无法使用。在这个过程中，需要顺便统计pattern中星号的数量，记为star。

若以上的检测都通过了，那么就使用f[index - len(pattern)] + costs + start来更新f[index]即可。

全部遍历完成后，f[-1]即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minCost(self, source, target, rules, costs):
        """
        :type source: str
        :type target: str
        :type rules: List[List[str]]
        :type costs: List[int]
        :rtype: int
        """
        
        if len(source) != len(target):
            return -1
        
        f = [0]
        info = sorted(zip(rules, costs), key=lambda d:len(d[0][0]))
        for index in range(1, len(source) + 1):
            if source[index - 1] == target[index - 1]:
                f.append(f[-1])
            else:
                f.append(-1)
            
            for (p, r), c in info:
                if len(p) > index:
                    break
                if f[index - len(p)] == -1 or target[index - len(p): index] != r:
                    continue

                star = 0
                flag = True
                for s_char, p_char in zip(source[index - len(p): index], p):
                    if p_char == '*':
                        star += 1
                        continue
                    if s_char != p_char:
                        flag = False
                        break
                    
                if flag and (f[-1] == -1 or f[-1] > f[index - len(p)] + c + star):
                    f[-1] = f[index - len(p)] + c + star

        return f[-1]
```
