---
title: "975. 奇偶跳"
aliases: ["yiduobo的每日leetcode 975.奇偶跳"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/362458787"
zhihu_id: "362458787"
zhihu_title: "yiduobo的每日leetcode 975.奇偶跳"
question_id: "975"
question: "奇偶跳"
problem_url: "https://leetcode.cn/problems/odd-even-jump/"
created: "2021-04-05T20:55:37+08:00"
updated: "2021-04-05T20:55:37+08:00"
upvotes: 0
comments: 0
---

# 975. 奇偶跳

> **[yiduobo的每日leetcode 975.奇偶跳](https://zhuanlan.zhihu.com/p/362458787) · 知乎 · 2021-04-05 · 赞同 0**
> 力扣：[975. 奇偶跳](https://leetcode.cn/problems/odd-even-jump/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

975.奇偶跳

[力扣](https://leetcode-cn.com/problems/odd-even-jump/)

题目看上去很复杂，但是仔细看奇数跳和偶数跳的目标选择方式可以发现，一旦选择了起点，那么整个跳跃的路径都是确定好了的，我们只需要判断出奇数跳和偶数跳时，从每个点起跳的目标点是哪一个。于是问题又转化成了可以使用logn数据结构解决的区间问题。

我在这里采用的是另一种做法，虽然时间复杂度也是O(nlogn)，但是无需用到复杂的数据结构。由于奇数跳和偶数跳仅有符号上的差别，因此这里只介绍奇数跳的处理方法，偶数跳可以如法炮制。

对于某个奇数跳的起点i，其目标j需要满足j > i且A[j] >\= A[i]，同时在A[j]最小的前提下j也要最小。由于这里需要优先满足A[j] >\= A[i]且A[j]最小，因此我们可以先将数组的下标0到n - 1按照其在A中对应的数值大小从小到大进行排序，数值大小相同的则按下标大小排序，得到排序后的下标数组sorted。

接下来从后往前进行一趟扫描，对于当前处理的sorted[i]而言，只有之前已经扫描过的sorted[i + 1]到sorted[n - 1]这些下标才满足数值大小关系，我们需要找到sorted[i + 1]到sorted[n - 1]这些下标当中，满足大于sorted[i]且最小的那个下标是什么。

对于一组sorted\[x\]和sorted\[y\]而言，我们不妨设x \< y，若此时有sorted\[x\] > sorted\[y\]，那么这里就有一个隐藏条件，也就是A\[sorted\[x\]\] \< A\[sorted\[y\]\]，等号在此时是不会成立的，因为在数值相等时是会按照下标排序的。对于所有小于x的下标而言，其目标点必然不可能是sorted\[y\]，证明也很简单。若此时有小于x的i，其对应的sorted\[i\]的目标点是sorted\[y\]，那么就有sorted\[i\] \< sorted\[y\]。但是此时存在x满足

A\[sorted\[i\]\] \<\= A\[sorted\[x\]\] \< A\[sorted\[y\]\]，且

sorted[i] \< sorted[y] \< sorted[x]

那么这里sorted[i]的目标点应该是sorted[x]，产生了矛盾。

有了上面这个结论，我们就可以使用一个单调栈维护所有可能成为答案的sorted[x]，然后对于当前处理的sorted[i]：

1、若栈顶元素小于sorted[i]，就将栈顶元素弹出直到栈为空或者栈顶元素大于sorted[i]。

2、若此时栈不为空，那么说明此时的栈顶元素就是sorted[i]的目标点，使用栈顶元素更新目标点。否则说明sorted[i]无法继续往后跳。

3、最后，将sorted[i]加入栈中然后继续往前扫描。

全部处理完成后，我们就得到了每个点奇数跳的目标next_odd。

同样的方法，我们也可以得到每个点偶数跳的目标next_even，只需要在对下标排序时将数值大小从大到小排序即可。

得到奇数跳和偶数跳的目标之后，我们可以从后往前倒推，使用两个数组odd和even分别表示当前跳为奇数跳和当前条为偶数跳时能否到达终点，那么有初始条件odd[n - 1]和even[n -1]都为true。接下来向前扫描，对于当前位置index而言：

1、若当前跳为奇数跳，那么其将跳到next_odd\[index\]这个位置，此时只需要检测next_odd\[index\]在偶数跳时能否到达终点，也就是even\[next_odd\[index\]\]是否为true

2、同理，若当前条为偶数跳，那么其将跳到next_even\[index\]这个位置，此时只需要检测next_even\[index\]在奇数跳时能否达到终点，也就是odd\[next_even\[index\]\]是否为true

全部处理完成后，even中true的数量即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def oddEvenJumps(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        n = len(arr)
        
        sorted_index = sorted(range(n), key = lambda x:(arr[x], x))
        next_odd = [-1] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and stack[-1] < sorted_index[index]:
                stack.pop()
            
            if stack:
                next_odd[sorted_index[index]] = stack[-1]

            stack.append(sorted_index[index])

        sorted_index = sorted(range(n), key = lambda x:(-arr[x], x))
        next_even = [-1] * n
        stack = []
        for index in range(n - 1, -1, -1):
            while stack and stack[-1] < sorted_index[index]:
                stack.pop()
            
            if stack:
                next_even[sorted_index[index]] = stack[-1]
            
            stack.append(sorted_index[index])

        odd = [False] * n
        even = [False] * n
        odd[-1] = even[-1] = True
        res = 1
        for index in range(n - 2, -1, -1):
            if next_odd[index] != -1 and even[next_odd[index]]:
                odd[index] = True
                res += 1
            if next_even[index] != -1 and odd[next_even[index]]:
                even[index] = True

        return res
```
