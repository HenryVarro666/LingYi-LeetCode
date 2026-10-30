---
title: "3343. 统计平衡排列的数目"
aliases: ["yiduobo的每日leetcode 3343.统计平衡排列的数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/七-其他线性-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/25686707200"
zhihu_id: "25686707200"
zhihu_title: "yiduobo的每日leetcode 3343.统计平衡排列的数目"
question_id: "3343"
question: "统计平衡排列的数目"
problem_url: "https://leetcode.cn/problems/count-number-of-balanced-permutations/"
difficulty: "Hard"
rating: 2615
created: "2025-02-23T00:06:05+08:00"
updated: "2025-02-23T00:06:05+08:00"
upvotes: 1
comments: 0
---

# 3343. 统计平衡排列的数目

> **[yiduobo的每日leetcode 3343.统计平衡排列的数目](https://zhuanlan.zhihu.com/p/25686707200) · 知乎 · 2025-02-23 · 赞同 1**
> 力扣：[3343. 统计平衡排列的数目](https://leetcode.cn/problems/count-number-of-balanced-permutations/) · Hard · 灵茶山艾府：[多重集排列数 + 计数 DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3343.统计平衡排列的数目

[3343. 统计平衡排列的数目 - 力扣（LeetCode）](https://leetcode.cn/problems/count-number-of-balanced-permutations/description/)

题目给出一个数字字符串num。若一个数字字符串中奇数位下标的数字之和，与偶数位下标的数字之和相等，那么就称这个数字字符串是平衡的。

问对于num的所有排列中，有多少个字符串是平衡的。

题目的数据规模并不大，字符串的长度最多为80，而对于这类填充类的问题，最先想到的自然是逐位填充的动态规划。不过需要注意的是，由于字符串中可能出现0到9一共10种数字，而在填充的过程中还需要监控每种数字的数目，因此逐位填充的动态规划其实并不好写。

---

既然逐位填充的方案行不通，那么不妨换一种思路，改成逐个数字填充。

在这里可以先判断特殊情况。不妨设num中所有数字之和为s，那么当s为奇数时，答案必然为0，可以直接返回。而对于s为偶数时，奇数位和偶数位的最终数字之和就应该为s // 2。由于题目只关心方案数，不关心具体的填充方案，那么在这里只需要计算将当前数字分配到奇数位和偶数位后占据的数位数量以及差值就行了，因此可以令f[v][even][diff]表示目前填充了所有的0、1、2、...、v，其中有even个数填充到了偶数位上，且奇数位和偶数位上数字和之差为diff时的方案数。这里有一个隐藏条件是在分配的过程中数字位之和不能超过s // 2。

对于数字v，可以先枚举所有的f[v - 1][pre_even][pre_diff]，然后考虑将v进行分配，得到对应的f[v][now_even][now_diff]。方便起见，记cnt[v]为v出现的次数，那么填充所有的0、1、2、...、v - 1这些数字后一共就填充了tot \= cnt[0] + cnt[1] + ... + cnt[v - 1]个数，若其中有pre_even个数填充到了偶数位，那么剩下的pre_odd \= tot - pre_even就填充到了奇数位上。

在这里需要注意的是，pre_even、pre_odd和pre_diff都需要在一定的边界内。具体来说，由于一共只有odd \= n // 2个奇数位，even \= n - odd个偶数位，因此pre_even必须小于等于even，同时pre_even也必须小于等于tot，同样的，pre_odd必须小于等于odd，而pre_diff则不能超过s // 2。

接下来枚举v的去处。一共有cnt[v]，不妨设有e个v填充到了偶数位，那么剩下的o \= cnt[v] - e个v将被填充到奇数位，因此在填充后偶数位和奇数位之差将会变为now_diff \= pre_diff + (e - o) \* v，同时now_even \= pre_even + e，now_odd \= pre_odd + o。

在这里需要注意的是，now_diff、now_even、now_odd也需要满足上面的限制条件。

接下来考虑这些v的具体分配方案数。由于一共有even个偶数位，填充0到v - 1用掉了pre_even个，因此还剩下even - pre_even个位置，从中选出e个位置填充v，因此一共有C(even - pre_even, e)种方案。同理，填充到奇数位上的v一共有C(odd - pre_odd, o)种方案，二者相乘就是可行的分配方案数。因此在这里就应该将

f[v - 1][pre_even][pre_diff] \* C(even - pre_even, e) \* C(odd - pre_odd, o)累加到f[v][now_even][now_diff]中。

按上面方式从0枚举到9，计算得到f后，最终答案就是f[9][even][0]。

注意到f的每一轮都只和上一轮的状态有关，因此在这里可以使用滚动数组省去v这一维。另外由于python的负数数字下标指的是数组倒序，因此对于diff这一维需要对所有diff加上s // 2这个偏移量，使得数组下标都变为非负。

最后附上python代码：

```python
class Solution(object):
    def countBalancedPermutations(self, num):
        """
        :type num: str
        :rtype: int
        """
        
        cnt = [0] * 10
        s = 0
        for c in num:
            cnt[int(c)] += 1
            s += int(c)
        
        if s % 2 == 1:
            return 0
        
        s //= 2
        odd = len(num) // 2
        even = len(num) - odd

        f = [[0] * (s + s + 1) for _ in range(even + 1)]
        f[0][s] = 1
        mod = 10 ** 9 + 7
        tot = 0

        C = [[0] * (even + 1) for _ in range(even + 1)]
        C[0][0] = 1
        for n in range(1, even + 1):
            for k in range(n + 1):
                if k == 0 or k == n:
                    C[n][k] = 1
                else:
                    C[n][k] = (C[n - 1][k - 1] + C[n - 1][k]) % mod

        for num in range(10):
            if cnt[num] == 0:
                continue
            g = copy.deepcopy(f)
            f = [[0] * (s + s + 1) for _ in range(even + 1)]
            for pre_even in range(min(even, tot) + 1):
                pre_odd = tot - pre_even
                for diff in range(s + s + 1):
                    if g[pre_even][diff] == 0:
                        continue
                    
                    for e in range(cnt[num] + 1):
                        o = cnt[num] - e
                        now_even = pre_even + e
                        now_odd = pre_odd + o
                        now_diff = diff + (e - o) * num
                        if now_even > even or now_odd > odd or now_diff < 0 or now_diff > s + s:
                            continue
                        f[now_even][now_diff] = (f[now_even][now_diff] + g[pre_even][diff] * C[even - pre_even][e] % mod * C[odd - pre_odd][o] % mod) % mod

            tot += cnt[num]

        return f[even][s]
```
