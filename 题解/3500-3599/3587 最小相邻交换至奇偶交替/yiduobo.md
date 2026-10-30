---
title: "3587. 最小相邻交换至奇偶交替"
aliases: ["yiduobo的每日leetcode 3587.最小相邻交换至奇偶交替"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "题单/贪心算法", "题单/贪心算法/八-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1939088531336197612"
zhihu_id: "1939088531336197612"
zhihu_title: "yiduobo的每日leetcode 3587.最小相邻交换至奇偶交替"
question_id: "3587"
question: "最小相邻交换至奇偶交替"
problem_url: "https://leetcode.cn/problems/minimum-adjacent-swaps-to-alternate-parity/"
difficulty: "Medium"
rating: 1548
created: "2025-08-13T22:30:19+08:00"
updated: "2025-08-13T22:30:19+08:00"
upvotes: 0
comments: 0
---

# 3587. 最小相邻交换至奇偶交替

> **[yiduobo的每日leetcode 3587.最小相邻交换至奇偶交替](https://zhuanlan.zhihu.com/p/1939088531336197612) · 知乎 · 2025-08-13 · 赞同 0**
> 力扣：[3587. 最小相邻交换至奇偶交替](https://leetcode.cn/problems/minimum-adjacent-swaps-to-alternate-parity/) · Medium · 灵茶山艾府：[把偶数视作空位，奇数视作汽车，贪心移动（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3587.最小相邻交换至奇偶交替

[3587. 最小相邻交换至奇偶交替 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-adjacent-swaps-to-alternate-parity/description/)

题目给出一个由互不相同的整数组成的数组nums，每次操作，可以交换其中的任意两个相邻元素。问至少需要多少次交换，才能使得nums中所有相邻元素是奇偶交替出现的。如果无法得到奇偶交替出现的nums，那么返回-1。

先一趟遍历，使用两个数组even和odd分别记录nums所有偶数以及所有奇数一开始的下标，那么：

1、当even和odd长度之差大于等于2时：

这种情况下必然无解，直接返回-1

2、当even和odd长度之差等于1时：

这种情况下应该将较长的那个数组中的下标重新分配到偶数下标，也就是0、2、4、...，对于具体的分配方案，在这里不妨记较长的那个数组为target_even，那么在这里就只需按顺序遍历target_even，依次将其中的下标安排到0、2、4、6...即可。

这样做的理由是对于target_even中的一组下标对p和q，若最终将p移动到x，q移动到y，那么在这里必然有x \< y，若x > y，则说明p和q的相对顺序会发生改变，也就是说这两个位置的元素将进行一次交换。但是实际上，本题中只关注元素的奇偶性，而target_even中的所有元素奇偶性相同，因此交换p和q显然是不优的。

基于这一点，最终分配的下标就必须按照target_even中下标的原始顺序，分配到0、2、4、6...，而每次交换的代价则为原始下标与目标下标的差的绝对值，将这些绝对值累加起来即为最终代价。

3、当even和odd长度相等时：

此时既可以将even安排到0、2、4、6...，也可以将odd安排到0、2、4、6...，但具体的分配方案与情况2相同，也必须按照顺序进行填充，因此只需对even进行一趟遍历，考察将其中的下标分配到0、2、4、6...以及1、3、5、7...所需的代价，取其中较小的即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def minSwaps(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        odd = []
        even = []
        for index, v in enumerate(nums):
            if v % 2 == 0:
                even.append(index)
            else:
                odd.append(index)
        
        if abs(len(even) - len(odd)) >= 2:
            return -1
        
        if len(even) == len(odd):
            case_even = 0
            case_odd = 0
            for index in range(len(nums) // 2):
                even_index = index * 2
                odd_index = index * 2 + 1
                case_even += abs(even_index - even[index])
                case_odd += abs(even_index - odd[index])
            
            return min(case_even, case_odd)
        
        target_even, target_odd = even, odd
        if len(target_even) < len(target_odd):
            target_even, target_odd = target_odd, target_even
        res = 0
        for index in range(len(nums) // 2 + 1):
            res += abs(target_even[index] - index * 2)
        
        return res
```
