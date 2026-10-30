---
title: "3942. 排序排列的最少操作数"
aliases: ["yiduobo的每日leetcode 3942.排序排列的最少操作数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2044207375691863998"
zhihu_id: "2044207375691863998"
zhihu_title: "yiduobo的每日leetcode 3942.排序排列的最少操作数"
question_id: "3942"
question: "排序排列的最少操作数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-sort-a-permutation/"
difficulty: "Medium"
rating: 1855
created: "2026-05-31T01:35:06+08:00"
updated: "2026-05-31T01:35:10+08:00"
upvotes: 2
comments: 0
---

# 3942. 排序排列的最少操作数

> **[yiduobo的每日leetcode 3942.排序排列的最少操作数](https://zhuanlan.zhihu.com/p/2044207375691863998) · 知乎 · 2026-05-31 · 赞同 2**
> 力扣：[3942. 排序排列的最少操作数](https://leetcode.cn/problems/minimum-operations-to-sort-a-permutation/) · Medium · 灵茶山艾府：[分类讨论（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3942.排序排列的最少操作数

<https://leetcode.cn/problems/minimum-operations-to-sort-a-permutation/description/>

题目给出一个长度为n的整数数组nums，其中nums是区间0到n - 1中所有数字的一个排列。

现在可以执行以下两种操作：

- 反转整个数组
- 将最左侧元素移动的数组末尾，然后将其他元素整体向左移动一位

问通过以上两种操作将nums变为递增排列的最少操作次数。若无法使得数组递增，则返回-1。

首先考虑特殊情况。当n \= 1时，答案显然为0。

接下来是一般情况。可以明确的是，如果将nums视为首尾相连，那么题目中的两种操作都不会影响到数组元素间的相邻关系，也就是说只有当nums是两段+1的递增、两段-1的递减，或者完整的正序排列、完整的逆序排列之一时，才有可能通过操作变回正序排列。另一方面，反转的次数也不应该超过两次，同时反转次数奇偶不同的状态下，不应该都执行左移操作，因为这样相当于抵消掉了。

为了判断nums属于哪种情况，在这里就可以先对nums进行遍历，找出其中0的下标p，接下来：

1、若p左侧的元素，即nums[(p - 1 + n) % n]为n - 1，那么说明nums只能是两段+1的递增或者完整的正序排列才有解。更进一步的，若p为零，那么就是完全的正序排列，否则就是前p个数为n - p到n - 1递增，后面为0到n - p + 1递增。在这里也可以将这两种情况融合起来，即前p个数为第一段，当p为0时这一段为空，后续剩下的n - p个数为第二段。接下来，需要先检测这两段是否都是+1递增，若不符合，则返回-1，反之基于上面得到的操作的准则，在这里只有两种操作方案，分别是左移p次，或者先反转，然后右移n - p次，再反转，因此答案就是min(p, n - p + 2)。

2、若p右侧的元素，即nums[(p + 1) % n]为n - 1，那么说明nums只能是两段-1的递减或者完整的逆序排列才有解。更进一步的，若p为n - 1，那么就是完全的逆序排列，否则就是前p + 1个数为p到0的递减，后面为n到p的递减。需要注意这里长度与上面有1的差别，理由是0在这种情况下属于前一段，而上面的情况则属于后一段。同样的，在这里拆分为前p + 1个数为第一段，后续剩下的n - p - 1个数为第二段，当p为n - 1时，第一段就是整个数组，而第二段为空。值得一提的是，对于[0, 1]这种边界情况，应该被检测为整段递增，而不是两段递减，因此需要先处理上面那种情况，在处理当前这种情况。接下来，同样是检测这两段是否都是-1递减，若不符合，则返回-1，否则同样是两种操作方案，分别是左移p + 1次然后反转，或者反转后再左移n - p - 1次，因此答案就是min(p + 2, n - p)。

3、若都不符合，说明0和n - 1不相邻，此时直接返回-1。

基于上面的讨论，可以进一步将这两种情况整合到一起。使用一个变量delta来辅助检测，若是递增，则delta为1，否则delta为-1。另外当delta为1时，设置offset为0，否则offset为1，表示第一段长度在递增时应该是p，递减时则为p + 1。

接下来，从0到p - 2 + offset遍历，检测当前元素加上delta是否等于下一个元素，若不符合，则返回-1。

然后，从p + offset到n - 2遍历，同样是检测当前元素加上delta是否等于下一个元素，若不符合，则返回-1。

若两个检测都通过，最后答案就是min(p + 1 - delta, n - p + 1 + delta)。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        if n == 1:
            return 0
        
        p = -1
        for index in range(n):
            if nums[index] == 0:
                p = index
                break

        if nums[(p - 1 + n) % n] == n - 1:
            delta = 1
        elif nums[(p + 1) % n] == n - 1:
            delta = -1
        else:
            return -1

        if delta == 1:
            offset = 0
        else:
            offset = 1

        for index in range(p - 1 + offset):
            if nums[index] + delta != nums[index + 1]:
                return -1
        
        for index in range(p + offset, n - 1):
            if nums[index] + delta != nums[index + 1]:
                return -1

        return min(p + 1 - delta, n - p + 1 + delta)
```
