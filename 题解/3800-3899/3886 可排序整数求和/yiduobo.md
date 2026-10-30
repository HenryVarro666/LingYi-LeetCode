---
title: "3886. 可排序整数求和"
aliases: ["yiduobo的每日leetcode 3886.可排序整数求和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/number-theory", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2022792314016252739"
zhihu_id: "2022792314016252739"
zhihu_title: "yiduobo的每日leetcode 3886.可排序整数求和"
question_id: "3886"
question: "可排序整数求和"
problem_url: "https://leetcode.cn/problems/sum-of-sortable-integers/"
difficulty: "Hard"
rating: 1999
created: "2026-04-01T22:15:07+08:00"
updated: "2026-04-01T22:15:22+08:00"
upvotes: 1
comments: 0
---

# 3886. 可排序整数求和

> **[yiduobo的每日leetcode 3886.可排序整数求和](https://zhuanlan.zhihu.com/p/2022792314016252739) · 知乎 · 2026-04-01 · 赞同 1**
> 力扣：[3886. 可排序整数求和](https://leetcode.cn/problems/sum-of-sortable-integers/) · Hard · 灵茶山艾府：[预处理 + 分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3886.可排序整数求和

<https://leetcode.cn/problems/sum-of-sortable-integers/description/>

题目给出一个长度为n的整数数组nums。

若一个整数k满足以下条件，则将其称为可排序整数：k是n的因数，且可以通过依次执行一下操作将nums排序为非递减顺序：

- 将nums划分为若干个长度为k的连续子数组
- 独立地对每个子数组进行循环移动(左移或者右移任意次数)

返回所有可能的可排序整数k的和。

为了使得最终的数组有序，那么这些子数组就需要满足：

1、每个子数组可以通过左移或者右移操作变成非递减的：

在这里不妨反过来考虑，一个非递减的子数组在经过若干步左移或者右移操作之后会变成什么。

这里有两种情况，第一种是保持不变，也就是说依然是一个非递减的子数组；第二种是某个后缀被移动到前面，这种情况下，满足：

- 子数组由两段单调非递减的子数组构成
- 前半段最小的元素，也就是子数组的首个元素，大于等于后半段最大的元素，也就是子数组的最后一个元素

2、不同子数组在排序后组合到一起，依然是非递减的：

这里就要求前一个子数组中的最大值必须小于等于后一个子数组的最小值

基于以上两点，就可以先一趟遍历，计算出一个数组f，其中f[index]表示从每个下标index开始，下一个不满足非递减的位置。

对于f数组的计算，可以令index从0开始向后遍历。

对于当前的index，令p从index + 1开始向后遍历。

若当前的p满足nums[p] >\= nums[p - 1]，那么就将p向后移动，直到p来到数组末尾，或者不满足nums[p] >\= nums[p - 1]为止。这样一来，从index到p - 1这一段就是非递减的，也就是说这些位置对应的f都是p。

最后，将index迭代到p，寻找下一个非递减数组即可。

得到f数组后，就可以从1开始到sqrt(n)一趟遍历，若当前遍历到的k是n的约数，那么就检测k是否合法。为了方便检测，还需要额外使用一个变量pre_ma记录前一个区间中的最大值，pre_ma初始情况下可以设置为0。

接下来遍历所有子数组的起点，也就是0、k、2k、...，记start和end分别为当前子数组的起点和终点，那么只有当满足一下两个情况之一时，当前划分的前缀才是合法的：

1、f[start] > end，同时nums[start] >\= pre_ma：

根据f数组的定义，从start到f[start] - 1这一段都是非递减的，而f[start] > end，那么就说明start到end这一段也是非递减的，此时只需要满足子数组中的最小值大于等于前一段的最大值，也就是nums[start] >\= pre_ma。

这种情况下，需要将pre_ma更新为nums[end]，因为当前子数组是单调不减的，因此其中的最大值自然就是nums[end]。

2、f\[f\[start\]\] > end，且nums\[end\] \<\= nums\[start\]，同时nums\[f\[start\]\] >\= pre_ma：

第一个条件说明子数组可以划分成了两段非递减的子数组，其中第一段是start到f\[start\] - 1，第二段是f\[start\]到end。第二个条件说明前半段的最小值依然大于等于后半段的最大值。最后，还需要满足子数组中的最小值，也就是后半段的开端，即nums\[f\[start\]\]大于等于上一段的最大值pre_ma。

这种情况下，需要将pre_ma更新为nums[f[start] - 1]，也就是前半段中的最后一个元素。

若不满足以上两种条件之一，说明当前的k不合法。

需要注意的是，若n // k与k不同，那么在检测k之后，还需要检测n // k。

最后附上python代码：

```python
class Solution(object):
    def sortableIntegers(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        f = []
        
        index = 0
        while index < n:
            p = index + 1
            while p < n and nums[p] >= nums[p - 1]:
                p += 1
            f.extend([p] * (p - index))
            index = p

        def check(k):
            pre_ma = 0
            for start in range(0, n, k):
                end = start + k - 1
                if f[start] > end:
                    if nums[start] >= pre_ma:
                        pre_ma = nums[end]
                    else:
                        return False
                
                elif f[f[start]] > end and nums[end] <= nums[start]:
                    if nums[f[start]] >= pre_ma:
                        pre_ma = nums[f[start] - 1]
                    else:
                        return False

                else:
                    return False
            
            return True

        res = 0
        k = 1
        while k * k <= n:
            if n % k == 0:
                if check(k):
                    res += k
                if n // k != k and check(n // k):
                    res += n // k
            k += 1
        
        return res
```
