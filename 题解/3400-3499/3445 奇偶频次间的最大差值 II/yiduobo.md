---
title: "3445. 奇偶频次间的最大差值II"
aliases: ["yiduobo的每日leetcode 3445.奇偶频次间的最大差值II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/two-pointers", "leetcode/enumeration", "leetcode/prefix-sum", "leetcode/sliding-window", "题单/常用数据结构", "题单/常用数据结构/一-前缀和"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1892380953931911452"
zhihu_id: "1892380953931911452"
zhihu_title: "yiduobo的每日leetcode 3445.奇偶频次间的最大差值II"
question_id: "3445"
question: "奇偶频次间的最大差值 II"
problem_url: "https://leetcode.cn/problems/maximum-difference-between-even-and-odd-frequency-ii/"
difficulty: "Hard"
rating: 2694
created: "2025-04-07T02:27:16+08:00"
updated: "2025-04-07T02:27:16+08:00"
upvotes: 0
comments: 0
---

# 3445. 奇偶频次间的最大差值II

> **[yiduobo的每日leetcode 3445.奇偶频次间的最大差值II](https://zhuanlan.zhihu.com/p/1892380953931911452) · 知乎 · 2025-04-07 · 赞同 0**
> 力扣：[3445. 奇偶频次间的最大差值 II](https://leetcode.cn/problems/maximum-difference-between-even-and-odd-frequency-ii/) · Hard · 灵茶山艾府：[枚举+前缀和+滑动窗口（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3445.奇偶频次间的最大差值II

[3445. 奇偶频次间的最大差值 II - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-difference-between-even-and-odd-frequency-ii/description/)

题目给出一个字符串s以及一个整数k，s长度可到30000，但是其中仅包含字符'0'到'4'。

要求找出s的子串subs中两个字符出现频次的最大差值freq[a] - freq[b]，其中：

1、subs的长度至少为k

2、a在subs中出现了奇数次

3、b在subs中出现了偶数次，这里的偶数次不能为0次

问最大的差值为多少。

本题虽然是之前3442题的进阶版，但是就题目要做的事情来说实际上更像是之前的3434题，都是要找出一个最优的子段。

[yiduobo：yiduobo的每日leetcode 3434.子数组操作后的最大频率](https://zhuanlan.zhihu.com/p/1890927742930907222)

与3434题不同的是，由于a和b都不确定，那么在这里再想一次性解决所有的问题就比较困难了。不过好在s中仅包含'0'到'4'最多5种不同的数字，那么在这里就可以先暴力枚举所有a和b的组合，接下来将s中所有的'a'都变为1，'b'都变为-1，其余元素都变为0，问题就变成了从得到的数组中找出一个子段和最大，且长度大于等于k的子串，这个子串中1出现的次数为奇数，-1出现的次数为偶数且大于0。

---

接下来针对这个转化后的问题进行讨论。

由于有了长度以及出现次数的限制，在这里用贪心法就不太方便了。对于子段和问题，另一种常见的处理方法就是转化为前缀和。对于以下标index为右边界的前缀，先计算当前的前缀和，然后找出之前出现过的前缀和最小，且符合题目要求的另一个前缀，二者相减即为以index为右边界的最大合法子段和。

这里所说的符合题目要求，指的就是这两个前缀和相减后对应的子段，需要满足上面长度大于等于k以及1和-1出现次数奇偶性的限制。

其中长度的限制是比较容易处理的。为了方便前缀和的运算，在这里记空串的前缀和为0，以index为右边界的前缀和是第index + 1个前缀和，那么只需将这个要找的最小前缀和限定在第0个到第index - k + 1个前缀和之间，就可以保证前缀和相减后对应的子段长度大于等于k。

而对于1和-1出现次数奇偶性的限制则相对复杂，不过好在只需要考虑1和-1两种元素的奇偶性，一共也就只有四种可能的情况，因此在这里可以利用状态压缩来进行处理。

设计状态state为两位的二进制数，其中高位表示1出现的次数是否为奇数次，若为奇数次这一位为1，否则为0；低位则表示-1出现的次数是否为奇数次，若为奇数次这一位为1，否则为0。

接下来就可以一趟遍历，使用两个数组f和state分别记录前缀和以及对应的state，同时使用两个变量state_a和state_b分别记录前缀中1和-1的奇偶性。那么对于当前遍历到的index，先通过v来更新f，然后根据当前元素值v是否为1或者-1来修正state_a和state_b，就可以通过state_a \<\< 1 | state_b来得到当前前缀对应的state。

为了使得子段中1出现奇数次，-1出现偶数次，那么对于另一个可用前缀，其中1出现次数的奇偶性就必须与state_a相反，而-1出现次数的奇偶性则必须与state_b相同，因此这个可用前缀对应的状态pre_state只能是(state_a ^ 1) \<\< 1 | state_b。

到了这里，问题就变成了从第0到第index - k + 1个前缀中找出对应的状态为pre_state，且前缀和最小的那一个。每次都去遍历寻找显然是不优的，在这里可以使用另一个数组best，用来记录可用前缀和中每种state对应的最小值。记当前可用前缀的最大右边界为left，那么随着index的移动，left也必然是跟着向后移动的，而当left向后移动时，只需使用f\[left\]来更新best\[state\[left\]\]就行了。

有了best，以index为右边界，且长度大于等于k，其中1和-1出现次数分别为奇数次和偶数次的最大子段和就是f[index + 1] - best[pre_state]。

需要特别注意的是，上面的做法并没有处理-1出现次数为0次的情况。这种情况下依然符合上面定义的-1出现了偶数次，但是不符合题目要求的b出现的次数不能为0。为了处理这种情况，还需要额外使用两个变量pre_first_b以及pre_second_b来记录-1最近两次出现的下标。在left移动时，除了长度k的限制之外，还需要保证left在pre_second_b的左侧，这样一来前缀相减得到的子串中就至少有两个-1了。另外由于1的出现次数限定为奇数次是不可能为0的，因此无需对1做类似的处理。

最后附上python代码：

```python
class Solution(object):
    def maxDifference(self, s, k):
        """
        :type s: str
        :type k: int
        :rtype: int
        """
        
        def calc(a, b):
            val = [0] * len(s)
            for index, char in enumerate(s):
                if char == a:
                    val[index] = 1
                elif char == b:
                    val[index] = -1
                else:
                    val[index] = 0
            
            f = [0]
            state = [0]
            pre_first_b = None
            pre_second_b = None
            left = 0
            state_a = 0
            state_b = 0
            best = [None] * 4
            res = -len(s)
            for index, v in enumerate(val):
                f.append(f[-1] + v)
                if v == 1:
                    state_a ^= 1
                elif v == -1:
                    state_b ^= 1
                    pre_first_b, pre_second_b = index + 1, pre_first_b
                
                state.append(state_a << 1 | state_b)

                while index - left + 1 >= k and left < pre_second_b:
                    if best[state[left]] is None or best[state[left]] > f[left]:
                        best[state[left]] = f[left]
                    left += 1
            
                pre_state = (state_a ^ 1) << 1 | state_b
                if best[pre_state] is not None:
                    res = max(res, f[-1] - best[pre_state])

            return res

        char_set = set(s)
        res = -len(s)
        for a in char_set:
            for b in char_set:
                if a == b:
                    continue
                res = max(res, calc(a, b))
        
        return res
```
