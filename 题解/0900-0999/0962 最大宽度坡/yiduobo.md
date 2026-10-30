---
title: "962. 最大宽度坡"
aliases: ["yiduobo的每日leetcode 962.最大宽度坡"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/361141611"
zhihu_id: "361141611"
zhihu_title: "yiduobo的每日leetcode 962.最大宽度坡"
question_id: "962"
question: "最大宽度坡"
problem_url: "https://leetcode.cn/problems/maximum-width-ramp/"
created: "2021-03-30T22:04:21+08:00"
updated: "2021-03-30T22:04:21+08:00"
upvotes: 0
comments: 2
---

# 962. 最大宽度坡

> **[yiduobo的每日leetcode 962.最大宽度坡](https://zhuanlan.zhihu.com/p/361141611) · 知乎 · 2021-03-30 · 赞同 0**
> 力扣：[962. 最大宽度坡](https://leetcode.cn/problems/maximum-width-ramp/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

962.最大宽度坡

[力扣](https://leetcode-cn.com/problems/maximum-width-ramp/)

朴素的做法是很容易想到的。直接遍历每个A[i]，然后从i + 1开始往后找出所有大于等于A[i]的A[j]，并使用j - i来更新答案即可。

更进一步的，由于这里每个数都不大于50000，因此可以将其转化为典型的动态区间最大值问题，使用log(n)的数据结构来求解。

另外，注意到这里并不需要对于每个A[i]都找到对应A[j]，因此还存在更好的做法。

首先，对于一组A[x]和A[y]，若存在x \< y且A[x] \<\= A[y]，那么A[y]必然不会成为答案中较小的那个数。证明也很简单，不妨设最终答案是由A[y]与A[k]组成的，这里有

k > y且A[k] >\= A[y]

若存在x满足x \< y且A[x] \<\= A[y]，那么必然有

A[x] \<\= A[y] \<\= A[k]

同时还可以通过x \< y得到-x > -y再得到k - x > k - y

也就是说此时选择A[x]与A[k]组成答案是更好的选择

根据上面的结论，我们可以先选出所有较小一侧的候选集。若存在一组A[x]和A[y]，若存在x \< y且A[x] \<\= A[y]，那么就放弃A[y]，也就是说最终我们可以得到一个单调递减的数组L。

接下来，我们还需要确定较大那一侧的位置。一个直观的想法就是从后往前进行枚举。若此时枚举到的A[j]大于等于数组L[-1]，那么对于L[-1]而言，其能形成的最好答案也就是L[-1]与A[j]的组合，因为之后枚举到的位置都要比j要小了。于是此时可以使用A[j]与L[-1]更新答案，同时将L[-1]从数组中移除。

从末尾移除数据，这说明L就是一个单调栈。

于是此时就有了一种做法：

1、维护一个栈stack，然后从头到尾对数组A进行一趟扫描。若此时栈为空或此时栈顶元素大于当前枚举到的元素，则将当前枚举到的元素入栈

2、从尾向头进行一趟扫描，若此时枚举到的元素大于等于栈顶元素，那么使用当前元素与栈顶元素更新答案，同时将栈顶元素弹出。重复此过程直到栈为空或者当前元素小于栈顶元素，此时再继续向前枚举下一个元素。

最后附上python代码：

```python
class Solution(object):
    def maxWidthRamp(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        stack = [0]
        for index in range(1, len(A)):
            if A[index] < A[stack[-1]]:
                stack.append(index)

        res = 0
        for index in range(len(A) - 1, -1, -1):
            while stack and A[stack[-1]] <= A[index]:
                res = max(res, index - stack[-1])
                stack.pop()
            
        return res
```
