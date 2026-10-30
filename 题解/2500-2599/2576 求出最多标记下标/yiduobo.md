---
title: "2576. 找出最多标记下标"
aliases: ["yiduobo的每日leetcode 2576.找出最多标记下标"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/two-pointers", "leetcode/binary-search", "题单/二分算法", "题单/贪心算法", "题单/二分算法/二-二分答案", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/642010547"
zhihu_id: "642010547"
zhihu_title: "yiduobo的每日leetcode 2576.找出最多标记下标"
question_id: "2576"
question: "求出最多标记下标"
problem_url: "https://leetcode.cn/problems/find-the-maximum-number-of-marked-indices/"
difficulty: "Medium"
rating: 1843
created: "2023-07-07T01:21:56+08:00"
updated: "2023-07-08T02:44:45+08:00"
upvotes: 0
comments: 0
---

# 2576. 找出最多标记下标

> **[yiduobo的每日leetcode 2576.找出最多标记下标](https://zhuanlan.zhihu.com/p/642010547) · 知乎 · 2023-07-07 · 赞同 0**
> 力扣：[2576. 求出最多标记下标](https://leetcode.cn/problems/find-the-maximum-number-of-marked-indices/) · Medium · 灵茶山艾府：[两种方法：二分答案/同向双指针+贪心（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2576.找出最多标记下标

[力扣](https://leetcode.cn/problems/find-the-maximum-number-of-marked-indices/)

乍一看感觉是贪心法的题目，但实际上贪心的标准不太好确定。

首先，数组中最小的数必然会作为某个nums[i]被选取，那么对于与其配对的nums[j]，其选取的标准就比较微妙了。

如果考虑选择尽量小的满足条件的nums[j]，那么就可能出现因为此次选择消耗掉了一个nums[i]的备选，从而使得最终结果不是最优。例如数组[1, 2, 3, 4]，对于1，最小的可以与其配对的整数为2，但是这样一来3和4是无法配对的，最优的配对方法应该是1-3、2-4。

反过来，如果考虑选择尽量大的满足条件的nums[j]，那么这显然也是不够优的，因为后续配对中的nums[i]都比本次的nums[i]要大，对nums[j]的大小要求也越大。在本次就将最大的nums[j]使用掉显然是不优的。

直接使用贪心法遇到的瓶颈，需要从另一个角度进行考虑。

可以发现，题目中的最大配对数显然是符合二分的条件的，因此在这里可以考虑二分答案res，将问题转化为检测数组中能否找出res组配对来。

在明确了配对的组数后，就可以使用贪心法了。为了使得配对尽量成功，那么就应该选取最小的res个数作为nums[i]，选取最大的res个数作为nums[j]，而这些数的配对则只需分别按从小到大顺序两两配对就行了。于是只需最开始将nums从小到大进行排序，然后二分答案res。二分的下界显然为0，而上界则为n / 2，因为n个数最多也就形成n / 2组配对。

对于当前二分到的mid，最小的mid个数就是nums[0]到nums[mid - 1]，而最大的mid个数就是nums[-mid]到nums[-1]，其中nums[0]需要与nums[-mid]配对，nums[1]需要与nums[-mid + 1]配对，以此类推。用更一般的写法，就是对于nums[0]到nums[mid - 1]这些数，其中的nums[index]需要尝试与nums[index - mid]配对。若都可以配对成功，那么说明可以达成mid组配对，此时更新下界为mid，否则更新上界为mid - 1。

最后得到配对的数量后，记得乘以2之后再返回，因为题目询问的是参与配对的数的数量。

最后附上python代码：

```python
class Solution(object):
    def maxNumOfMarkedIndices(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        n = len(nums)
        nums.sort()

        left = 0
        right = n / 2
        while left < right:
            mid = (left + right + 1) / 2
            flag = True
            for index in range(mid):
                if nums[index] + nums[index] > nums[index - mid]:
                    flag = False
                    break

            if flag:
                left = mid
            else:
                right = mid - 1
        
        return left + left
```
