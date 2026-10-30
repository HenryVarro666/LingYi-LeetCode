---
title: "3267. 统计近似相等数对II"
aliases: ["yiduobo的每日leetcode 3267.统计近似相等数对II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/math", "leetcode/bitmask", "leetcode/sorting", "leetcode/meet-in-the-middle", "leetcode/bao-li", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/常用数据结构/零-常用枚举技巧", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/747786785"
zhihu_id: "747786785"
zhihu_title: "yiduobo的每日leetcode 3267.统计近似相等数对II"
question_id: "3267"
question: "统计近似相等数对 II"
problem_url: "https://leetcode.cn/problems/count-almost-equal-pairs-ii/"
difficulty: "Hard"
rating: 2545
created: "2024-09-29T02:53:57+08:00"
updated: "2024-09-29T02:53:57+08:00"
upvotes: 1
comments: 0
---

# 3267. 统计近似相等数对II

> **[yiduobo的每日leetcode 3267.统计近似相等数对II](https://zhuanlan.zhihu.com/p/747786785) · 知乎 · 2024-09-29 · 赞同 1**
> 力扣：[3267. 统计近似相等数对 II](https://leetcode.cn/problems/count-almost-equal-pairs-ii/) · Hard · 灵茶山艾府：[排序+枚举右维护左+暴力交换（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3267.统计近似相等数对II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/count-almost-equal-pairs-ii/description/)

之前3265题的加强版，本题中可操作的次数变为了两次，而且数据规模略有增大。

按照上一题的处理方法来看，本题需要执行的运算次数大概在5000 \* 15^2 \* 6 \= 6750000左右。这个运算次数比较微妙，做一些适当的常数优化应该就行了。

上面计算式子中的5000表示的数组长度。15^2指的是两次交换需要的循环次数。这里15的由来是i从0遍历到4时，j一共有5 + 4 + 3 + 2 + 1 \= 15种可行的取值。最后的6则是将这个长度为6的数组拼接成数字的开销。

最简单的两个常数优化自然是避免重复交换的出现。即对于单次操作，交换的数位上的数不应该相同；对于两次交换，也不应该将上一次交换的数值换回来。

接下来，对于拼接的开销，在这里可以先提前计算好10的幂次，然后通过对交换数位10的幂次做加减来节省运算次数。例如对于x \= 12345中的3和5进行交换时，相当于将x减去300再减去5，再加上500在加上3，这样一来就不需要循环拼接了。

在这里最好的处理方法应该是在上一题的基础上，检测当前元素x在操作后的所有新元素，而不是只是x自身，与freq中新元素的匹配情况。由于不需要嵌套执行两次操作，因此在时间复杂度方面可以省去一个15。不过由于本题中x和y的匹配只能在答案中计算一次，但是x操作后的新元素可能在freq中命中多次y操作后的新元素，去重方面需要分若干情况讨论，直观感觉上会很麻烦。

实际上，我在加上第一个i和j对应的数值不应该相同的优化后本题就可以通过了，所以后续的我都没加。

最后附上python代码：

```python
class Solution(object):
    def countPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        nums.sort(reverse=True)

        freq = {}
        res = 0

        def get_new_v(v_set):
            new_v_set = set()
            for v in v_set:
                digits = list(str(v))
                for i in range(len(digits) - 1):
                    for j in range(len(digits)):
                        if digits[i] == digits[j]:
                            continue
                        digits[i], digits[j] = digits[j], digits[i]
                        new_v = int(''.join(digits))
                        if new_v not in v_set:
                            new_v_set.add(new_v)
                        digits[i], digits[j] = digits[j], digits[i]
            
            return new_v_set

        for v in nums:
            res += freq.get(v, 0)
            one_step = get_new_v(set([v]))
            one_step.add(v)
            two_step = get_new_v(one_step)
            for new_v in one_step:
                freq[new_v] = freq.get(new_v, 0) + 1
            for new_v in two_step:
                freq[new_v] = freq.get(new_v, 0) + 1
        
        return res
```
