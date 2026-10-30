---
title: "3287. 求出数组中最大序列值"
aliases: ["yiduobo的每日leetcode 3287.求出数组中最大序列值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/dynamic-programming", "leetcode/enumeration", "题单/动态规划", "题单/位运算", "题单/动态规划/三-背包", "题单/动态规划/专题-前后缀分解", "题单/位运算/五-试填法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/855053187"
zhihu_id: "855053187"
zhihu_title: "yiduobo的每日leetcode 3287.求出数组中最大序列值"
question_id: "3287"
question: "求出数组中最大序列值"
problem_url: "https://leetcode.cn/problems/find-the-maximum-sequence-value-of-array/"
difficulty: "Hard"
rating: 2545
created: "2024-10-08T00:31:19+08:00"
updated: "2024-10-08T00:31:19+08:00"
upvotes: 0
comments: 0
---

# 3287. 求出数组中最大序列值

> **[yiduobo的每日leetcode 3287.求出数组中最大序列值](https://zhuanlan.zhihu.com/p/855053187) · 知乎 · 2024-10-08 · 赞同 0**
> 力扣：[3287. 求出数组中最大序列值](https://leetcode.cn/problems/find-the-maximum-sequence-value-of-array/) · Hard · 灵茶山艾府：[前后缀分解 + 二维 0-1 背包 + 优化所选元素个数 + 试填法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3287.求出数组中最大序列值

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-maximum-sequence-value-of-array/description/)

题目给出一个整数数组nums以及一个正整数k，定义长度为2 \* x的序列seq的值为

(seq[0] OR seq[1] OR ... OR seq[x - 1]) XOR (seq[x] OR seq[x + 1] OR ... OR seq[2 \* x - 1])

请你求出nums中所有长度为2 \* k的子序列的最大值。

---

对于这类两个部分的结果组合形成最终结果的问题，一般的处理方法就是找一个分割点划开，然后分别计算前半部分和后半部分可以达成的所有可行结果，从中选出最优的结果对构成最终的结果。

回到本题。注意到本题中nums的取值范围不超过2^7，因此可以尝试直接将数值表示在状态中。

对于前半部分可以达成的所有结果，就是f\[i\]\[j\]\[k\]表示是否可以从nums的前i个数中选取j个数，这些数的按位或结果为k。初始状态下f\[0\]\[0\]\[0\]为true，其他均为false。接下来对于所有值为true的f\[i\]\[j\]\[k\]，若接下来选取nums\[i + 1\]，那么f\[i + 1\]\[j + 1\]\[k | nums\[i + 1\]\]true；若不选取，则有f\[i + 1\]\[j\]\[k\] \= true。

得到f后，令rf[i][j][k]表示是否可以从nums的最后i个数中选取j个数，这些数的按位或结果为k，此时只需反向遍历nums，按相同的方法计算出rf。

得到f和rf之后，需要枚举分割点以及所有可能的取值，还是有点复杂，在这里可以先进行进一步的转化。

令g[k]表示所有值为true的f[i][x][k]中最小的i，rg[k]则表示所有值为true的rf[i][x][k]中最小的i，在计算f和rf时可以同步更新g和rg。

得到g和rg之后，就可以从大到小枚举最终结果res，以及左半边的按位或取值left_part，那么右半边的取值right_part \= res ^ left_part，若g[left_part] + rg[right_part]小于等于n，那么res即为最终答案。

这样做表示的是通过nums的前g[left_part]个元素中选出x个构成left_part，nums的后g[right_part]个元素中选出x个构成right_part，只要这里的前g[left_part]个元素与后g[right_part]个元素不重叠，就可以通过这2x个元素构造出res。

对于上面给出的算法，计算f和rf的时间复杂度为O(n^2 \* ma)，计算最终答案的时间复杂度为O(ma^2)。其中n \<\= 400, ma \< 128。即使通过一些常数优化让i枚举的范围缩进都到200，计算f的运算次数依然在200^2 \* 128这个量级，是比较危险的，还需要再进行优化。

---

优化的突破点依然是nums的取值范围。由于nums最大的取值也只有127，也就是全为1的7位二进制，而f的计算又是基于按位或的，那么若f[i][j][k]为true，当j > 7时一定也有f[i][7][k] \= true，因为在最坏情况下也只需要选出来的7个数，每个为特定的二进制位上提供一个1就行了。换言之，之前的状态f[i][j][k]中的j这一维，上限就可以从x降低到min(x, 7)。

不过需要注意的是，题目要求一定要凑够x个数，那么即使存在j \<\= 7的f[i][j][k]为true，f[i][x][k]也不一定为true，因为其他的数字可能在k的非1二进制位上恰好为1，例如想通过在[2, 2, 2, 2, 2, 2, 2, 1, 1, 1]中选出8个数，使得按位或的结果为2，此时的f[11][1][2]到f[11][7][2]都为true，但是由于后续的1都不能被选取，因此f[11][8][2]依然为false。

换言之，当x \<\= 7时，通过仅计算所有j \<\= 7的f[i][j][k]是没有问题的，但是当x > 7时，就需要想办法找一些群演来填剩下的坑了。找群演的标准其实很简单，只需其数值v与k的按位或结果中不会出现k以为的1就行了，另外上面f[i][j][k]中选出来组成k的这些数也必然符合群演的标准，实际上在这里只需要找出最靠前的x个就行了。

具体来说，同样令g[k]表示所有值为true的f[i][j][k]中最小的i，注意这里j的取值不受限制，但是按上面f的计算方法也不会超过7。g同样可以随着f[i][j][k]的计算来更新。

接下来对于特定的k，若g[k]存在，那么还需要从头到尾遍历一趟nums，若当前的nums[index] | k \= k，就说明找到了一个可用的群演，一旦找齐了x个，就可以更新g[k] \= max(g[k], index+ 1)并退出循环了。若找不齐x个，那么说明凑不齐x个数来构成k，因此需要重置g[k]为None。

按上面的方法得到g和rg后，依然是按照先枚举res再枚举left_part的方式计算最终结果，此时总的时间复杂度就优化到了O(n \* log(ma) \* ma + ma^2)。

另外注意到上面f每一轮的状态只和上一轮有关，因此还可以通过反向遍历j来省去i这一维。

最后附上python代码：

```python
class Solution(object):
    def maxValue(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        one = min(7, k)

        def get(nums):
            f = [[False] * 128 for _ in range(one + 1)]
            f[0][0] = True
            g = [None] * 128

            for index, v in enumerate(nums):
                for state in range(128):
                    for cnt in range(one - 1, -1, -1):
                        if f[cnt][state]:
                            nxt_state = state | v
                            f[cnt + 1][nxt_state] = True
                            if g[nxt_state] is None:
                                g[nxt_state] = index + 1
        
            for state in range(128):
                if g[state] is None:
                    continue
                cnt = 0
                for index, v in enumerate(nums):
                    if (state | v) == state:
                        cnt += 1
                        if cnt == k:
                            g[state] = max(g[state], index + 1)
                            break
            
                if cnt < k:
                    g[state] = None
        
            return g

        
        left = get(nums)
        right = get(nums[::-1])

        for res in range(127, -1, -1):
            for left_part in range(128):
                right_part = res ^ left_part
                if left[left_part] is not None and right[right_part] is not None and left[left_part] + right[right_part] <= len(nums):
                    return res
```
