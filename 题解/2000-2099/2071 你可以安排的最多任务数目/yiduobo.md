---
title: "2071. 你可以安排的最多任务数目"
aliases: ["yiduobo的每日leetcode 2071.你可以安排的最多任务数目"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/binary-search", "题单/二分算法", "题单/常用数据结构", "题单/贪心算法", "题单/二分算法/二-二分答案", "题单/常用数据结构/四-队列", "题单/贪心算法/一-贪心策略"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/515943379"
zhihu_id: "515943379"
zhihu_title: "yiduobo的每日leetcode 2071.你可以安排的最多任务数目"
question_id: "2071"
question: "你可以安排的最多任务数目"
problem_url: "https://leetcode.cn/problems/maximum-number-of-tasks-you-can-assign/"
difficulty: "Hard"
rating: 2648
created: "2022-05-17T22:11:21+08:00"
updated: "2022-05-17T22:11:21+08:00"
upvotes: 0
comments: 0
---

# 2071. 你可以安排的最多任务数目

> **[yiduobo的每日leetcode 2071.你可以安排的最多任务数目](https://zhuanlan.zhihu.com/p/515943379) · 知乎 · 2022-05-17 · 赞同 0**
> 力扣：[2071. 你可以安排的最多任务数目](https://leetcode.cn/problems/maximum-number-of-tasks-you-can-assign/) · Hard · 灵茶山艾府：[二分答案+贪心匹配+双端队列（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2071.你可以安排的最多任务数目

[力扣](https://leetcode.cn/problems/maximum-number-of-tasks-you-can-assign/)

首先，题目只要求完成任务的数目最大，假设最终目标是完成k个任务，那么肯定应该选择最简单的k个任务来做。另外，这个k肯定是越小越容易满足，符合二分的性质，因此在这里可以想将所有任务按需要的力量从小到大进行排序，然后二分答案。对于当前二分到的mid，检测排序后的前mid个任务能否被完成。

由于问题转化成了二分答案后验证的形式，因此对于当前的mid个任务，肯定是要尽力全部完成的，那么显然就应该先考虑完成困难的任务，因此在具体分配任务时应该从第mid - 1个任务开始开始向0倒序遍历，并尝试将当前任务分配出去。若某一时刻无法分配，那么说明mid太大了，需要调整二分上界r，否则调整二分下界l。

接下来考虑如何进行具体的分配。

一个自然的想法是困难的任务分配给力量大的人，但是这里有药丸的存在，且药丸的数目优先，因此这种做法是有问题。

简单举例就是0和1两个工人、T0和T1两个任务，以及一颗药丸。其中0必须借助药丸才能完成T0或者T1，而1则可以在不借助药丸的情况下完成T0，但同样必须借助药丸完成T1。

按上面的思路，先尝试让1去完成T1，发现必须使用药丸。在使用了药丸之后0无法完成T0，最终结果只完成了T1这一个任务。

而正确的做法应该是让1直接去完成T0，让0借助药丸完成T1，从而完成T0和T1两个任务。

可以发现，将困难的任务分配给力量大的人这种做法是有问题的。

注意到分配方案的变数主要来自于药丸，那么不妨转换一下思路，从是否使用药丸的角度出发来考虑。

首先是不使用药丸。如果有若干工人都可以完成最困难的任务，那么对于当前二分的mid而言，这些工人都是等价的，因为这些工人可以完成任意一个剩下的任务，因此这些工人互相之间都是可替代的，那么为了方便起见，不妨就让力量最大的工人去完成最困难的任务。

接下来是使用药丸。设所有可以通过借助药丸完成最困难任务的员工集合为candidate，那么从上面的例子来看，应该尽量留着力量大的工人，因为这些工人可能不借助药丸完成一些其他的任务，那么此时就应该选择candidate中力量最小的工人借助药丸去完成最困难的任务。一个假设是，是否存在某种情况，是通过其他工人借助药丸完成了最困难的任务，而留着candidate中力量最小的工人去完成别的任务？同样是分两种情况讨论。

第一种可能是candidate中力量最小的工人是借助药丸完成的其他任务。实际上，在借助药丸的情况下，candidate中的工人同样是等价的，原因与上面相同，因此在将上面所说的其他工人与candidate中力量最小的工人对调也是不会出现问题的。

第二种可能是candidate中力量最小的工人没有借助药丸完成了其他任务。在这种情况下，上面所说的其他工人力量值大于等于candidate中力量最小的工人，那么很明显其他工人也可以不借助药丸完成对应的任务，因此在这里将二者对调同样不会出现问题。

到了这里就有了两个结论。当存在不需要使用药丸就可以完成最困难任务的工人时，可以选择力量最大的工人去完成任务。当存在需要使用药丸才能完成最困难任务的工人时，可以选择力量最小的工人去完成任务。

那么问题又来了，对于上面这两部分候选集，应该优先选择哪个部分呢？很明显就应该选择直接让力量最大的工人不借助药丸去完成最困难的任务，将药丸省下来。因为完全有可能出现candidate中力量最小的工人也通过自己的实力在不借助药丸的情况下完成某个任务，将药丸留给了其他力量更小的工人使用。

到了这里，就有了一种分配方案。

从mid - 1到0倒序遍历按困难度排序后的每个任务，对于当前任务，如果剩余工人中力量最大的工人可以直接完成，那么就将其分配给这个工人，否则选择可以借助药丸完成该任务的工人中力量最小的工人。乍一看又是一个区间最值问题，但是在这里同样可以利用单调性。

将工人按力量值从大到小排序后，随着任务的向前推荐，需求的力量值是越来越小的，换言之可以借助药丸完成这个任务的工人也是越来越多的，这是一个单调不减的过程，那么很自然想到使用栈或者队列来保存当前的candidate，而candidate中力量最小的工人必然位于栈顶或者队尾。

另一方面，除了找出candidate中力量最小的工人外，还需要优先找出剩余工人中力量最大的工人。力量最大的工人显然也是candidate中的一员，由于单调性，那么其必然位于栈底或者队首。

由于需要选择这两类工人，在这里采用双端队列而不是栈显然是更好的做法。

于是现在的做法就是对于当前的任务，首先在上一轮的基础上将新增的可以通过药丸完成任务的工人加入到队尾，接下来判断队首的工人能否不借助药丸完成任务。若可以，那么让队首工人完成该任务，将其弹出，否则就让队尾工人借助药物完成该任务，将其弹出。

若在这个过程中队列为空，或者选择队尾工人完成任务却发现药丸已经用完了，那么说明无法完成当前的任务。

最后还有一点的是本题同样需要注意二分的上下界。当可以完成mid个任务时，二分会将左边界l移动到mid，若不行，则会将右边界移动到mid - 1。为了避免边界不移动的情况，此时计算mid必须使用(l + r + 1) / 2而不是常规的(l + r) / 2。

最后附上python代码：

```python
class Solution(object):
    def maxTaskAssign(self, tasks, workers, pills, strength):
        """
        :type tasks: List[int]
        :type workers: List[int]
        :type pills: int
        :type strength: int
        :rtype: int
        """

        sorted_tasks = sorted(tasks)
        sorted_workers = sorted(workers, reverse=True)
        
        def check():
            if mid > len(sorted_workers):
                return False

            q = []
            l = 0
            r = 0
            p = 0
            cnt = 0
            
            for index in range(mid - 1, -1, -1):
                now_task = sorted_tasks[index]
                while p < len(sorted_workers) and sorted_workers[p] + strength >= now_task:
                    q.append(sorted_workers[p])
                    r += 1
                    p += 1
                
                if l == r:
                    return False
                if q[l] >= now_task:
                    l += 1
                elif cnt == pills:
                    return False
                else:
                    cnt += 1
                    q.pop()
                    r -= 1
            
            return True

        l = 0
        r = len(sorted_tasks)
        while l < r:
            mid = (l + r + 1) >> 1
            if check():
                l = mid
            else:
                r = mid - 1
        
        return l
```
