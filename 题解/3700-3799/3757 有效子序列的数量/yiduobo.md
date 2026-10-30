---
title: "3757. 有效子序列的数量"
aliases: ["yiduobo的每日leetcode 3757.有效子序列的数量"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/math", "leetcode/dynamic-programming", "leetcode/combinatorics", "题单/动态规划", "题单/数学算法", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1976053960189161764"
zhihu_id: "1976053960189161764"
zhihu_title: "yiduobo的每日leetcode 3757.有效子序列的数量"
question_id: "3757"
question: "有效子序列的数量"
problem_url: "https://leetcode.cn/problems/number-of-effective-subsequences/"
difficulty: "Hard"
rating: 2519
created: "2025-11-25T23:27:49+08:00"
updated: "2025-11-25T23:27:56+08:00"
upvotes: 0
comments: 0
---

# 3757. 有效子序列的数量

> **[yiduobo的每日leetcode 3757.有效子序列的数量](https://zhuanlan.zhihu.com/p/1976053960189161764) · 知乎 · 2025-11-25 · 赞同 0**
> 力扣：[3757. 有效子序列的数量](https://leetcode.cn/problems/number-of-effective-subsequences/) · Hard · 灵茶山艾府：[正难则反 + 容斥原理 + SOS DP（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3757.有效子序列的数量

[3757. 有效子序列的数量 - 力扣（LeetCode）](https://leetcode.cn/problems/number-of-effective-subsequences/description/)

题目给出一个整数数组nums，其长度不超过10^5，其中元素的大小在1到10^6之间。另外定义其强度为数组中所有元素的按位或。

若移除某个子序列会使得剩余数组的强度严格减少，那么这个子序列就别称为有效子序列。

问nums中有效子序列的数目。

由于强度是数组中所有元素按位或得到的，那么要让强度减少，就必须让最终按位或结果中的至少一位从1变成0。那么在这里可以先做一个前置处理：对于最终按位或结果中等于0的位，nums中的所有元素在这一位上都必然为0，无需考虑这一位。于是可以先记录一开始按位或结果中所有为0的位，接下来将nums中所有元素的这些位都剔除掉。例如样例3中的[8, 8]，二进制下就是[1000, 1000]，此时的后三位都是可以剔除掉了，此时就相当于在计算[1, 1]对应的结果。

在具体实现上，剔除最好是从高位到低位进行，因为低位如果先剔除掉，高位就需要额外计算偏移了。

不妨设当前剔除的是元素v从低到高的第d位，那么此时的目标就是将d + 1位到最高位与第0到d - 1位拼接起来。对于高位的部分，可以将v先右移d + 1位，然后再左移d位。对于低位的部分，则可以用(1 \<\< d) - 1，也就是二进制下的d个1与v做按位与操作，提取出v最低的d位。最后，将这两个部分按位或起来，就成功剔除掉了第d位。

处理完无用的位之后，接下来需要思考如何计算使得强度减少的方案数。一个直观的思路是先确定从1变0的有哪些位，不妨记为state，那么只需将所有在state对应的位上至少有一个1的元素都去掉，就可以使得强度减少。

在state对应的位上至少有一个1这个说法比较绕，但是仔细想一下就可以知道，实际上这部分元素就是与state的按位与结果非0的元素。记f[state]为这部分元素的数量，那么在选择剔除f[state]对应的所有的元素之后，最终的强度必然会减少，而对于剩余的元素，则可以选择留下或者选择剔除掉，因此一共有2^(n - f[state])种可行的剔除方案。

但是需要注意的是，以上的计算方法可能会出现重复。例如样例1中的[1, 2, 3]，在二进制下为[01, 10, 11]，那么f[1] \= 2，对应的是1和3；f[2] \= 2, 对应的是2和3；f[3] \= 3，对应的是1、2、3。可以发现，当state \= 1时，计算了剔除掉[1, 3]以及[1, 3, 2]这两种情况；当state \= 2时，计算了剔除掉[2, 3]以及[2, 3, 1]这两种情况；当state \= 3时，计算了剔除掉[1, 2, 3]这种情况。其中[1, 2, 3]被计算了多次，是有问题的。

为了处理重复计算的问题，在这里就需要用到容斥原理了。

不妨先从简单的例子看起。令t[x]表示选择x时可以得到的方案数，那么：

只有a和b两种选项时，t[a]包含了t[ab]、t[b]也包含了t[ab]，那么在累加了t[a]以及t[b]之后，t[ab]被额外计算了一次，需要减去t[ab]。

有a、b、c时，t[a]包含了t[ab]、t[ac]、t[abc]，t[b]包含了t[ab]、t[bc]、t[abc]，t[c]包含了t[ac]、t[bc]、t[abc]，因此如果累加了t[a]、t[b]、t[c]，那么t[ab]、t[ac]、t[bc]都被计算了两次，而t[abc]被计算了三次。

此时一种处理方法是减去一次t[ab]、t[ac]、t[bc]，这样一来t[ab]、t[ac]、t[bc]的账就平了，但是需要注意的是，t[ab]、t[ac]、t[bc]都是包含了t[abc]的，因此相当于t[abc]又被减去了三次。可以发现，此时还需要额外计算一次t[abc]，才是正确的结果。

更一般的，不妨设一共有n种选择，那么需要计算这些选择的各种组合的情况。当组合的元素个数为奇数时，应该将对应的结果累加到答案中；反之，则应该将其减去。理由是对于一个由k种选项组合起来的情况，其在计算单个选项时被计算了C(k, 1)次，计算两个选项时又被减去了C(k, 2)次，计算三个选项时被额外计算了C(k, 3)次，以此类推，那么其一共被计算的次数是C(k, 1) - C(k, 2) + C(k, 3) - ...，这里需要根据k的奇偶性才能确定这个式子的形式。

若k为奇数，上面的式子就是

C(k, 1) - C(k ,2) + C(k, 3) - ... - C(k, k - 1)

由于C(k, x) \= C(k, k - x)，因此上面的式子的结果恰好为0，因此在这里就应该额外再计算一次，也就是当k为奇数时，应该将对应的结果累加到答案中。

若k为偶数，上面的式子就是

C(k, 1) - C(k, 2) + C(k, 3) - ... + C(k, k - 1)

对于这个式子，则可以通过C(k, x) \= C(k - 1, x - 1) + C(k - 1, x)来变形，得到

C(k - 1,0) + C(k - 1, 1) - C(k - 1, 1) - C(k - 1, 2) + C(k - 1, 2) + C(k - 1, 3) - ... + C(k - 1, k -2) + C(k - 1, k - 1)

可以发现，除了头部的C(k - 1, 0)以及尾部的C(k - 1, k - 1)之外，其他所有的项都被抵消掉了，也就是说此时被计算了两次，还需要减掉一次，也就是当k为偶数时，应该将对应的结果从答案中减去。

基于上面的结论，在这里就可以将每种位视为一种单独的选项，通过2^(n - f[state])以及容斥原理来计算最终结果了。

例如样例1中的[1, 2, 3]，对应的f[1] \= 2, f[2] \= 2, f[3] \= 3，那么最终答案就是

2^(3 - f[1]) + 2^(3 - f[2]) - 2^(3 - f[3]) \= 3

而样例4中的[2, 2, 1]，二进制表示为[10, 10, 01]，对应的f[1] \= 1, f[2] \= 2, f[3] \= 3，那么最终答案就是

2^(3 - f[1]) + 2^(3 - f[2]) - 2^(3 - f[3]) \= 4 + 2 - 1 \= 5

于是只需从1到2^m - 1遍历所有的state，其中m为nums中最大值的位数。对于当前的state，先统计state中1的数量。若为奇数，则将2^(n - f[state])累加到答案中，否则将2^(n - f[state])从答案中减去即可。

到了这里，还有一个关键问题就是，f的值如何计算。鉴于本题的数据规模，直接暴力计算显然是不行的，而且关于f的定义自身也有重复计算的问题，例如state \= 3时，除了计算1、2这些单纯的位之外，还需要防止3被重复计算。

既然直接计算很困难，那么不妨想办法反向计算。

对于一个state，虽然需要计算的f[state]是与state按位与不为0的元素，但是在这里也可以反过来考虑，有多少元素与state按位与为0，然后用n减去这些与state按位与为0的元素的数量，就是对应的f[state]了。

更进一步的，所有与state按位与为0的元素数目，实际上就是二进制中所有的1都出现在(2^m - 1)^state中的元素的数量。很好理解，就是这些元素中为1的位，只会出现在state为0的那些位上。

而对于这个问题，就好办多了。令g[state]表示被state包含的元素数量，初始情况下，先遍历nums，对于当前遍历到的v，将g[v]加上1。接下来从低位开始向高位遍历，对于当前遍历到的位index，若state中包含1 \<\< index，那么将g[state ^ (1 \<\< index)]累加到g[state]就行了。

需要特别注意的是，这里必须保证外层遍历位，内层遍历state，因为只有在保证了位遍历的顺序的前提下才不会出现重复计算的情况。

得到g[state]后，还原到f就是f[2^m - 1 - state] \= n - g[state]。不过上面在使用容斥原理计算结果时已经用到了2^(n - f[state])，那么在这里索性就不还原出f数组了，直接使用2^g[2^m - 1 - state]参与计算就行了。

最后附上python代码：

```python
class Solution(object):
    def countEffective(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        o = 0
        for v in nums:
            o |= v
        
        m = len(bin(o)[2:])
        zero = []
        for d in range(m - 1, -1, -1):
            if o & (1 << d) == 0:
                zero.append(d)

        for d in zero:
            for index, v in enumerate(nums):
                nums[index] = (v >> (1 + d) << d) | (v & ((1 << d) - 1))

        m = len(bin(max(nums))[2:])
        max_state = (1 << m) - 1
        f = [0] * (max_state + 1)
        p2 = [1]
        mod = 10 ** 9 + 7
        for v in nums:
            f[v] += 1
            p2.append(p2[-1] + p2[-1])
            if p2[-1] >= mod:
                p2[-1] -= mod
        
        mod = 10 ** 9 + 7
        for index in range(m):
            for state in range(1, max_state + 1):
                if state & (1 << index) == (1 << index):
                    f[state] += f[state ^ (1 << index)]
                    if f[state] >= mod:
                        f[state] -= mod
        
        one = [None] * (max_state + 1)
        one[0] = 0
        for state in range(1, max_state + 1):
            lowbit = state & -state
            one[state] = one[state ^ lowbit] + 1

        res = 0
        n = len(nums)
        for state in range(1, max_state + 1):
            rev_state = max_state - state
            if one[state] % 2 == 1:
                delta = 1
            else:
                delta = -1

            res = res + p2[f[rev_state]] * delta
            if res < 0:
                res += mod
            if res >= mod:
                res -= mod
        
        return res
```
