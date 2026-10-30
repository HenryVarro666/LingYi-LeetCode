---
title: "3533. 判断连接可整除性"
aliases: ["yiduobo的每日leetcode 3533.判断连接可整除性"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/bit-manipulation", "leetcode/depth-first-search", "leetcode/recursion", "leetcode/sorting", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/动态规划/专题-输出具体方案-打印方案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1905049205938029420"
zhihu_id: "1905049205938029420"
zhihu_title: "yiduobo的每日leetcode 3533.判断连接可整除性"
question_id: "3533"
question: "判断连接可整除性"
problem_url: "https://leetcode.cn/problems/concatenated-divisibility/"
difficulty: "Hard"
rating: 2257
created: "2025-05-15T23:14:46+08:00"
updated: "2025-05-15T23:14:46+08:00"
upvotes: 0
comments: 0
---

# 3533. 判断连接可整除性

> **[yiduobo的每日leetcode 3533.判断连接可整除性](https://zhuanlan.zhihu.com/p/1905049205938029420) · 知乎 · 2025-05-15 · 赞同 0**
> 力扣：[3533. 判断连接可整除性](https://leetcode.cn/problems/concatenated-divisibility/) · Hard · 灵茶山艾府：[全排列暴搜（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3533.判断连接可整除性

[3533. 判断连接可整除性 - 力扣（LeetCode）](https://leetcode.cn/problems/concatenated-divisibility/description/)

题目给出一个正整数数组nums以及一个正整数k，其中nums的长度不超过13，nums中元素的大小不超过10^5，k的大小不超过100。

现在要求将nums中的元素重新排列，使得这些元素按顺序连接后形成的整数可以被k整除，同时这个排列的字典序最小。需要特别注意，本题中是排列的字典序最小，而不是按顺序连接后形成的整数字典序最小，例如样例1中的nums \= [3, 12, 45]，k \= 5，其中[12, 3, 45]以及[3, 12, 45]都是可行的排列，但是[3, 12, 45]的字典序更小。

以题目个数据规模来看，使用状态压缩动态规划是比较合适的。令f[state][x]表示选取state中的元素进行拼接，且拼接得到的整数模k余x时的最小字典序排列，那么对于f[state][x]，可以枚举所有元素的下标index，若state & (1 \<\< index) \=\= 0，说明index这个元素还没有用过，可以尝试将其拼接在整数的前方，那么下一个状态表示nxt_state就是state | (1 \<\< index)。

在这里拼接在前方的理由是计算位数比较方便，因为对于state中的元素，无论具体是如何排列的，这些元素拼接后得到整数的位数都是固定的，在这里可以利用数组length来记录每种state对应的整数位数，在首次遇到length[nxt_state]时，可以通过length[state] + len(str(nums[index]))来更新length[nxt_state]。

将nums\[index\]拼接在前方后，需要重新计算余数nxt_x。由于已经得到了state对应的整数的位数，那么在其前方拼接nums\[index\]相当于加上了nums\[index\] \* 10^length\[state\]，在这里可以提前预处理出所有10的幂对k取模的余数，并记为数组r，其中r\[index\]表示10^index模k的余数，那么nums\[index\] \* 10^length\[state\]模k的余数就可以写作nums\[index\] \* r\[length\[state\]\]，于是就有nxt_x \= (x + nums\[index\] \* r\[length\[state\]\]) % k。

另一方面，下一个状态的排列nxt_list则是\[nums\[index\]\]拼接在f\[state\]\[x\]前方，接下来就可以使用nxt_list来更新f\[nxt_state\]\[nxt_x\]了。

另外，本题需要计算的是字典序最小的排列，那么在这里就可以先将nums从小到大进行排序，接下来依然是按上面的顺序执行动态规划。由于state是按照从小到大的顺序枚举的，那么对于某个状态f[state][x]，其如果有两个可用的两个前置状态f[pre1][x1]以及f[pre2][x2]，且pre1 \< pre2，那么就说明pre2新添加的元素相比pre1新添加的元素的二进制表示更小，换言之就是这个元素是排在nums中更靠前的元素。更进一步的，由于nums已经按从小到大的顺序排序，那么更靠前的元素拼接在排列的前方就可以使得得到的字典序更小。

基于这一点，就可以默认使用最大的可用的前置状态来更新当前状态，没有必要再对于每个f[state][x]维护具体的排列。另外为了构造最终答案，还需要使用两个数组pre以及use分别维护前置状态以及从前置状态到达当前状态使用的元素。在动态规划完成后，从后往前倒推即可得到最终答案。

最后附上python代码：

```python
class Solution(object):
    def concatenatedDivisibility(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        """
        
        tot_length = 0
        str_nums = []
        nums.sort()
        for v in nums:
            str_nums.append(str(v))
            tot_length += len(str(v))

        r = [1 % k]
        for index in range(1, tot_length):
            r.append(r[-1] * 10 % k)
        
        n = len(nums)
        tot_state = (1 << n)
        f = [[False] * k for _ in range(tot_state)]
        use = [[None] * k for _ in range(tot_state)]
        pre = [[None] * k for _ in range(tot_state)]

        length = [None] * tot_state
        f[0][0] = True
        length[0] = 0

        for state in range(tot_state):
            for x in range(k):
                if f[state][x]:
                    for index in range(n):
                        if state & (1 << index) == 0:
                            nxt_state = state | (1 << index)
                            if length[nxt_state] is None:
                                length[nxt_state] = length[state] + len(str_nums[index])
                            
                            nxt_x = (x + r[length[state]] * nums[index]) % k
                            f[nxt_state][nxt_x] = True
                            use[nxt_state][nxt_x] = nums[index]
                            pre[nxt_state][nxt_x] = (state, x)
        
        if not f[-1][0]:
            return []
        
        res = []
        state, x = tot_state - 1, 0
        while state:
            res.append(use[state][x])
            state, x = pre[state][x]
        return res
```
