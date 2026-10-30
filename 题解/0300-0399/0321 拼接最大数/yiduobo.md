---
title: "321. 拼接最大数"
aliases: ["yiduobo的每日leetcode 321.拼接最大数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/159460234"
zhihu_id: "159460234"
zhihu_title: "yiduobo的每日leetcode 321.拼接最大数"
question_id: "321"
question: "拼接最大数"
problem_url: "https://leetcode.cn/problems/create-maximum-number/"
created: "2020-07-14T22:35:21+08:00"
updated: "2020-07-14T22:35:21+08:00"
upvotes: 0
comments: 0
---

# 321. 拼接最大数

> **[yiduobo的每日leetcode 321.拼接最大数](https://zhuanlan.zhihu.com/p/159460234) · 知乎 · 2020-07-14 · 赞同 0**
> 力扣：[321. 拼接最大数](https://leetcode.cn/problems/create-maximum-number/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

321.拼接最大数<https://leetcode-cn.com/problems/create-maximum-number/>

首先可以明确的是，对于最后拼接长答案的两个数组，设其长度分别为k1与k2，那么这两个数组在nums1和nums2中一定是字典序最大的，于是可以从0到k枚举k1，然后通过k - k1计算出k2，之后分别在nums1和nums2中找出对应的数组再进行合并。

对于字典序最大的问题，可以沿用之前316题的单调栈做法。这里从数组nums中选取k个数，可以看成是从数组中删去del_num \= len(nums) - k个数，那么这里单调栈弹栈的条件就变成了，栈顶元素小于当前元素，且del_num大于0。

到了这里，我们已经可以在O(n)的时间内分别找到nums1中长度为k1的最大的数组以及nums2中长度为k2的最大的数组，接下来需要想办法将这两个数组进行合并。在这里可以沿用二路归并的做法，不过有一个特殊情况是当nums1[p] \= nums2[q]时，不能随便任选，例如样例二中的[6，7]和[6，0，4]，两个数组的第一位都是6，而在这里我们必须选择第一个数组中的6，因为第一个数组中6之后的7大于第二个数组中6之后的0。那么对于这种情况，我们需要不断往后迭代p和q直到nums1[p + l]不等于nums2[q + l]，然后根据nums1[p + l]和nums2[q + l]的大小关系来决定应该选择nums1[p]还是nums2[q]。

最后附上python代码：

```python
class Solution(object):
    def maxNumber(self, nums1, nums2, k):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :type k: int
        :rtype: List[int]
        """

        res = []

        for first_len in range(k + 1):
            if k - first_len > len(nums2):
                continue
            if first_len > len(nums1):
                break

            del_num = len(nums1) - first_len
            choose_num1 = []
            for num in nums1:
                while del_num > 0 and choose_num1 and num > choose_num1[-1]:
                    choose_num1.pop()
                    del_num -= 1
                choose_num1.append(num)
            
            del_num = len(nums2) - (k - first_len)
            choose_num2 = []
            for num in nums2:
                while del_num > 0 and choose_num2 and num > choose_num2[-1]:
                    choose_num2.pop()
                    del_num -= 1
                choose_num2.append(num)

            choose_num = []
            pos1 = pos2 = 0

            while pos1 < first_len or pos2 < k - first_len:
                l = 0
                while pos1 + l < first_len and pos2 + l < k - first_len and choose_num1[pos1 + l] == choose_num2[pos2 + l]:
                    l += 1
                if pos1 + l == first_len:
                    choose_num.append(choose_num2[pos2])
                    pos2 += 1
                elif pos2 + l == k - first_len or choose_num1[pos1 + l] > choose_num2[pos2 + l]:
                    choose_num.append(choose_num1[pos1])
                    pos1 += 1
                else:
                    choose_num.append(choose_num2[pos2])
                    pos2 += 1

            if not res:
                res = choose_num[:]
            else:
                flag = False
                for index in range(k):
                    if res[index] > choose_num[index]:
                        break
                    if res[index] < choose_num[index]:
                        flag = True
                        break
                if flag:
                    res = choose_num[:]

        return res
```
