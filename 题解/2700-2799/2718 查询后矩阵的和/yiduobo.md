---
title: "2718. 查询后矩阵的和"
aliases: ["yiduobo的每日leetcode 2718.查询后矩阵的和"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/651972119"
zhihu_id: "651972119"
zhihu_title: "yiduobo的每日leetcode 2718.查询后矩阵的和"
question_id: "2718"
question: "查询后矩阵的和"
problem_url: "https://leetcode.cn/problems/sum-of-matrix-after-queries/"
difficulty: "Medium"
rating: 1769
created: "2023-08-24T03:06:57+08:00"
updated: "2023-08-24T03:06:57+08:00"
upvotes: 0
comments: 0
---

# 2718. 查询后矩阵的和

> **[yiduobo的每日leetcode 2718.查询后矩阵的和](https://zhuanlan.zhihu.com/p/651972119) · 知乎 · 2023-08-24 · 赞同 0**
> 力扣：[2718. 查询后矩阵的和](https://leetcode.cn/problems/sum-of-matrix-after-queries/) · Medium · 灵茶山艾府：[倒序操作+简洁写法！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

2718.查询后矩阵的和

[力扣（LeetCode）官网 - 全球极客挚爱的技术成长平台](https://leetcode.cn/problems/sum-of-matrix-after-queries/)

题目的数据规模比较大，直接暴力模拟覆盖情况肯定是不行的。注意到本题的操作是覆盖，那么某个位置最终的结果必然是最后一次覆盖的结果，可以考虑倒推求解。另外，每次覆盖的范围是整行或者整列，因此可以尝试按行或者按列来处理，不过在这里就需要处理一个问题，即覆盖某行或者某列时，若该行或该列中存在之后再次被覆盖的单元格，那么本次覆盖的值就不应该计入最终答案中。

对于这个问题也很好求解。对于行的覆盖，若本次覆盖后还出现了k次不同的列覆盖，那么本行中就有k列的值不应该被计算进去，对于列的覆盖也是同样。由于在倒推求解时本来就需要已经覆盖的行和列，那么通过这个信息就可以很方便的知道本次覆盖有多少行或者列应该被计算进去。

最后附上python代码：

```python
class Solution(object):
    def matrixSumQueries(self, n, queries):
        """
        :type n: int
        :type queries: List[List[int]]
        :rtype: int
        """

        vis_r = set()
        vis_c = set()
        res = 0
        for t, index, v in queries[::-1]:
            if t == 0:
                if index in vis_r:
                    continue
                vis_r.add(index)
                res += (n - len(vis_c)) * v
            else:
                if index in vis_c:
                    continue
                vis_c.add(index)
                res += (n - len(vis_r)) * v
        
        return res
```
