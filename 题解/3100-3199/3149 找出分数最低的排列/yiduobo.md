---
title: "3149. 找出分数最低的排列"
aliases: ["yiduobo的每日leetcode 3149.找出分数最低的排列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "leetcode/di-tui", "题单/动态规划", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/动态规划/专题-输出具体方案-打印方案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/703742079"
zhihu_id: "703742079"
zhihu_title: "yiduobo的每日leetcode 3149.找出分数最低的排列"
question_id: "3149"
question: "找出分数最低的排列"
problem_url: "https://leetcode.cn/problems/find-the-minimum-cost-array-permutation/"
difficulty: "Hard"
rating: 2642
created: "2024-06-17T02:33:42+08:00"
updated: "2024-06-17T02:33:42+08:00"
upvotes: 0
comments: 0
---

# 3149. 找出分数最低的排列

> **[yiduobo的每日leetcode 3149.找出分数最低的排列](https://zhuanlan.zhihu.com/p/703742079) · 知乎 · 2024-06-17 · 赞同 0**
> 力扣：[3149. 找出分数最低的排列](https://leetcode.cn/problems/find-the-minimum-cost-array-permutation/) · Hard · 灵茶山艾府：[状压 DP：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3149.找出分数最低的排列

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-minimum-cost-array-permutation/description/)

题目给出一个数组nums，其为0到n - 1的一个排列，这里的n满足2 \<\= n \<\= 14。

对于一个排列perm，定义其得分

score(perm) \= |perm\[0\] - nums\[perm\[1\]\]| + |perm\[1\] - nums\[perm\[2\]\]| + ... + |perm\[n - 1\] - nums\[perm\[0\]\]|

现在要求找出分数最小的排列perm，且这个排列的字典序最小。

首先观察score(perm)，可以发现这是一个循环的式子。更具体的说，对于排列perm1 \= \[p\[0\], p\[1\], ..., p\[n - 1\]\]，那么

score(perm1) \= |p\[0\] - nums\[p\[1\]\]| + |p\[1\] - nums\[p\[2\]\]| + ... + |p\[n - 1\] - nums\[p\[0\]\]|

而对于另一个排列perm2 \= \[p\[1\], p\[2\], ..., p\[n - 1\], p\[0\]\]，其得分

score(perm2) \= |p\[1\] - nums\[p\[2\]\]| + |p\[2\] - nums\[p\[3\]\]| + ... + |p\[0\] - nums\[p\[1\]\]|

可以发现，此时的score(perm1) \= score(perm2)。换言之，对于一个排列perm，其元素循环位移后得到的新排列得分与perm完全相同。

注意到题目要求最终答案的字典序最小，那么对于任意一个得分最小的排列，都可以通过循环位移将0移动到排列的头部，也就是说最终答案必然是以0开头的一个排列。

确定了答案的头部值为0，接下来需要确定排列中其他元素的值。题目中n的数据规模很小，可以考虑使用状态压缩动态规划进行求解。在这里需要特别注意的是，除了得分最小之外，题目还要求字典序最小，那么在这里就需要使用一个数组记录每个状态的前一个状态是什么。

在具体实现上，如果不想实时保存当前状态对应的排列，就需要从后往前倒推计算，每一轮都按照从0到n - 1的顺序枚举当前的数是多少。这样做可以保证字典序最小的原理与基数排序的原理相同，在排序时先对比低位再对比高位，这样一来高位对最终结果顺序的影响就必低位要高；而对于本题，先确定排列中靠后的元素，再确定排列中靠前的元素，就可以保证得到的结果是靠前元素较小的排列，也就是字典序最小的排列。

令f[state][last]表示当前已经使用state中的元素填充排列的前缀，且最后一个元素为last时，使用其他元素填充完整个排列可以得到的最小分数是多少，nxt[state][last]则表示f[state][last]取最优解时选择的下一个元素是什么。那么对于f[state][last]：

1、若state已经等于2^n - 1：

说明此时已经填充完整个排列，但是此时还需要把score的最后一项容纳进来，因此就有f[state][last] \= abs(last - nums[0])。

2、对于其他情况：

此时则需要从0到n - 1枚举下一个填充的元素index。

若index没有被使用过，即state & (1 \<\< index) \= 0，那么就可以尝试将index加入进来，此时的总代价

v \= f[state | (1 \<\< index)][index] + abs(last - nums[index])

若v小于当前的f[state][last]，那么就需要将f[state][last]更新为v，同时将nxt[state][last]设置为index。

具体实现上，使用记忆化搜索会比较方便，入口则为state \= 1, last \= 0。计算完成后，只需初始化答案排列为[0]，接下来从(state \= 1, last \= 0)开始，不断将当前的nxt[state][last]加入到答案中，同时使用其更新state和last，直到nxt[state][last]为空，就可以得到答案对应的排列。

最后附上python代码：

```python
class Solution(object):
    def findPermutation(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """

        n = len(nums)
        max_state = (1 << n) - 1
        f = [[None] * n for _ in range(max_state + 1)]
        nxt = [[None] * n for _ in range(max_state + 1)]

        def calc(state, last):
            if f[state][last] is None:
                if state == max_state:
                    f[state][last] = abs(last - nums[0])
                else:
                    for index in range(n):
                        if (state & (1 << index)) == 0:
                            v = calc(state | (1 << index), index) + abs(last - nums[index])
                            if f[state][last] is None or v < f[state][last]:
                                f[state][last] = v
                                nxt[state][last] = index
            
            return f[state][last]
        
        calc(1, 0)
        res = [0]
        state = 1
        last = 0
        while nxt[state][last] is not None:
            res.append(nxt[state][last])
            nxt_state = state | (1 << nxt[state][last])
            last = nxt[state][last]
            state = nxt_state
        
        return res
```
