---
title: "1186. 删除一次得到子数组最大和"
aliases: ["yiduobo的每日leetcode 1186.删除一次得到子数组最大和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/一-入门-DP", "题单/动态规划/六-状态机-DP", "题单/动态规划/七-其他线性-DP", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/380357681"
zhihu_id: "380357681"
zhihu_title: "yiduobo的每日leetcode 1186.删除一次得到子数组最大和"
question_id: "1186"
question: "删除一次得到子数组最大和"
problem_url: "https://leetcode.cn/problems/maximum-subarray-sum-with-one-deletion/"
difficulty: "Medium"
rating: 1799
created: "2021-06-13T15:09:14+08:00"
updated: "2021-06-13T15:09:14+08:00"
upvotes: 0
comments: 0
---

# 1186. 删除一次得到子数组最大和

> **[yiduobo的每日leetcode 1186.删除一次得到子数组最大和](https://zhuanlan.zhihu.com/p/380357681) · 知乎 · 2021-06-13 · 赞同 0**
> 力扣：[1186. 删除一次得到子数组最大和](https://leetcode.cn/problems/maximum-subarray-sum-with-one-deletion/) · Medium · 灵茶山艾府：[教你一步步思考动态规划：从记忆化搜索到递推（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1186.删除一次得到子数组最大和

[力扣](https://leetcode-cn.com/problems/maximum-subarray-sum-with-one-deletion/)

最大子段和问题的进阶版，可以删除其中一个数字。为了凸显出删除一次这个操作，我们可以令f[i]表示以arr[i]结尾，且没有删除过数字的最大子段和是多少，令g[i]表示以arr[i]结尾，删除过一次数字的最大子段和是多少，这里的删除也可以是删除掉arr[i]本身。

对于f[i]，我们可以在f[i - 1]的基础上加上arr[i]，或者舍去前面的f[i - 1]，只保留arr[i]，那么在这里我们只需判断f[i - 1]是否大于0，若大于则将其保留，否则舍去，那么就有

f[i] \= max(f[i - 1], 0) + arr[i]

对于g[i]，我们可以在g[i - 1]的基础上加上arr[i]，或者舍去arr[i]自身，也就是从f[i - 1]的基础上删去arr[i]，那么就有

g[i] \= max(g[i - 1] + arr[i] , f[i - 1])

一趟遍历计算出所有的f和g，取其中的最大值即为最终答案。

另外，注意到这里的f和g都只与上一轮的状态有关，那么我们可以通过先更新g，然后更新f的方式滚动起来，省略掉一维。

最后附上python代码：

```python
class Solution(object):
    def maximumSum(self, arr):
        """
        :type arr: List[int]
        :rtype: int
        """

        f = res = arr[0]
        g = 0
        for num in arr[1:]:
            g = max(g + num, f)
            f = max(f, 0) + num
            res = max(res, f, g)
        
        return res
```
