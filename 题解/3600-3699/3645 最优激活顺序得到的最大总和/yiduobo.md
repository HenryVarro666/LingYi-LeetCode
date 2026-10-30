---
title: "3645. 最优激活顺序得到的最大总和"
aliases: ["yiduobo的每日leetcode 3645.最优激活顺序得到的最大总和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "leetcode/sorting", "题单/贪心算法", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1948162454744970651"
zhihu_id: "1948162454744970651"
zhihu_title: "yiduobo的每日leetcode 3645.最优激活顺序得到的最大总和"
question_id: "3645"
question: "最优激活顺序得到的最大总和"
problem_url: "https://leetcode.cn/problems/maximum-total-from-optimal-activation-order/"
difficulty: "Medium"
rating: 2019
created: "2025-09-08T21:50:37+08:00"
updated: "2025-09-08T21:50:37+08:00"
upvotes: 0
comments: 0
---

# 3645. 最优激活顺序得到的最大总和

> **[yiduobo的每日leetcode 3645.最优激活顺序得到的最大总和](https://zhuanlan.zhihu.com/p/1948162454744970651) · 知乎 · 2025-09-08 · 赞同 0**
> 力扣：[3645. 最优激活顺序得到的最大总和](https://leetcode.cn/problems/maximum-total-from-optimal-activation-order/) · Medium · 灵茶山艾府：[阅读理解题/脑筋急转弯（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3645.最优激活顺序得到的最大总和

[3645. 最优激活顺序得到的最大总和 - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-total-from-optimal-activation-order/description/)

题目给出两个长度为n的整数数组value和limit。在一开始，所有元素都是非活跃的，可以按照任意顺序激活它们，但是只有当前活跃元素的数量小于limit[index]时，才能激活非活跃的元素index。当激活了index后，需要将value[index]累加到总和当中。另外，若激活了某个元素之后激活元素的数量变为了x，那么所有limit不超过x的元素都将永久变为非活跃状态。

问按照最后顺序激活可以得到的最大总和是多少。

根据题目中关于limit的要求可以得知，激活的顺序应该按limit从小到大进行，因为当同时激活的元素到达一定数量时，limit较小的元素就不再能激活。如果先激活limit较大的元素，limit较小的元素可能就无法再激活了。但是如果先激活limit较小的元素，是不会影响到limit较大的元素的。

另一方面，可以激活的limit值相同的元素也不超过其对应的limit，因此在这里就应该选择value最大的limit个元素。一旦选择的数目达到了limit个，这些元素都将被强制变成永久非激活，不会影响到后续元素的激活。还有一种特殊情况就是当前limit值的元素不足limit个，但是也不影响上面的结果。理由当后续元素激活时，如果激活的元素达到了limit，这些元素也将变为非激活状态，相当于此时只激活了后续的元素。

基于以上两点，就可以将所有元素先按照limit从小到大，按value从大到小进行排序。接下来从1到n遍历所有可能的limit阈值l，同时使用一个变量p记录接下来可以使用元素下标。对于当前遍历到的l，先将p向后移动到limit大于等于l的位置，接下来从p开始，取出最多l个limit恰好等于l的元素，并将其对应的value累加起来。若不足，就有多少算多少。计算完成后，只需继续考虑后续的l即可。

最后附上python代码：

```python
class Solution(object):
    def maxTotal(self, value, limit):
        """
        :type value: List[int]
        :type limit: List[int]
        :rtype: int
        """
        
        info = sorted(zip(value, limit), key=lambda d:(d[1], -d[0]))
        p = 0
        res = 0
        for l in range(1, len(info) + 1):
            while p < len(info) and info[p][1] < l:
                p += 1
            if p == len(info):
                break
            
            cnt = 0
            while cnt < l and p < len(info) and info[p][1] == l:
                res += info[p][0]
                p += 1
                cnt += 1
        
        return res
```
