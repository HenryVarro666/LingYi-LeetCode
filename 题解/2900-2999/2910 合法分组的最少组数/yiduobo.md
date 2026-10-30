---
title: "2910. 合法分组的最少组数"
aliases: ["yiduobo的每日leetcode 2910.合法分组的最少组数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/hash-table", "leetcode/enumeration", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/664215380"
zhihu_id: "664215380"
zhihu_title: "yiduobo的每日leetcode 2910.合法分组的最少组数"
question_id: "2910"
question: "合法分组的最少组数"
problem_url: "https://leetcode.cn/problems/minimum-number-of-groups-to-create-a-valid-assignment/"
difficulty: "Medium"
rating: 2132
created: "2023-10-31T04:34:36+08:00"
updated: "2023-10-31T04:34:36+08:00"
upvotes: 0
comments: 0
---

# 2910. 合法分组的最少组数

> **[yiduobo的每日leetcode 2910.合法分组的最少组数](https://zhuanlan.zhihu.com/p/664215380) · 知乎 · 2023-10-31 · 赞同 0**
> 力扣：[2910. 合法分组的最少组数](https://leetcode.cn/problems/minimum-number-of-groups-to-create-a-valid-assignment/) · Medium · 灵茶山艾府：[本题最简单写法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2910.合法分组的最少组数

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/minimum-number-of-groups-to-create-a-valid-assignment/description/)

题目要求分组的数量最少，那么实际上就是要找出一个最大的group_len，问是否能将每种数分为大小为group_len或者group_len - 1的组。

首先可以明确的是，group_len的最大值ma是每种数出现次数的最小值加1，因为更大的话出现次数最少的数就没法分了。得到这个最大值后，就可以从这个最大值开始逐个向下枚举，检测当前枚举到的group_len是否可行。

对于当前枚举到的group_len，不妨考虑如何用这个大小对出现了cnt次的某个数进行分组。

分组的组数group_cnt为cnt / group_len，而剩下的数的个数则为rest_cnt则是group_cnt % group_len。

若这里的rest_cnt不为0，则需要想办法将其补充到group_len - 1的大小形成新的组，否则就无法按照group_len来进行分组，那么需要补充的数need就是group_len - 1 - rest_cnt，而补充的方法则只能从之前的group_cnt个组中的某些组中抽调1个数出来补到该组，因此就需要满足need \<\= group_cnt，否则就没有足够的1让rest_cnt补足到group_len - 1。

当确定了可用的group_len之后，则只需将每个数计算得到的group_cnt以及是否需要额外补充一组累加到答案中即可。可以明确的是，2一定是一个可行的group_len，因此在这里无需考虑无解的情况。

另外需要说明的是，本题的实现虽然看上去是O(n^2)的，但是由于每种数出现的次数都大于等于ma，因此对于每种group_len只需枚举n / ma种不同的数，而单个数校验的时间为O(1)，因此总的时间复杂度还是O(n)。

最后附上python代码：

```python
class Solution(object):
    def minGroupsForValidAssignment(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        cnt = {}
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
        
        group_len = min(cnt.values()) + 1
        while group_len > 1:
            flag = True
            res = 0
            for v in cnt:
                group_cnt = cnt[v] / group_len
                res += group_cnt

                rest_cnt = cnt[v] % group_len
                if rest_cnt > 0:
                    need = group_len - 1 - rest_cnt
                    if need > group_cnt:
                        flag = False
                        break
                    res += 1
                
            if flag:
                break
            
            group_len -= 1
        
        return res
```
