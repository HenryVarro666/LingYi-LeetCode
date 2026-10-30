---
title: "1871. 跳跃游戏VII"
aliases: ["yiduobo的每日leetcode 1871.跳跃游戏VII"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/dynamic-programming", "leetcode/prefix-sum", "题单/滑动窗口与双指针", "题单/常用数据结构", "题单/动态规划", "题单/滑动窗口与双指针/三-单序列双指针", "题单/常用数据结构/二-差分", "题单/动态规划/十一-优化-DP", "题单/动态规划/专题-跳跃游戏"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/474961276"
zhihu_id: "474961276"
zhihu_title: "yiduobo的每日leetcode 1871.跳跃游戏VII"
question_id: "1871"
question: "跳跃游戏 VII"
problem_url: "https://leetcode.cn/problems/jump-game-vii/"
difficulty: "Medium"
rating: 1896
created: "2022-03-02T23:20:12+08:00"
updated: "2022-03-02T23:20:13+08:00"
upvotes: 0
comments: 0
---

# 1871. 跳跃游戏VII

> **[yiduobo的每日leetcode 1871.跳跃游戏VII](https://zhuanlan.zhihu.com/p/474961276) · 知乎 · 2022-03-02 · 赞同 0**
> 力扣：[1871. 跳跃游戏 VII](https://leetcode.cn/problems/jump-game-vii/) · Medium · 灵茶山艾府：[三种方法：DP/差分数组/同向双指针（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1871.跳跃游戏VII

[力扣](https://leetcode-cn.com/problems/jump-game-vii/)

题目存在一个跳跃区间[minJump, maxJump]，那么对于位置index而言，其最远可以从index - maxJump跳过去，最近则可以从index - minJump跳过去。也就是说，若index这个位置为'0'，且[index - maxJump, index - minJump]之间有一个位置是可以到达的话，index这个位置也可以到达。

那么很自然想到动态规划，令f[i]表示能否跳到位置i，那么对于f[i]，只需要检测f[i - maxJump]到f[i - minJump]之间是否有一个为true就行了。

当然，在这里直接枚举这个区间的话时间复杂度太高了，不过注意到这里区间是一个定长的区间，那么就可以使用滑动窗口，随着i的向后移动跟着一起向后移动。使用一个变量cnt表示滑动窗口内f值为true的数量，那么对于f[i]而言，若cnt > 0且当前位置为'0'，那么f[i]就为true，否则就是false。

当处理完f[i]继续向后遍历时，滑动窗口也跟着向右滑动，此时原来的左边界i - maxJump被滑出去了，因此需要根据f[i - maxJump]是否为真来更新cnt。同样的，此时右边界变成了i + 1 - minJump，因此也需要根据f[i + 1 - minJump]是否为真来更新cnt。

而对于边界情况，首先f[0]必然为true，而f[1]到f[minJump - 1]必然都是false，接下来从minJump开始向后遍历求解f，因此cnt的初始值就是f[0]这里提供的1。

最后附上python代码：

```python
class Solution(object):
    def canReach(self, s, minJump, maxJump):
        """
        :type s: str
        :type minJump: int
        :type maxJump: int
        :rtype: bool
        """

        cnt = 1
        f = [True]
        for index in range(1, minJump):
            f.append(False)
        
        n = len(s)
        for index in range(minJump, n):
            if s[index] == '1' or cnt == 0:
                f.append(False)
            else:
                f.append(True)

            if index - maxJump >= 0:
                if f[index - maxJump]:
                    cnt -= 1
            
            if f[index - minJump + 1]:
                cnt += 1

        return f[-1]
```
