---
title: "2350. 不可能得到的最短骰子序列"
aliases: ["yiduobo的每日leetcode 2350.不可能得到的最短骰子序列"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/561018329"
zhihu_id: "561018329"
zhihu_title: "yiduobo的每日leetcode 2350.不可能得到的最短骰子序列"
question_id: "2350"
question: "不可能得到的最短骰子序列"
problem_url: "https://leetcode.cn/problems/shortest-impossible-sequence-of-rolls/"
difficulty: "Hard"
rating: 1961
created: "2022-09-04T00:31:27+08:00"
updated: "2022-09-04T00:31:27+08:00"
upvotes: 0
comments: 0
---

# 2350. 不可能得到的最短骰子序列

> **[yiduobo的每日leetcode 2350.不可能得到的最短骰子序列](https://zhuanlan.zhihu.com/p/561018329) · 知乎 · 2022-09-04 · 赞同 0**
> 力扣：[2350. 不可能得到的最短骰子序列](https://leetcode.cn/problems/shortest-impossible-sequence-of-rolls/) · Hard · 灵茶山艾府：[贪心及其证明（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2350.不可能得到的最短骰子序列

[力扣](https://leetcode.cn/problems/shortest-impossible-sequence-of-rolls/)

题目要求找出最短的长度，使得rolls中不存在该长度的某个子序列。令f[i]表示包含长度i的所有子序列的最短前缀长度，那么目标就是找出最小的k，使得存在f[k - 1]但不存在f[k]。

不妨从1开始考虑。对于f\[1\]，一共有k种长度为1的子序列，那么这k中子序列第一次出现位置的最大值就是f\[1\]了。换言之，从rolls\[0\]到rolls\[f\[1\]\]这个前缀中包含了所有的k种数字，但是rolls\[0\]到rolls\[f\[1\] - 1\]这个前缀中则缺少了其中某种数字。对于这个问题，可以一趟遍历，使用set记录当前出现过的数字。当某一时刻set中包含了k个数字，当前的下标就是f\[1\]了。

接下来考虑f\[2\]。对于所有长度为2的子序列而言，其第一次出现位置最靠后的那个子序列必然是由rolls\[f\[1\]\]开头的。一个简单的证明是为了得到所有长度为2且以rollsf\[1\]\]开头的子序列，那么在rolls\[f\[1\] + 1\]到rolls\[-1\]之间，1到k必须都出现一次，设这些数字第一次出现的最后一个位置为pos。根据f\[1\]的求解方式可知，在rolls\[0\]到rolls\[f\[1\] - 1\]之间必然出现了1到k中，除rolls\[f\[1\]\]之外的所有数字。那么用这些出现过的数字作为第一位，rolls\[f\[1\] + 1\]到pos之间出现的1到k作为第二位，就可以得到所有除rolls\[f\[1\]\]开头之外的长度为2的子序列了。

可以发现，实际上这里的pos恰好就是要找的f[2]了。

更进一步的，现在已知f[p]，那么f[p + 1]就是rolls[f[p] + 1]到rolls[n - 1]之间，1到k第一次出现位置的最大值。若其中某个数字没有出现过，那么说明f[p + 1]不存在，p + 1就是最终答案，否则就计算得到f[p + 1]，然后继续向后计算。

具体实现上，初始化res \= 1，接下来一趟遍历，使用哈希表记录当前出现过的数字。若某一时刻哈希表的长度为k，就并更新res为res + 1，同时清空哈希表用来进行新一轮的计算。

最后附上python代码：

```python
class Solution(object):
    def shortestSequence(self, rolls, k):
        """
        :type rolls: List[int]
        :type k: int
        :rtype: int
        """

        num_set = set()
        res = 1
        for num in rolls:
            num_set.add(num)
            if len(num_set) == k:
                res += 1
                num_set = set()
        
        return res
```
