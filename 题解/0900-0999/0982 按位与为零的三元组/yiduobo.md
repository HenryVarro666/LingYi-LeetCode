---
title: "982. 按位与为零的三元组"
aliases: ["yiduobo的每日leetcode 982.按位与为零的三元组"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/bit-manipulation", "leetcode/hash-table", "leetcode/enumeration", "题单/位运算", "题单/位运算/九-其他"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/363591953"
zhihu_id: "363591953"
zhihu_title: "yiduobo的每日leetcode 982.按位与为零的三元组"
question_id: "982"
question: "按位与为零的三元组"
problem_url: "https://leetcode.cn/problems/triples-with-bitwise-and-equal-to-zero/"
difficulty: "Hard"
rating: 2085
created: "2021-04-09T18:22:31+08:00"
updated: "2021-04-09T18:22:31+08:00"
upvotes: 0
comments: 0
---

# 982. 按位与为零的三元组

> **[yiduobo的每日leetcode 982.按位与为零的三元组](https://zhuanlan.zhihu.com/p/363591953) · 知乎 · 2021-04-09 · 赞同 0**
> 力扣：[982. 按位与为零的三元组](https://leetcode.cn/problems/triples-with-bitwise-and-equal-to-zero/) · Hard · 灵茶山艾府：[有技巧的枚举 + 常数优化（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

982.按位与为零的三元组

[力扣](https://leetcode-cn.com/problems/triples-with-bitwise-and-equal-to-zero/)

最直观的做法自然直接枚举i、j、k，然判断A[i] & A[j] & A[k]是否等于0，不过时间复杂度显然是无法接受的。

简单的优化也是很容易想到的，先枚举i和j，使用dict记录A[i] & A[j]的结果出现的次数，然后再枚举k，统计哈希表中满足A[k] & key等于0的key对应的value的数量。由于这里最大的数也就65535，那么最坏情况下时间方面可以勉强过关。

注意到这里的操作是&，那么对于A[k] & key这个操作而言，如果需要结果为0，那么对于A[k]二进制表示中为1的位置而言，key二进制表示中对应的位置应该为0，其他的位置上则可以为0或者1。于是我们可以预先计算出一个check_list，具体为计算方法为初始化check_list为[0]，然后从0到15枚举位置index，若当前的1 \<\< index出现在A[k]中，那么就跳过，否则将1 \<\< index与当前check_list中的所有元素相加，然后添加到check_list当中即可。得到check_list之后，只需要枚举check_list中的key而不需要枚举dict中的所有key了。虽然理论上的时间复杂度并不会减少，但是实际上应该可以节省不少不必要的枚举。

最后附上python代码：

```python
class Solution(object):
    def countTriplets(self, A):
        """
        :type A: List[int]
        :rtype: int
        """

        cnt_dict = {}
        for x in A:
            for y in A:
                z = x & y
                cnt_dict[z] = cnt_dict.get(z, 0) + 1
        
        res = 0
        for x in A:
            check_pow = range(16)
            check_list = [0]
            for p in check_pow:
                if x & (1 << p):
                    continue
                check_list.extend([y + (1 << p) for y in check_list])
            
            res += sum([cnt_dict.get(y, 0) for y in check_list])

        return res
```
