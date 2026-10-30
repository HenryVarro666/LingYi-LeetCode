---
title: "907. 子数组的最小值之和"
aliases: ["yiduobo的每日leetcode 907.子数组的最小值之和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/stack", "leetcode/math", "leetcode/counting", "leetcode/shao-bing", "leetcode/monotonic-stack", "题单/单调栈", "题单/单调栈/三-贡献法"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/354144143"
zhihu_id: "354144143"
zhihu_title: "yiduobo的每日leetcode 907.子数组的最小值之和"
question_id: "907"
question: "子数组的最小值之和"
problem_url: "https://leetcode.cn/problems/sum-of-subarray-minimums/"
difficulty: "Medium"
rating: 1976
created: "2021-03-03T00:16:29+08:00"
updated: "2021-03-03T00:16:29+08:00"
upvotes: 0
comments: 0
---

# 907. 子数组的最小值之和

> **[yiduobo的每日leetcode 907.子数组的最小值之和](https://zhuanlan.zhihu.com/p/354144143) · 知乎 · 2021-03-03 · 赞同 0**
> 力扣：[907. 子数组的最小值之和](https://leetcode.cn/problems/sum-of-subarray-minimums/) · Medium · 灵茶山艾府：[贡献法+单调栈，从三次遍历到一次遍历（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

907.子数组的最小值之和

[力扣](https://leetcode-cn.com/problems/sum-of-subarray-minimums/)

对于这个题目，我们可以先转换一下思路，将计算各个子数组的最小值之和，转变为对于数组中的每个数来说，这个数是多少个子数组的最小值？

例如样例一中[3, 1, 2, 4]：

1、对于3而言，其只是子数组[3]的最小值，仅有1个子数组，因此3为最终答案贡献了3

2、对于1而言，其是子数组[3, 1]、[3, 1, 2]、[3, 1, 2, 4]、[1]、[1, 2]、[1, 2, 4]的最小值，一共有6个子数组，因此1为最终答案贡献了6

3、对于2而言，其实子数组[2]、[2, 4]的最小值，一共有2个子数组，因此2为最终答案贡献了4

4、对于4而言，其只是子数组[4]的最小值，仅有1个子数组，因此4位最终答案贡献了4

综合起来，最终答案就是3 + 6 + 4 + 4 \= 17

于是现在问题就转化成了对于数组中的每个数而言，要如何计算其实多少个子数组的最小值。需要注意的是，这里的最小值在遇到相同数字的时候只能计算一次，因此我们可以默认当两数相同时选择下标较小的那个作为最小值。

对于数组中的某个数arr[index]，设index左侧第一个大于等于arr[index]的下标为l，右侧第一个大于arr[index]的下标为r，那么从l + 1到index - 1这一段可以提供index - 1 - (l + 1) + 1种选择，而index + 1到r - 1这一段可以提供r - 1 - (index + 1) + 1种选择，二者相乘就是以arr[index]为最小值的子数组的数量了。

接下来的问题就是对于arr[index]，如何找到l和r。一个经典的做法是正反两趟扫描，不过我在这里采用的是最小栈的做法。

我们从左往右进行一趟扫描，对于当前的arr[index]，我们是很容易知道l的位置的，但是r的位置还需要继续扫描才能知道。如果我们使用一个栈来维护这些暂时不知道r的位置，那么这个栈就必然是一个单调递减的栈。

接下来对于当前的arr[index]，若arr[index]大于栈顶元素，说明栈顶元素找到了r的位置。若此时栈中有不止一个元素，那么栈顶元素的l就是栈中的倒数第二个元素，否则l就是数组的左边界了。相对应的，此时栈顶元素的r就是当前的index，于是此时可以计算出栈顶元素最后对于答案的贡献，同时将栈顶元素弹出。重复此过程直到栈为空或者栈顶元素小于等于arr[index]。接下来将arr[index]压入栈中即可。

当扫描完成后，栈可能依然非空，即栈中所有元素的r都是数组的右边界，此时逐个将元素从栈中弹出同时计算其对于答案的贡献即可。

最后附上python代码，其中stack中元素的[0]表示的为该元素的数值，[1]表示的则是该元素在arr中的下标位置：

```python
class Solution(object):
    def sumSubarrayMins(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        res = 0
        mod = 10 ** 9 + 7
        stack = []
        for index, num in enumerate(arr):
            while stack and stack[-1][0] > num:
                if len(stack) == 1:
                    l = stack[-1][1] + 1
                else:
                    l = stack[-1][1] - stack[-2][1]
                
                r = index - stack[-1][1]

                res = (res + stack[-1][0] * l * r) % mod
                stack.pop()
            
            stack.append([num, index])

        n = len(arr)
        for index in range(len(stack) - 1, -1, -1):
            if index == 0:
                l = stack[index][1] + 1
            else:
                l = stack[index][1] - stack[index - 1][1]
            
            r = n - stack[index][1]

            res = (res + stack[index][0] * l * r) % mod
        
        return res
```
