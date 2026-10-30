---
title: "2499. 让数组不相等的最小总代价"
aliases: ["yiduobo的每日leetcode 2499.让数组不相等的最小总代价"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/633784967"
zhihu_id: "633784967"
zhihu_title: "yiduobo的每日leetcode 2499.让数组不相等的最小总代价"
question_id: "2499"
question: "让数组不相等的最小总代价"
problem_url: "https://leetcode.cn/problems/minimum-total-cost-to-make-arrays-unequal/"
difficulty: "Hard"
rating: 2633
created: "2023-06-01T02:16:28+08:00"
updated: "2023-06-01T02:16:28+08:00"
upvotes: 0
comments: 0
---

# 2499. 让数组不相等的最小总代价

> **[yiduobo的每日leetcode 2499.让数组不相等的最小总代价](https://zhuanlan.zhihu.com/p/633784967) · 知乎 · 2023-06-01 · 赞同 0**
> 力扣：[2499. 让数组不相等的最小总代价](https://leetcode.cn/problems/minimum-total-cost-to-make-arrays-unequal/) · Hard · 灵茶山艾府：[思维题 + 分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2499.让数组不相等的最小总代价

[力扣](https://leetcode.cn/problems/minimum-total-cost-to-make-arrays-unequal/)

贪心法的题目。首先一趟遍历，找出所有满足nums1[index]等于nums2[index]的下标index，对于这些位置是必须进行交换的，也就是说本题答案的下限就是这些下标之和。

接下来的问题是在什么情况下可以达到这个下限。很明显，在这里如果能得到一种不将其他位置牵扯进来的交换方案，那么就可以达到这个下限。不妨将问题做一个变形：给出一个数组，每次可以将数组中任意两个数减去1，问是否有一种方案可以使得这个数组变为0。这样变形的理由是将原始需要交换的数出现的次数视为新数组中的数，那么每次选择两个不同的数进行交换，就相当于在新数组中将其中两个数减去1。

对于这个问题，可以参考之前1753题的做法处理

[yiduobo：yiduobo的每日leetcode 1753.移除石子的最大得分](https://zhuanlan.zhihu.com/p/458702976)

对于本题，记需要交换的数字中出现次数最多的数字为check_num，其出现次数为max_cnt，而需要交换次数的总数为swap_cnt，那么此时就只需检测max_cnt是否超过swap_cnt的一半。若没有，那么就可以套用1753题的交换方案，答案就是所有需要交换的数字下标之和，反过来，就需要从一开始并不需要交换的下标中再选择一些来填这个坑。对于后面这种情况，就需要再进行一趟遍历，不断选择nums1[index]与nums2[index]不相等且都不等于check_num的下标index，将index也加入到swap_cnt中，直到max_cnt来到swap_cnt的一半，或者没有可用的下标为止。

最后附上python代码：

```python
class Solution(object):
    def minimumTotalCost(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: int
        """

        cnt = {}
        max_cnt = 0
        check_num = None

        swap_cnt = 0
        swap_cost = 0

        for index, (x, y) in enumerate(zip(nums1, nums2)):
            if x == y:
                cnt[x] = cnt.get(x, 0) + 1
                if cnt[x] > max_cnt:
                    max_cnt = cnt[x]
                    check_num = x
                
                swap_cnt += 1
                swap_cost += index
        
        if max_cnt * 2 <= swap_cnt:
            return swap_cost
        
        for index, (x, y) in enumerate(zip(nums1, nums2)):
            if x != y and x != check_num and y != check_num:
                swap_cost += index
                swap_cnt += 1
                if max_cnt * 2 <= swap_cnt:
                    return swap_cost
        
        return -1
```
