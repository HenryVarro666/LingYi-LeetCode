---
title: "1007. 行相等的最少多米诺旋转"
aliases: ["yiduobo的每日leetcode 1007.行相等的最少多米诺旋转"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/brainteaser", "题单/贪心算法", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/366763785"
zhihu_id: "366763785"
zhihu_title: "yiduobo的每日leetcode 1007.行相等的最少多米诺旋转"
question_id: "1007"
question: "行相等的最少多米诺旋转"
problem_url: "https://leetcode.cn/problems/minimum-domino-rotations-for-equal-row/"
difficulty: "Medium"
rating: 1541
created: "2021-04-21T22:15:11+08:00"
updated: "2021-04-21T22:15:11+08:00"
upvotes: 0
comments: 0
---

# 1007. 行相等的最少多米诺旋转

> **[yiduobo的每日leetcode 1007.行相等的最少多米诺旋转](https://zhuanlan.zhihu.com/p/366763785) · 知乎 · 2021-04-21 · 赞同 0**
> 力扣：[1007. 行相等的最少多米诺旋转](https://leetcode.cn/problems/minimum-domino-rotations-for-equal-row/) · Medium · 灵茶山艾府：[[灵茶山艾府题解/solutions/1007 行相等的最少多米诺旋转 · 都变成 tops-0- 或者 bottoms-0-（Python-Java-C++-C-Go-JS-Rust）|都变成 tops[0] 或者 bottoms[0]（Python/Java/C++/C/Go/JS/Rust）]]

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

1007.行相等的最少多米诺旋转

[力扣](https://leetcode-cn.com/problems/minimum-domino-rotations-for-equal-row/)

匹配的目标只有A[0]或B[0]，那么可能出现4种情况：

1、A[0]不动，后续的数来匹配A[0]

2、A[0]与B[0]进行翻转，后续的数来匹配老的A[0]

3、B[0]不动，后续的数来匹配B[0]

4、B[0]与A[0]进行翻转，后续的数来匹配老的B[0]

对于这4中情况，其中情况1和情况2是完全对称的。对于情况1而言，就是A[0]之后部分骨牌执行翻转操作。设这些需要翻转的骨牌的下标集合为R_A[0]，那么需要翻转的次数为len(R_A[0])。我们也可以将除了R_A[0]之外的骨牌进行翻转，那么此时就得到了情况2，翻转的次数为n - len(R_A[0]) - both_A[0]。这里的both_A[0]指的是上下部分都等于A[0]的骨牌。无论A[0]是否进行旋转，这块骨牌都不需要进行旋转。

同样地，情况3和情况4也是对称的。

有了上面的结论，我们只需要一趟遍历，判断是否存在合法的R_A[0]或R_B[0]以及各自的大小。若存在合法的R_A[0]，那么匹配A[0]的代价就是

min(len(R_A[0]), n - len(R_A[0]) - both_A[0])

同样地，若存在合法的R_B[0]，那么匹配B[0]的代价则就是

min(len(R_B[0]), n - len(R_B[0]) - both_B[0])

二者再取较小值即为最后的答案

最后附上python代码：

```python
class Solution(object):
    def minDominoRotations(self, A, B):
        """
        :type A: List[int]
        :type B: List[int]
        :rtype: int
        """

        flag_A = flag_B = True
        cnt_A = cnt_B = 0
        both_A = both_B = 0

        for index in range(1, len(A)):
            if flag_A:
                if A[index] == A[0]:
                    if B[index] == A[0]:
                        both_A += 1
                elif B[index] == A[0]:
                    cnt_A += 1
                else:
                    flag_A = False

            if flag_B:
                if B[index] == B[0]:
                    if A[index] == B[0]:
                        both_B += 1
                elif A[index] == B[0]:
                    cnt_B += 1
                else:
                    flag_B = False

        res = len(A) + 1

        if flag_A:
            res = min(res, cnt_A, len(A) - both_A - cnt_A)
        
        if flag_B:
            res = min(res, cnt_B, len(A) - both_B - cnt_B)
        
        if res > len(A):
            res = -1

        return res
```
