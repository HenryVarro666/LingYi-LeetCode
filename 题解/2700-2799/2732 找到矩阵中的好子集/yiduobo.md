---
title: "2732. 找到矩阵中的好子集"
aliases: ["yiduobo的每日leetcode 2732.找到矩阵中的好子集"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/math", "leetcode/dynamic-programming", "题单/动态规划", "题单/贪心算法", "题单/动态规划/九-状态压缩-DP-状压-DP", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/652581821"
zhihu_id: "652581821"
zhihu_title: "yiduobo的每日leetcode 2732.找到矩阵中的好子集"
question_id: "2732"
question: "找到矩阵中的好子集"
problem_url: "https://leetcode.cn/problems/find-a-good-subset-of-the-matrix/"
difficulty: "Hard"
rating: 2240
created: "2023-08-27T02:39:06+08:00"
updated: "2023-08-27T02:39:06+08:00"
upvotes: 0
comments: 0
---

# 2732. 找到矩阵中的好子集

> **[yiduobo的每日leetcode 2732.找到矩阵中的好子集](https://zhuanlan.zhihu.com/p/652581821) · 知乎 · 2023-08-27 · 赞同 0**
> 力扣：[2732. 找到矩阵中的好子集](https://leetcode.cn/problems/find-a-good-subset-of-the-matrix/) · Hard · 灵茶山艾府：[严格证明+三种计算方法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2732.找到矩阵中的好子集

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/find-a-good-subset-of-the-matrix/description/)

首先，如果存在一个行数为奇数的好子集，那么从这个子集中去掉任意一行，剩下的依然是一个好子集，也就是说如果有解，那么必然存在一个偶数行的解。

接下来，由于题目中的行数很多，因此需要猜测本题符合某种性质，才能想办法构造出答案。一个最直观的猜测就是如果有解，那么必然存在一个只有两行的解，下面给出证明。

可以明确的是，不存在每行都至少有3个1的解。

在极限情况下，每行有5个数，那么一组k行的解中最多只有k / 2 \* 5个1出现，但是若某组解的每行都至少有3个1，那么这k行中就有3k个1，已经超出了上限，因此对于一组解，其中必然存在某一行中1的个数小于等于2个。

接下来，对1的数量不超过2个的行分情况讨论：

1、该行全0：

此时任选另一行与该行组合都是可行解

2、该行只有一个1：

对于这个1所在的列，之前k行形成的这一组解中有k / 2行在该列上都是0，从中任选一行与该行组合都是可行解

3、该行有两个1：

采用上面类似的思路，如果存在这k行中的某一行在这两列上都是0，那么与该行组合就是可行解。

在极限情况下，这两列的单列中最多还可以出现k / 2 - 1个1，两列一起就是k / 2 - 2个1。将这些1分配到除了最开始的这一行的其他行，那么最多只能让k - 2行在这两列中具有至少一个1，也就是说至少存在一行在这两列上都为0，只需将这行与最开始的这一行组合就是可行解

到了这里，就证明了如果有解，那么必然存在一个仅由两行组合的解。由于每一行最多只有2^n种可能的状态，那么只需枚举两种合法的状态组合，然后检测这两种状态是否都在矩阵中出现过即可。

最后附上python代码：

```python
class Solution(object):
    def goodSubsetofBinaryMatrix(self, grid):
        """
        :type grid: List[List[int]]
        :rtype: List[int]
        """

        state_dict = {}
        for index, line in enumerate(grid):
            state = 0
            for v in line:
                state = state * 2 + v
            
            if state == 0:
                return [index]
            
            state_dict[state] = index
        
        for s1 in state_dict:
            for s2 in state_dict:
                if s1 & s2 == 0:
                    return sorted([state_dict[s1], state_dict[s2]])
        
        return []
```
