---
title: "3539. 魔法序列的数组乘积之和"
aliases: ["yiduobo的每日leetcode 3539.魔法序列的数组乘积之和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/七-其他线性-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1907566908812788777"
zhihu_id: "1907566908812788777"
zhihu_title: "yiduobo的每日leetcode 3539.魔法序列的数组乘积之和"
question_id: "3539"
question: "魔法序列的数组乘积之和"
problem_url: "https://leetcode.cn/problems/find-sum-of-array-product-of-magical-sequences/"
difficulty: "Hard"
rating: 2694
created: "2025-05-18T23:11:47+08:00"
updated: "2025-05-18T23:11:47+08:00"
upvotes: 1
comments: 0
---

# 3539. 魔法序列的数组乘积之和

> **[yiduobo的每日leetcode 3539.魔法序列的数组乘积之和](https://zhuanlan.zhihu.com/p/1907566908812788777) · 知乎 · 2025-05-18 · 赞同 1**
> 力扣：[3539. 魔法序列的数组乘积之和](https://leetcode.cn/problems/find-sum-of-array-product-of-magical-sequences/) · Hard · 灵茶山艾府：[状态设计 + 多重集排列数 + 可行性剪枝（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3539.魔法序列的数组乘积之和

[3539. 魔法序列的数组乘积之和 - 力扣（LeetCode）](https://leetcode.cn/problems/find-sum-of-array-product-of-magical-sequences/)

题目给出两个整数m和k，其中1 \<\= k \<\= m \<\= 30，另外给出一个整数数组nums，其长度n不超过50。

接下来对于一个整数序列seq，如果满足以下三个条件：

1）seq的长度为m

2）seq中元素的大小在0到n - 1之间

3）2^seq[0] + 2^seq[1] + ... + 2^seq[m - 1]的二进制表示中恰好有k个1

那么就称seq为魔法序列，定义其乘积为nums\[seq\[0\]\] \* nums\[seq\[1\]\] \* ... \* nums\[seq\[m - 1\]\]。

问所有合法魔法序列的数组乘积之和，结果需要对10^9 + 7取模。

题目描述中的魔法序列实际上就是要选出m个0到n - 1之间的数，可以重复选择，然后以这些元素为指数的2的幂次之和的二进制表示中恰好有k个1。

由于可以重复选择，那么当选取多个相同元素时，以这些元素为指数的2的幂次之和就会产生进位，这将会对1的数量产生影响。例如选取3个0时，得到的是2^0 + 2^0 + 2^0 \= 3，二进制表示中有两个1，但是选取4个1时，得到的却是2^0 + 2^0 + 2^0 + 2^0 \= 4，二进制表示中只剩下一个1了。

另一方面，seq中元素的大小顺序只会影响去重，但是不会影响2的幂次之和以及数组乘积的计算，因此可以安装元素值从小到大的顺序来构造seq。

---

基于以上两点，就可以得到一种基本的动态规划算法。

令f[index][x][state]表示选取了x个0到index - 1之间的元素，以这些元素为指数的2的幂次和为state时的数组乘积总和，那么对于f[index][x][state]，还有m - x个位置没有填充，因此可以枚举接下来会填充y个值为index的元素，那么得到的nxt_state就等于state + y \* 2^index，于是就有

f[index + 1][x + y][nxt_state] +\= f[index][x][state] \* C(m - x, y) \* nums[index]^y

其中C(m - x, y)表示从剩下m - x个位置中选出y个位置来填充index的方案数，而最后的nums[index] ^ y则是因为填充了y个index，数组乘积需要乘上y个nums[index]。

---

然而本题中index的取值范围在0到n - 1之间，state中可能的状态数太多了，需要进行优化。

注意到随着index的遍历，其对应的2^index也是越来越大的，对state二进制表示中的0到index - 1这些数位不会产生任何影响，因此对于这些数位，只需要记录其中1的数目cnt，而不需要记录其具体是什么样的。更进一步的，在去掉这些数位后，对于f[index][x][state]，在极限情况下也只能选取x个值为index - 1个元素，而state表示的是移除掉第0到第index - 1位的幂次和，因此state的值不会超过x的一半。

这样一来，对于f[index][x][state]，依然是枚举值为index的元素数量y，基于目前state截断低位后的定义，此时就可以直接将y而不是y \* 2^index累加到state中，得到nxt_state。

接下来需要对nxt_state进行截断，具体来说，若其最低位为1，那么低位1的数量就需要加上1，可以记nxt_delta为1，否则记nxt_delta为0。得到nxt_delta后，将nxt_state除以2就完成了截断。

得到nxt_delta以及nxt_state后，还需要再枚举f[index][x][state]中所有可能的低位1数量cnt，接下来就有

f[index + 1][x + y][nxt_state][cnt + nxt_delta] +\= f[index][x][state][cnt] \* C(m - x, y) \* nums[index]^y

全部计算完成后，需要枚举f[-1][-1]中的每种state，将f[-1][-1][state][k - bit_set(state)]累加到答案中，其中bit_set(x)表示x二进制表示中1的数量。这样做的理由是最终幂次之和的二进制表示中需要恰好有k个1，去除掉state中的1之后，剩下低位1的数量就是k - bit_set(state)个。

---

另外本题中还涉及都组合数以及取模，又要用到乘法逆元。在具体实现上，在枚举y时可以基于上一个y的结果C(m - x, y - 1) \* nums[index]^(y - 1)来更新C(m - x, y) \* nums[index]^y，也就是说在之前的结果上乘以(m - x - y + 1) \* inv[y] \* nums[index]即可，其中inv[y]为y的乘法逆元。

最后附上python代码：

```python
class Solution(object):
    def magicalSum(self, m, k, nums):
        """
        :type m: int
        :type k: int
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        
        set_bit = [0] * (m + 1)
        for x in range(m + 1):
            tmp = x
            while tmp:
                set_bit[x] += 1
                tmp -= tmp & -tmp

        mod = 10 ** 9 + 7

        inv = [None, 1]
        for x in range(2, m + 1):
            inv.append(-(mod // x) * inv[mod % x] % mod)

        f = [[[{} for _ in range((m >> 1) + 1)] for _ in range(m + 1)] for _ in range(n + 1)]
        f[0][0][0][0] = 1
        for index in range(n):
            for x in range(m + 1):
                for state in range((x >> 1) + 1):
                    v = 1
                    for y in range(m - x + 1):
                        nxt_state = state + y
                        nxt_delta = nxt_state & 1
                        nxt_state >>= 1
                        if y > 0:
                            v = v * (m - x - y + 1) * inv[y] * nums[index] % mod

                        for cnt in f[index][x][state]:
                            nxt_cnt = cnt + nxt_delta
                            if nxt_cnt <= k:
                                f[index + 1][x + y][nxt_state][nxt_cnt] = (f[index + 1][x + y][nxt_state].get(nxt_cnt, 0) + f[index][x][state][cnt] * v % mod) % mod

        res = 0
        for state in range((m >> 1) + 1):
            res += f[-1][-1][state].get(k - set_bit[state], 0)
        
        return res % mod
```
