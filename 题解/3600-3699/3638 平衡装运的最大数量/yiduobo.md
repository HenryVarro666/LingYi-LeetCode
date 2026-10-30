---
title: "3638. 平衡装运的最大数量"
aliases: ["yiduobo的每日leetcode 3638.平衡装运的最大数量"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1947422357514884494"
zhihu_id: "1947422357514884494"
zhihu_title: "yiduobo的每日leetcode 3638.平衡装运的最大数量"
question_id: "3638"
question: "平衡装运的最大数量"
problem_url: "https://leetcode.cn/problems/maximum-balanced-shipments/"
difficulty: "Medium"
rating: 1463
created: "2025-09-05T22:27:31+08:00"
updated: "2025-09-05T22:27:32+08:00"
upvotes: 0
comments: 0
---

# 3638. 平衡装运的最大数量

> **[yiduobo的每日leetcode 3638.平衡装运的最大数量](https://zhuanlan.zhihu.com/p/1947422357514884494) · 知乎 · 2025-09-05 · 赞同 0**
> 力扣：[3638. 平衡装运的最大数量](https://leetcode.cn/problems/maximum-balanced-shipments/) · Medium · 灵茶山艾府：[脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3638.平衡装运的最大数量

[3638. 平衡装运的最大数量 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-balanced-shipments/)

题目给出一个长度为n的整数数组weight，表示按直线排列的n个包裹的重量。装运定义为包裹的一个连续子数组，若一个装运满足以下条件，则称其为平衡装运：最后一个包裹的重量严格小于该装运中所有包裹的最大重量。现在要求从中选出若干个不重叠的平衡装运，每个包裹只能出现在一次装运中，部分包裹可以不装运。

问可以形成的平衡装运的最大数量。

题目描述绕来绕去，实际上就是要从weight中找出尽可能多的满足最后一个元素小于其中最大值的子数组。对于这个问题，动态规划是很容易想到的。令f[index]表示weight[0]到weight[index]可以形成的最多装运数量，那么对于f[index]，如果选择不装运weight[index]，此时的f[index]就等于f[index - 1]。另一方面，如果要装运weight[index]，那么就应该找到一个满足weight[p] > weight[index]的下标p，此时就有f[index] \= max(f[index], f[p - 1] + 1)。

另一方面，由于f[index]始终由f[index - 1]这个转移途径，那么就说明f数组必然是单调不减的，因此对于f[index] \= max(f[index], f[p - 1] + 1)这种转移途径而言，为了使得f[p - 1]尽可能大，就应该选择最大的满足条件的p，也就是index的上一个大于weight[index]的元素下标p。对于这个问题，则可以利用单调栈进行求解，这样一来就可以在O(n)的时间内得到最终答案了。

更进一步的，对于weight[index]以及其上一个更大的元素下标p，若p和index之间还存在其他元素，那么这些元素必然是小于weight[p]的，也就是说，以weight[p]开头，以weight[p + 1]到weight[index]之间任意元素结尾的子数组都是可行的装运。无论选择其中哪一个，都不会影响到f[index]。基于这一点，就无需使用动态规划了，可以直接贪心求解：一趟遍历，对于当前的weight[index]，若其小于weight[index - 1]，那么就直接将这两个元素形成一组装运；反之，weight[index - 1]不可能越过weight[index]与后面的元素形成装运，因此在这里直接舍弃掉weight[index - 1]就行了。

最后附上python代码：

```python
class Solution(object):
    def maxBalancedShipments(self, weight):
        """
        :type weight: List[int]
        :rtype: int
        """
        
        res = 0
        ma = None
        for w in weight:
            if ma is None or w >= ma:
                ma = w
            else:
                res += 1
                ma = None

        return res
```
