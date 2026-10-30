---
title: "3850. 统计结果等于K的序列数目"
aliases: ["yiduobo的每日leetcode 3850.统计结果等于K的序列数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/recursion", "leetcode/memoization", "leetcode/math", "leetcode/dynamic-programming", "leetcode/number-theory", "题单/链表-二叉树与回溯", "题单/动态规划", "题单/数学算法", "题单/链表-二叉树与回溯/四-回溯", "题单/动态规划/七-其他线性-DP", "题单/数学算法/二-组合数学"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2011495370388173265"
zhihu_id: "2011495370388173265"
zhihu_title: "yiduobo的每日leetcode 3850.统计结果等于K的序列数目"
question_id: "3850"
question: "统计结果等于 K 的序列数目"
problem_url: "https://leetcode.cn/problems/count-sequences-to-k/"
difficulty: "Hard"
rating: 1965
created: "2026-03-03T23:59:25+08:00"
updated: "2026-03-03T23:59:25+08:00"
upvotes: 1
comments: 0
---

# 3850. 统计结果等于K的序列数目

> **[yiduobo的每日leetcode 3850.统计结果等于K的序列数目](https://zhuanlan.zhihu.com/p/2011495370388173265) · 知乎 · 2026-03-03 · 赞同 1**
> 力扣：[3850. 统计结果等于 K 的序列数目](https://leetcode.cn/problems/count-sequences-to-k/) · Hard · 灵茶山艾府：[记忆化搜索：三种写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3850.统计结果等于K的序列数目

<https://leetcode.cn/problems/count-sequences-to-k/description/>

题目给出一个整数数组nums，其长度不超过19，且其中的元素大小在1到6之间。

从初始值val \= 1开始，从左到右处理nums，在每个下标index处，需要选择一下操作之一：

- 将val乘以nums[index]
- 将val除以nums[index]，需要注意这里是有理数除法而不是整除
- 保持val不变

另外给出一个整数k，其大小在1到10^15之间。问有多少种可行的操作方案，使得在处理完所有元素后，val恰好等于k。

题目中k的规模很大，但是nums中元素的取值范围在1到6之间，也就是说最终得到的整数中，仅有2、3、5这三种质因子，因此可以先将k中所有的2、3、5都分离出来，得到一个长度为3的数组need，其中need[0]、need[1]和need[2]分别表示每种因子的数目。

若分离后的k不为1，说明k中还有其他的质因子，那么无论对nums进行什么样的操作，都不可能凭空变出这些其他的质因子，因此最终答案必然为0。

若分离后的k为1，则可以尝试使用动态规划进行求解。令f[index][two][three][five]表示经过index步操作，得到的结果中2、3、5的幂次分别为two、three、five的方案数量，接下来考虑对nums[index]进行的操作，枚举所有的f[index - 1][two][three][five]：

1、如果执行的是乘以nums[index]，那么就有

f\[index\]\[two + cnt\[0\]\]\[three + cnt\[1\]\]\[five + cnt\[2\]\] +\= f\[index - 1\]\[two\]\[three\]\[five\]

2、如果执行的是除以nums[index]，那么就有

f\[index\]\[two - cnt\[0\]\]\[three - cnt\[1\]\]\[five - cnt\[2\]\] +\= f\[index - 1\]\[two\]\[three\]\[five\]

3、如果不执行操作，那么就有

f[index][two][three][five] \= f[index - 1][two][three][five]

计算完成后，最终答案就是f\[-1\]\[need\[0\]\]\[need\[1\]\]\[need\[2\]\]。

在具体实现上，由于会出现负数的下标，修正起来比较麻烦，因此可以改成哈希表来实现，将所有的[two][three][five]都做成三元组(two, three, five)来当做哈希表的key。

另一方面，由于f的每一轮都只与上一轮有关，因此可以使用滚动哈希表来省去index这一维。

最后附上python代码：

```python
class Solution(object):
    def countSequences(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """
        
        need = [0] * 3
        p = [2, 3, 5]
        for index, v in enumerate(p):
            while k % v == 0:
                need[index] += 1
                k //= v
        
        if k != 1:
            return 0

        f = {(0, 0, 0): 1}
        for x in nums:
            g = copy.deepcopy(f)
            cnt = [0] * 3
            for index, v in enumerate(p):
                while x % v == 0:
                    cnt[index] += 1
                    x //= v
            
            for key in g:
                for sign in [-1, 1]:
                    nxt_key = (key[0] + sign * cnt[0], key[1] + sign * cnt[1], key[2] + sign * cnt[2])
                    f[nxt_key] = f.get(nxt_key, 0) + g[key]
        
        return f.get((need[0], need[1], need[2]), 0)
```
