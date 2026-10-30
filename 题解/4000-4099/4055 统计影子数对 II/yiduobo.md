---
title: "4055. 统计影子数对II"
aliases: ["yiduobo的每日leetcode 4055.统计影子数对II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/stack", "leetcode/binary-search", "leetcode/divide-and-conquer", "leetcode/sorting", "leetcode/monotonic-stack", "题单/常用数据结构", "题单/常用数据结构/十-CDQ-分治-/-值域分治"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2084054594775167040"
zhihu_id: "2084054594775167040"
zhihu_title: "yiduobo的每日leetcode 4055.统计影子数对II"
question_id: "4055"
question: "统计影子数对 II"
problem_url: "https://leetcode.cn/problems/count-shadow-pairs-ii/"
difficulty: "Hard"
rating: 2631
created: "2026-09-17T23:42:16+08:00"
updated: "2026-09-17T23:42:20+08:00"
upvotes: 2
comments: 0
---

# 4055. 统计影子数对II

> **[yiduobo的每日leetcode 4055.统计影子数对II](https://zhuanlan.zhihu.com/p/2084054594775167040) · 知乎 · 2026-09-17 · 赞同 2**
> 力扣：[4055. 统计影子数对 II](https://leetcode.cn/problems/count-shadow-pairs-ii/) · Hard · 灵茶山艾府：[值域分治 + 单调栈二分（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4055.统计影子数对II

<https://leetcode.cn/problems/count-shadow-pairs-ii/description/>

题目给出一个长度为n的整数数组nums。

若一对下标(i, j)满足i \< j且nums[i] \< nums[j]，同时不存在k满足i \< k \< j且nums[i] \< nums[k] \< nums[j]，那么就称(i, j)为影子对。

问数组中影子对的总数。

本题中破坏影子对成立的nums[k]此时需要考虑nums[i]与nums[j]这两侧的大小关系，因此做法相比之前复杂了很多，那么不妨从简到难来思考。

首先可以明确的是，对于每个左边界值nums[i]，其对应的右边界值必然是单调不增的，因为一旦出现了递增的关系，前面这个较小的右边界值就会成为破坏影子对成立的k。基于这一点，就可以为每个左边界都维护一个右边界的上界，即对于每个下标i，都维护一个upper[i]，那么对于i右侧的某个下标j，若nums[i] \< nums[j] \<\= upper[i]，此时的j就可以与i形成影子对。这种情况下，还需要将upper[i]更新为nums[j]。

到了这里，就得到了一种暴力算法。一趟遍历，对于每个下标i维护一个upper[i]，初始情况下所有的upper[i]都是无穷大。接下来对于当前遍历到的j，若某个i满足nums[i] \< nums[j] \<\= upper[i]，就将upper[i]更新为nums[j]，同时将答案加上1。

以上的算法时间复杂度为O(n^2)，需要想办法进行优化。

---

注意到以上过程中，修正upper是动态的，而左边界nums[i]是静态的，那么在这里就可以先考虑将左边界按大小顺序收拢，那么检测并修改上界就变成对连续区间修改上界的问题。

以样例1为例。对于nums \= \[3,1,4,2,5\]，其对应的数组o \= \[2, 0, 3, 1, 4\]，那么将upper按顺序收集后的数组就是\[upper\[1\], upper\[3\], upper\[0\], upper\[2\], upper\[4\]\]。可以发现，对于任意j，所有小于等于nums\[j\]的元素对应的upper就都落在这个数组的0到o\[j\] - 1之间。

需要注意的是，在遍历到j时，如果还没有遍历到0到o[j] - 1之间的i，那么这个i是无法与j形成影子对的，因此在这里需要将upper全部初始化为-1，表示不可用。这样一来在遍历到j时，由于要找到的是0到o[j] - 1直接大于等于nums[j]的upper，那么等于-1，也就是尚未遍历到的i就不会被计入答案。而在处理完j后，此时再将o[j]对应的upper更新为无穷大，表示当前的j可以作为后续的i来使用。

初始情况下，upper聚集后为[-1, -1, -1, -1, -1]。接下来依次遍历nums。

1、首先是nums[0] \= 3，对应的o[0] \= 2，那么需要检测的就是前两位也就是[-1, -1]，发现无法形成影子对。接下来，需要将o[0] \= 2这一位上的值修正为无穷大，得到的聚集数组就是[-1, -1, ∞, -1, -1]，对应了区间(3, ∞)。

2、接下来是nums[1] \= 1，对应的o[1] \= 0，没有需要检测的上界。接下来需要将o[1] \= 0这一位上的值修正为无穷大，得到的聚集数组就是[∞, -1, ∞, -1, -1]，对应了区间(1, ∞)以及(3, ∞)。

3、接下来是nums[2] \= 4，对应的o[2] \= 3，那么需要检测是就是前三位[∞, -1, ∞]，其中有两个元素都是无穷大，大于4，因此可以形成两组影子对，实际上就是区间(1, ∞)对应的下标对1以及区间(3, ∞)对应的下标对0，分别与2形成的下标对(1, 2)以及(0, 2)。接下来需要将这两个位置对应的upper都修正为4，同时还需要将o[2] \= 3这一位上的值修正为无穷大，得到的聚集数组就是[4, -1, 4, ∞, -1]，对应了区间(1, 4]、(3, 4]以及(4, ∞)。

4、接下来是nums[3] \= 2，对应的o[3] \= 1，那么仅需要检测第一位[4]，可以形成影子对，实际上就是区间(1, 4]对应的下标1与3形成的下标对(1, 3)。接下来需要将1对应的upper修正为2，同时还需要将o[3] \= 1这一位上的值修正为无穷大，得到的聚集数组就是[2, ∞, 4, ∞, -1]，对应了区间(1, 2]、(2, ∞)，(3, 4]、(4, ∞)。值得一提的是，这里的(1, 4]被修正为了(1, 2]，对应了最上面所说的单调不增。

5、最后是nums[4] \= 5，对应的o[4] \= 4，那么需要检测的就是前四位[2, ∞, 4, ∞]，其中的两个无穷大都大于5，可以形成两组影子对，实际上就是区间(2, ∞)对应的下标3与区间(4, ∞)对应的下标2，分别与4形成的下标对(3, 4)与(2, 4)。接下来依然需要进行修正，但是后续没有其他元素了，所以这里就不展开了。

全部计算完成，一共得到了(1, 2)、(0, 2)、(1, 3)、(3, 4)、(2, 4)这五组影子对。

可以发现，到了这里，问题就变成了如何高效计算一个区间内所多少个元素小于等于特定的元素x，同时将这些元素都修改为这个元素x。除此之外，还附带了一个单点修改j的操作。

乍一看上面是一个区间修改以及一个单点修改的问题，应该使用线段树来处理，但是这个区间修改是特殊操作，因为区间中小于等于特定值x的元素不一定连续出现，因此常规线段树是无法处理这个问题的。

为了处理这个问题，可以用到非常有意思的吉司机树，最终的时间复杂度依然是均摊logn。

---

为了处理区间修改，线段树中的每个节点需要维护子树中的最大值first，次大值second以及最大值出现的次数first_cnt。对于依次修改x，可以分为三种情况：

1、x > first：对于这种情况，子树中所有节点值都小于x，因此无事发生，可以直接return

2、first >\= x > second：对于这种情况，子数组所有的first都需要变为x，此时可以利用懒更新的策略，将first置为x就行了。同时，此次修改意味着这first_cnt个first对应的左边界可以与x形成合法数对，因此需要更新答案

3、second >\= x：对于这种情况，需要递归更新左右子树。需要注意在此之前，要先将first下放，用来更新左右子树的first，理由是情况2中的修改可能被懒更新策略拦截在了这一层，因此如果要向下递归更新，必须先将这次修改传递下去。而根据情况2的不等式关系，这个first只需要用来更新子树的first，second就不用管了。这一步的时间复杂度看上去很高，但是使用势能法可以发现均摊是logn的，后续会有详细的说明

---

接下来先说明具体的计算流程。

首先，将数组元素按照大小nums[i]为第一关键字，初始位置i为第二关键字排序，然后依次填充到线段树的叶子节点中。初始情况下，这些节点都处于未激活状态，对应的first和second都是-1。

接下来遍历原数组，对于当前元素v，先找出其在排序后数组中的位置o，以及这是碰到的第几个v，也就是cnt[v]，那么数组中所有严格小于v的元素在线段树中的位置，就是0到o - cnt[v]，也就是说，查询并修改上界的操作就在0到o - cnt[v]这一段中执行。

执行完成后，v自身也将成为可用的左边界，因此需要将线段树中v对应的节点，也就是o这个点的上界修改为无穷大，在这里也可以取max(nums) + 1。修改的方式就是常规线段树的修改，不过在流程中需要记得下放first，然后递归修改完成后需要更新first和second。

---

最后来说明一下时间复杂度为什么是均摊O(logn)。

线段树中的常规操作的复杂度这里就不展开了，着重说明一下为什么递归修改左右子树的均摊复杂度为O(logn)。

直观感觉上，每次上界的调整如果进入了递归的环节，可能会伴随着部分元素被压扁到这个新的上界，使得后续在此递归的机会变少。

严谨的证明，则是令整棵树的势能为，每颗子树中，不同元素的数量之和。那么在初始情况下，即使nums中的元素都互不相同，树中的势能上界也不超过nlogn，因为一共是logn层树，每层的所有子树互不相交且涵盖整个数组，因此单层的势能不超过nums中的元素数量n。

接下来则是考虑修改区间上界与单点修改这两种操作对势能的影响：

1、首先是修改上界。

一次区间修改操作，最多涉及到logn层，每一层则一定是由至多两个边界区间，以及若干个完整覆盖区间构成。

对于边界区间，修改上界操作可能会在区间中引入新的元素，例如区间[3, 1, 3]，修改的对象是后两个元素，新上界为2，那么修改后就应该变为[3, 1, 2]，相当于引入了一个新元素。因此对于边界区间，最多会使得势能上升2 \* logn，也就是区间的数量。

而对于中部区间，修改上界操作则不会使得势能上升，因为新的上界要么不会影响区间的元素，要么会完全替换掉区间内的某个元素，因此势能不变。

综合起来，修改上界操作至多会让势能上升的量级为logn。

2、然后是单点修改。

一次单点修改会影响logn个区间，每个区间都可能因为这次修改新增一个不同的元素，也就是势能上升1，因此单点修改同样至多会让势能上升logn。

根据上面的结论，由于整个流程中，一共n次修改上界，n次单点修改，因此总的势能依然维持在nlogn的量级。

最后再回到递归修改左右子区间上界这里。出现这种情况，意味着新的上界x小于等于second，那么：

1、若x \= second，此时区间中的first将全部替换成second，相当于势能减少1

2、若x \< second，此时区间中的first、second，以及大于x的所有元素将全部替换为x。即使x可能是区间中之前没出现过的元素，但是至少有first与second这两种元素被消灭掉，因此势能同样至少减1

也就是说，递归修改一旦发生，总的势能至少减去1，而势能的上限是nlogn，也就是说递归修改发生的次数的量级不可能超过nlogn，从而得出区间上界修改的复杂度就是均摊logn。这也就是上面直觉中提到的被压扁的严谨的解释。

最后附上python代码：

```python
class Solution(object):
    def shadowPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        sorted_nums = sorted(nums)
        order = {}
        cnt = {}
        for index, v in enumerate(sorted_nums):
            cnt[v] = cnt.get(v, 0) + 1
            order[(v, cnt[v])] = index
        
        first = [-1] * (n * 4)
        first_cnt = [0] * (n * 4)
        second = [-1] * (n * 4)

        def update_first(p):
            if first[p * 2 + 1] > first[p * 2 + 2]:
                first[p] = first[p * 2 + 1]
                first_cnt[p] = first_cnt[p * 2 + 1]
                second[p] = max(first[p * 2 + 2], second[p * 2 + 1])
            
            elif first[p * 2 + 1] < first[p * 2 + 2]:
                first[p] = first[p * 2 + 2]
                first_cnt[p] = first_cnt[p * 2 + 2]
                second[p] = max(first[p * 2 + 1], second[p * 2 + 2])
            
            else:
                first[p] = first[p * 2 + 1]
                first_cnt[p] = first_cnt[p * 2 + 1] + first_cnt[p * 2 + 2]
                second[p] = max(second[p * 2 + 1], second[p * 2 + 2])

        def ch_min(p, left, right, start, end, v):
            if left == start and right == end:
                if first[p] < v:
                    return 0
                if second[p] < v:
                    first[p] = v
                    return first_cnt[p]
            
            first[p * 2 + 1] = min(first[p * 2 + 1], first[p])
            first[p * 2 + 2] = min(first[p * 2 + 2], first[p])
            mid = (left + right) // 2
            if end <= mid:
                pair = ch_min(p * 2 + 1, left, mid, start, end, v)
            elif start > mid:
                pair = ch_min(p * 2 + 2, mid + 1, right, start, end, v)
            else:
                pair = ch_min(p * 2 + 1, left, mid, start, mid, v) + ch_min(p * 2 + 2, mid + 1, right, mid + 1, end, v)
            
            update_first(p)
            return pair

        def update_point(p, left, right, index, v):
            if left == right:
                first[p] = v
                first_cnt[p] = 1
                second[p] = -1
                return
            
            first[p * 2 + 1] = min(first[p * 2 + 1], first[p])
            first[p * 2 + 2] = min(first[p * 2 + 2], first[p])
            mid = (left + right) // 2
            if index <= mid:
                update_point(p * 2 + 1, left, mid, index, v)
            else:
                update_point(p * 2 + 2, mid + 1, right, index, v)
            
            update_first(p)

        cnt = {}
        res = 0
        for v in nums:
            cnt[v] = cnt.get(v, 0) + 1
            o = order[(v, cnt[v])]
            bound = o - cnt[v]
            if bound >= 0:
                res += ch_min(0, 0, n - 1, 0, bound, v)
            
            update_point(0, 0, n - 1, o, sorted_nums[-1] + 1)

        return res
```
