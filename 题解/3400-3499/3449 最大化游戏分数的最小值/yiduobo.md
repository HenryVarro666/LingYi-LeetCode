---
title: "3449. 最大化游戏分数的最小值"
aliases: ["yiduobo的每日leetcode 3449.最大化游戏分数的最小值"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/binary-search", "题单/二分算法", "题单/贪心算法", "题单/二分算法/二-二分答案", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1893134919099733211"
zhihu_id: "1893134919099733211"
zhihu_title: "yiduobo的每日leetcode 3449.最大化游戏分数的最小值"
question_id: "3449"
question: "最大化游戏分数的最小值"
problem_url: "https://leetcode.cn/problems/maximize-the-minimum-game-score/"
difficulty: "Hard"
rating: 2748
created: "2025-04-09T03:43:14+08:00"
updated: "2025-04-09T03:43:14+08:00"
upvotes: 1
comments: 0
---

# 3449. 最大化游戏分数的最小值

> **[yiduobo的每日leetcode 3449.最大化游戏分数的最小值](https://zhuanlan.zhihu.com/p/1893134919099733211) · 知乎 · 2025-04-09 · 赞同 1**
> 力扣：[3449. 最大化游戏分数的最小值](https://leetcode.cn/problems/maximize-the-minimum-game-score/) · Hard · 灵茶山艾府：[二分答案+从左到右贪心+正确性解释（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3449.最大化游戏分数的最小值

[3449. 最大化游戏分数的最小值 - 力扣（LeetCode）](https://leetcode.cn/problems/maximize-the-minimum-game-score/)

题目给出一个长度为n的正整数数组points，这里的n在2到50000之间。同时有一个长度为n的数组gameScore，其中gameScore[index]表示第index个游戏的得分。初始状态下gameScore中全为0。

游戏一开始，玩家位于下标-1处，现在给出一个整数m，表示可以执行至多m次操作。每次操作中，可以将下标增加1，也可以将下标减少1。在操作后，需要将当前下标index对应的points[index]添加到gameScore[index]。需要注意，在第一次操作后下标index必须在0到n - 1之间。

问至多m次操作后，gameScore中的最小值最大为多少。

首先考虑特殊情况。

当m \< len(points)时，无论如何移动，index必然时小于len(points) - 1的，因此最终答案必然为0。

接下来考虑一般情况。

对于这类最大化最小值的问题，依然还是尝试采用二分答案的方法来进行处理。二分的下界为min(points)，因为每次都向右移动，至少可以保证gameScore中的所有元素都等于points中对应的元素。二分的上界不太明确，在这里可以设置得大一点，我在这里设置的是min(points) \* m。

接下来对于当前二分到的mid，需要计算出最少需要多少次操作，才能使得gameScore中的所有元素都大于等于mid。

不妨从边界情况开始进行分析。

对于index \= 0这个位置，除了第一次操作将index从-1移动到0之外，如果还想增加gameScore[0]的值，就需要不断将index从0移动到1，再将index从1移动到0。为了使得gameScore[0]大于等于mid，一共需要的移动次数need \= (mid - 1) // points[0] + 1。也就是说，需要走出形如010101...010的操作，其中有need个0，因此一共需要need \* 2 - 1次操作。

这里有一个隐藏条件是除了第一次从-1走到0的操作之外，如果还想走到0，那么就必须先从0走到1，再从1走回到0，一共需要need - 1次0走到1的操作以及need - 1次1走到0的操作。不妨设这些0到1以及1到0的操作分布在整个操作序列中，那么将这些操作全部集中到整个操作序列的头部并不会影响最终需要的操作总次数，因此在这里就可以先执行010101...010这样的操作。

另一方面，在这个过程中到达了下标1一共need - 1次，这些操作对于后续计算走到1的次数是有用的，需要记nxt为need - 1。

接下来考虑index \= 1这个位置。同样是计算need \= (mid - 1) // points[1] + 1，需要分两种情况进行讨论：

1、若need > nxt：

这种情况下，之前对下标0进行操作顺带到达下标1的次数nxt是不够的，还需要到达下标1至少need - nxt次，而这种情况下显然应该往后走，因为再往前走的话走到0的分数就浪费了，但是往后走可以提供一些下标2的分数，也就是说此时的操作应该是1212...121，其中有need - nxt个1，因此一共需要(need - nxt) \* 2 - 1次操作。另一方面，在这里走到了下标2一共need - nxt - 1次，因此在这里应该使用need - nxt - 1来更新nxt。

2、若need \<\= nxt：

此时无需再走到下标1，但是如果1不是gameScore中的最后一个下标，那么就还需要继续向右侧走，因此在这种情况下还需要1次操作，从下标0走到下标1，同时由于没有走到下标2，因此nxt应该更新为0。

反之，若1是最后一个下标，那么此时gameScore中的所有元素都已经大于等于mid，无需再从0走动1。

推广到更一般的情况，对于当前下标index，先通过(mid - 1) // points[index] + 1计算出需要达到index的次数need，接下来对比need与之前到达index的次数nxt。若need > nxt，那么就需要在index和index + 1之间来回走，一共需要(need - nxt) \* 2 - 1次操作，然后将nxt更新为need - nxt - 1，因为在这个过程中走到index + 1一共need - nxt - 1次；反之，若need \<\= nxt，此时只需检测index是否来到了数组末尾，若没有来到数组末尾，则需要一次操作，从index - 1走到index，然后将nxt更新为0。

得到所需的总操作次数后，若其大于m，说明无法使得gameScore中的所有元素大于等于mid，此时应该将二分上界调整为mid - 1，否则可以将二分下界调整为mid。

最后附上python代码：

```python
class Solution(object):
    def maxScore(self, points, m):
        """
        :type points: List[int]
        :type m: int
        :rtype: int
        """
        
        if m < len(points):
            return 0

        mi = min(points)

        left = mi
        right = mi * m
        while left < right:
            mid = (left + right + 1) // 2
            cnt = 0
            nxt = 0

            for index, v in enumerate(points):
                need = (mid - 1) // v + 1
                if need > nxt:
                    cnt += (need - nxt) * 2 - 1
                    nxt = need - nxt - 1
                elif index != len(points) - 1:
                    cnt += 1
                    nxt = 0
            
            if cnt > m:
                right = mid - 1
            else:
                left = mid
        
        return left
```
