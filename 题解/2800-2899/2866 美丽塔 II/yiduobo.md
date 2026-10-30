---
title: "2866. 美丽塔II"
aliases: ["yiduobo的每日leetcode 2866.美丽塔II"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/monotonic-stack", "题单/动态规划", "题单/单调栈", "题单/动态规划/十一-优化-DP", "题单/单调栈/一-单调栈"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/661904260"
zhihu_id: "661904260"
zhihu_title: "yiduobo的每日leetcode 2866.美丽塔II"
question_id: "2866"
question: "美丽塔 II"
problem_url: "https://leetcode.cn/problems/beautiful-towers-ii/"
difficulty: "Medium"
rating: 2072
created: "2023-10-18T03:27:02+08:00"
updated: "2023-10-18T03:27:02+08:00"
upvotes: 0
comments: 0
---

# 2866. 美丽塔II

> **[yiduobo的每日leetcode 2866.美丽塔II](https://zhuanlan.zhihu.com/p/661904260) · 知乎 · 2023-10-18 · 赞同 0**
> 力扣：[2866. 美丽塔 II](https://leetcode.cn/problems/beautiful-towers-ii/) · Medium · 灵茶山艾府：[前后缀分解+单调栈（附题单！）Python/Java/C++/Go](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2866.美丽塔II

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/beautiful-towers-ii/)

上一题的强化版。由于本题的数据规模增大，如果想继续使用枚举山峰下标的做法，那么就不能再通过枚举来计算两侧山坡上的数值之和，而是需要提前预处理出前缀和后缀数组prefix以及suffix，其中prefix[index]和suffix[index]分别表示以下标index结尾的单调不减的前缀的最大和，以及以下标index开头的单调不增的后缀的最大和，那么当选择index作为山峰时，其左侧下山路径的最大和就是prefix[index] - maxHeight[index]，而右侧下山路径的最大和则是suffix[index] - maxHeight[index]，从而得到最终的和为prefix[index] + suffix[index] - maxHeight[index]。

到了这里，问题就变成了如何求解prefix以及suffix。由于二者的求解方法是对称的，因此在这里依然以左侧的下山路径举例。

注意到山坡路径的高度是单调的，而与单调性联系比较多的是栈，那么在这里就可以考虑使用栈来进行优化。使用一个栈维护当前每个已经遍历过的下标的最终高度，那么这个栈必然是单调不减的，接下来对于maxHeight[index]。

若栈为空或者maxHeight[index]大于等于栈顶的高度，那么就可以直接将其加入到路径中，此时就有prefix[index] \= prefix[index - 1] + maxHeight[index]，同时将maxHeight[index]压入栈中。

反过来则相对比较复杂。为了使得maxHeight[index]可以加入到路径中，就必须要求其左侧所有最终高度大于maxHeight[index]的位置的最终高度调整为maxHeight[index]。由于已经用单调栈储存了之前所有位置的最终高度，寻找超标高度的下标是比较好处理的，不断对比栈顶元素和maxHeight[index]的大小，将大于maxHeight[index]的元素弹出并更新高度和就行了。不过在这里如果逐个再将其修正后的高度重新添加回来，这就是一个O(n^2)的预处理了，没有起到任何优化的效果。

注意到这些被弹出的位置的最终高度值都将等于maxHeight\[index\]，那么在这里就可以将单调栈记录的内容从每个位置的最终高度调整为所有从未修改过高度的位置的下标，也就是说对于stack\[-j\]以及stack\[-j - 1\]，从stack\[-j\] + 1到stack\[-j - 1\]这一段下标位置的高度都是maxHeight\[stack\[-j\]\]。根据这一点，在完成弹栈操作之后，此时的prefix\[index\]就应该等于prefix\[stack\[-1\]\] + (index - (stack\[-1\] + 1) +1) \* maxHeight\[index\]，也就是从stack\[-1\] + 1这一段到index这一段的最终高度都调整为maxHeight\[index\]，然后再将index压入栈中。

这样一来，就可以保证每个下标进出栈的次数最多只有一次，从而在O(n)的时间内完成预处理。

最后附上python代码：

```python
class Solution(object):
    def maximumSumOfHeights(self, maxHeights):
        """
        :type maxHeights: List[int]
        :rtype: int
        """

        n = len(maxHeights)

        prefix = [maxHeights[0]]
        stack = [0]
        s = maxHeights[0]
        for index in range(1, n):
            while stack and maxHeights[stack[-1]] > maxHeights[index]:
                right = stack.pop()
                if stack:
                    left = stack[-1]
                else:
                    left = -1
                
                s -= maxHeights[right] * (right - left)
            
            if stack:
                left = stack[-1]
            else:
                left = -1
            
            s += (index - left) * maxHeights[index]
            stack.append(index)
            prefix.append(s)
        
        suffix = [maxHeights[n - 1]]
        stack = [n - 1]
        s = maxHeights[n - 1]
        for index in range(n - 2, -1, -1):
            while stack and maxHeights[stack[-1]] > maxHeights[index]:
                left = stack.pop()
                if stack:
                    right = stack[-1]
                else:
                    right = n
                
                s -= maxHeights[left] * (right - left)

            if stack:
                right = stack[-1]
            else:
                right = n

            s += (right - index) * maxHeights[index]
            stack.append(index)
            suffix.append(s)
        
        suffix.reverse()

        res = 0
        for index in range(n):
            res = max(res, prefix[index] + suffix[index] - maxHeights[index])
        
        return res
```
