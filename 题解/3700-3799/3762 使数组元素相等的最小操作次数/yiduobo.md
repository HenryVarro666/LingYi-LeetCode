---
title: "3762. 使数组元素相等的最小操作次数"
aliases: ["yiduobo的每日leetcode 3762.使数组元素相等的最小操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/greedy", "leetcode/segment-tree", "leetcode/math", "leetcode/number-theory", "题单/常用数据结构", "题单/贪心算法", "题单/常用数据结构/八-树状数组和线段树", "题单/贪心算法/四-数学贪心"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1978557820489188782"
zhihu_id: "1978557820489188782"
zhihu_title: "yiduobo的每日leetcode 3762.使数组元素相等的最小操作次数"
question_id: "3762"
question: "使数组元素相等的最小操作次数"
problem_url: "https://leetcode.cn/problems/minimum-operations-to-equalize-subarrays/"
difficulty: "Hard"
rating: 2497
created: "2025-12-01T20:54:17+08:00"
updated: "2025-12-01T20:54:18+08:00"
upvotes: 1
comments: 0
---

# 3762. 使数组元素相等的最小操作次数

> **[yiduobo的每日leetcode 3762.使数组元素相等的最小操作次数](https://zhuanlan.zhihu.com/p/1978557820489188782) · 知乎 · 2025-12-01 · 赞同 1**
> 力扣：[3762. 使数组元素相等的最小操作次数](https://leetcode.cn/problems/minimum-operations-to-equalize-subarrays/) · Hard · 灵茶山艾府：[中位数贪心 + 可持久化线段树（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3762.使数组元素相等的最小操作次数

[3762. 使数组元素相等的最小操作次数 - 力扣（LeetCode）](https://leetcode.cn/problems/minimum-operations-to-equalize-subarrays/description/)

题目给出一个整数数组nums以及一个整数k。

在一次操作中，可以将nums中的任意元素加上k或者减去k。

另外给出一个二维整数数组queries，其中queries\[index\] \= \[left\[index\], right\[index\]\]。

对于其中的每个查询，需要计算将nums\[left\[index\]\]到nums\[right\[index\]\]这个子数组中所有元素变为相等所需的最小操作次数。若无法实现，那么此次查询的答案为-1。

对于一组询问[start, end]，如果要将nums[start]到nums[end]都变为相等，那么这些元素模k的结果必须都一样，因为若其中的两个元素nums[p]与nums[q]模k的结果不同，那么二者之差的绝对值diff模k必然不为0，也就是说不可能通过加减k操作让二者变为相等。

基于这一点，就可以先一趟遍历，将nums按照模k的余数分为连续的段。若一组询问[start, end]中的起始位置start与end属于不同的段，那么其对应的答案就必然为-1。

---

接下来考虑有解的情况。

这是一个非常经典的贪心的问题，不妨先考虑简化版的问题：给出一个有序的数组，计算将其中所有元素变为相等所需的操作次数。

对于这个问题，最优的处理方法就是将其中的所有元素都变为数组正中间的那个元素。一个简单的证明是将这些元素从两端到中间两两配对，那么：

1、当nums[x] \<\= target \<\= nums[y]时：

所需的代价为nums[y] - target + target - nums[x] \= nums[y] - nums[x]

2、当target \< nums[x]时：

所需的代价为nums[x] - target + nums[y] - target

将nums[y] - target写成nums[y] - nums[x] + nums[x] - target，那么就有

nums[x] - target + nums[y] - target \= nums[y] - nums[x] + (nums[x] - target) \* 2

3、当target > nums[y]时：

与情况2对称，此时的代价为nums[y] - nums[x] + (target - nums[y]) \* 2

可以发现，让target保持在所有数对之间时所需的代价最小，因此让target取数组正中间的元素时最优。

---

回到本题。对于无序的子区间nums[start: end + 1]，问题实际上就是需要找到区间的中位数v，然后计算v与区间中小于v的元素之差的和，再加上区间中大于v的元素与v之差的和，除以k之后即为此次查询的答案。

简单来说，这是一个经典的静态区间第k小值的问题。我在这里采用的是划分树。

接下来简单介绍一下划分树的原理。

从名称来看，划分树是基于分治的一种数据结构，实际上也可以认为其就是对数组执行快速排序过程的一种记录。更具体的，划分树可以认为是一种大小为n \* log(n)的二维数组，其一共有log(n)层，其中第level层对应的是nums在执行快速排序进行第level次递归后得到的数组。

对于传统的快速排序，区间的划分基准pivot一般是取中或者随机获取，但是在通过数组nums建立划分树时，由于nums已知，那么可以先将nums排序得到sorted_nums，那么对于区间[left, right]，其最优的pivot显然就是sorted_nums[mid]，其中mid \= (left + right) // 2。很明显，使用pivot可以将left到right切分成长度最接近的两部分。

接下来遍历left到right，根据当前遍历到的元素与pivot的大小关系确定当前元素应该被划分到下一层树中的左半部分还是右半部分，即划分到下一层的left到mid之间，还是mid + 1到right之间。

在这里需要注意处理等于pivot的元素的划分方案，一种可行的处理方法是在划分前先进行一次遍历，计算有多少个元素严格小于pivot，那么左半区间一共mid - left + 1个元素，减去这些严格小于pivot的元素数量，剩下的位置就需要留给等于pivot元素。

例如数组[7, 1, 4, 3, 2, 5, 0, 6]，排序后的结果为[0, 1, 2, 3, 4, 5, 6, 7]，那么一共4层的数组就分别为

level \= 0：此时就是原始数组[7, 1, 4, 3, 2, 5, 0, 6]

level \= 1：此时只有区间[0, 7]。取有序数组的中间元素为3，得到的结果就是[1, 3, 2, 0, 7, 4, 5, 6]

level \= 2：此时有区间[0, 3]以及[4, 7]。对于前者，取中间元素1，划分得到的数组为[1, 0, 3, 2]；对于后者，取中间元素5，划分得到的数组为[4, 5, 7, 6]。因此这一层的结果为[1, 0, 3, 2, 4, 5, 7, 6]

level \= 3：此时有区间[0, 1], [2, 3], [4, 5], [6, 7]。这四个区间划分后分别为[0, 1], [2, 3], [4, 5], [6, 7]，这一层的结果为[0, 1, 2, 3, 4, 5, 6, 7]

综合起来，得到的4层，长度为8的数组就是

[7, 1, 4, 3, 2, 5, 0, 6]

[1, 3, 2, 0, 7, 4, 5, 6]

[1, 0, 3, 2, 4, 5, 7, 6]

[0, 1, 2, 3, 4, 5, 6, 7]

对应的就是执行快速排序的中间结果。

---

如果只进行划分，相当于仅进行了一次排序，依然无法计算区间第k大值，因此在这里还需要想办法记录每个区间中被划分到下一层左半区间的元素数量。涉及到区间计数问题，转化为前缀之差是很自然的想法，于是可以对于每层的所有区间，都是用一个数组left_cnt记录区间前缀被划分到下一层左半区间的元素数量。与树的元素对应，这个left_cnt也是一个n \* log(n)的二维数组。

对于第level层的区间[left, right]，不妨设现在需要查询子区间[start, end]中第k小的元素，那么：

- left到start - 1这一段中，被划分到下一层左半区间的元素数量prefix_in_left就是left_cnt[level][start - 1]
- 基于prefix_in_left，很容易知道left到start - 1这一段中，被划分到下一层右半区间的元素数量prefix_in_right就是start - left - prefix_in_left
- start到end这一段中，被划分到下一层左半区间的元素数量interval_in_left就是left_cnt的前缀和之差，即left_cnt[level][end] - prefix_in_left
- 基于interval_in_left，很容易知道start到end这一段中，被划分到下一层右半区间的元素数量interval_in_right就是end - start + 1 - interval_in_left

接下来，若k \<\= interval_in_left，那么就说明第k小的元素位于下一层的左半区间中。这个左半区间中的前prefix_in_left个元素是[left, start - 1]这一段中被划分到左半区间的这些元素，因此在下一层的左半区间[left, mid]中：

- 查询区间的起点nxt_start就是left + prefix_in_left
- 终点nxt_end就是nxt_start + interval_in_left - 1
- 于是问题就转化成了递归查询左半区间[left, mid]的子区间[nxt_start, nxt_end]中的第k小元素是什么

反之，若k > interval_in_left，那么就说明第k小的元素，是下一层右半区间中的第k - interval_in_left小的元素。这个右半区间中的前prefix_in_right个元素是[left, start - 1]这一段中被划分到右半区间的这些元素，因此在下一层的右半区间[mid + 1, right]中：

- 查询区间的起点nxt_start就是mid + 1 + prefix_in_right
- 终点nxt_end就是nxt_start + interval_index_right - 1
- 于是问题就转化成了递归查询右半区间[mid + 1, right]的子区间[nxt_start, nxt_end]中的第k - interval_in_left小的元素是什么

到了这里，就可以在O(logn)的时间内查询任意区间的第k小值了。

还是以上面的[7, 1, 4, 3, 2, 5, 0, 6]为例，得到的划分树为

[7, 1, 4, 3, 2, 5, 0, 6]

[1, 3, 2, 0, 7, 4, 5, 6]

[1, 0, 3, 2, 4, 5, 7, 6]

[0, 1, 2, 3, 4, 5, 6, 7]

left_cnt则为：

left_cnt[0] \= [0, 1, 1, 2, 3, 3, 4, 4]。其中产生变化的四个位置分别是1, 3, 2, 0所在的位置

left_cnt[1] \= [1, 1, 1, 2, 0, 1, 2, 2]。其中左半部分[1, 3, 2, 0]，对应的left_cnt是[1, 1, 1, 2]，产生变化的两个位置为1和0所在的位置；右半部分[7, 4, 5, 6]，对应的left_cnt是[0, 1, 2, 2]，产生变化的两个位置为4和5所在的位置

left_cnt[2] \= [0, 1, 0, 1, 1, 1, 0, 1]。其中四个部分分别为[1, 0], [3, 2], [4, 5], [7, 6]，对应的left_cnt分别为[0, 1], [0, 1], [1, 1], [0, 1]，四个部分中产生变化的位置分别为0、2、4、6所在的位置

假设现在要查询整个数组[0, 7]的子区间[3, 6]中的第2小元素，即[3, 2, 5, 0]中的第二小元素，答案应该为2。

首先level \= 0，[left, right] \= [0, 7]，对应的区间为[7, 1, 4, 3, 2, 5, 0, 6]，left_cnt为[0, 1, 1, 2, 3, 3, 4, 4]。此时的[start, end]为[3, 6]，k \= 2：

- prefix_in_left \= left_cnt[0][3 - 1] \= 1，对应的就是[7, 1, 4]中的1
- prefix_in_right \= start - left - prefix_in_left \= 3 - 0 - 1 \= 2，对应的就是[7, 1, 4]中的7和4
- interval_in_left \= left_cnt[0][6] - prefix_in_left \= 4 - 1 \= 3，对应的就是[3, 2, 5, 0]中的3、2、0
- interval_in_right \= end - start + 1 - interval_in_left \= 6 - 3 + 1 - 3 \= 1，对应的就是上面剩下的5

可以发现，k \= 2 \<\= interval_in_left，因此答案位于下一层的左半区间[1, 3, 2, 0]中：

- nxt_start \= left + prefix_in_left \= 1，因为[7, 1, 4]中的1占了下一层左半区间的第一个位置
- nxt_end \= nxt_start + interval_in_left - 1 \= 1 + 3 - 1 \= 3，也就是[3, 2, 5, 0]中的3、2、0占了从nxt_start到nxt_end的3个位置

此时问题转化为了计算左半区间[0, 3]的子区间[1, 3]中的第2小元素。

接下来level \= 1，划分树在这一层为[1, 3, 2, 0, 7, 4, 5, 6]，left_cnt为[1, 1, 1, 2, 0, 1, 2, 2]。

[left, right] \= [0, 3]，对应的值为[1, 3, 2, 0]，对应的left_cnt为[1, 1, 1, 2]。

此时的[start, end]为[1, 3]，k \= 2：

- prefix_in_left \= left_cnt[1][1 - 1] \= 1，对应的就是最左侧那个1
- prefix_in_right \= start - left - prefix_in_left \= 1 - 0 - 1 \= 0，没有元素被分到下一层的右半区间
- interval_in_left \= left_cnt[1][3] - prefix_in_left \= 2 - 1 \= 1，对应的就是[3, 2, 0]中的0
- interval_in_right \= end - start + 1 - interval_in_left \= 3 - 1 + 1 - 1 \= 2，对应的就是上面剩下的3和2

可以发现，k \= 2 > interval_in_left，因此答案位于下一层的右半区间[3, 2]中：

- nxt_start \= mid + 1 + prefix_in_right \= 2，因为left左侧仅有[1]，没有元素被划分到下一层的右半区间，因此下一层子区间的起点就是区间起点mid + 1 \= 2
- nxt_end \= nxt_start + interval_in_right - 1 \= 2 + 2 - 1 \= 3，也就是[3, 2, 0]中的3和2占了从nxt_start到nxt_end的2个位置

此时问题转化为了计算右半区间[2, 3]的子区间[2, 3]中的第1小元素。

接下来level \= 2，划分树在这一层为[1, 0, 3, 2, 4, 5, 7, 6]，left_cnt为[0, 1, 0, 1, 1, 1, 0, 1]。

[left, right] \= [2, 3]，对应的区间为[3, 2]，对应的left_cnt为[0, 1]。此时的[start, end]为[2, 3]，k \= 1：

- prefix_in_left \= 0，需要注意，这里的start就是区间起点，因此左侧没有其他元素需要划分
- prefix_in_right \= start - left - prefix_in_left \= 2 - 2 \= 0
- interval_in_left \= left_cnt[2][3] - prefix_in_left \= 1 - 0 \= 1，对应的就是[3, 2]中的2
- interval_in_right \= end - start + 1 - interval_in_left \= 3 - 2 + 1 - 1 \= 1，对应的就是上面剩下的3

可以发现，k \= 1 \<\= interval_in_left，因此答案位于下一层的左半区间[2, 2]中。此时实际上没必要再计算nxt_start和nxt_end，因为下一层计算时区间长度为1，已经定位到了答案，也就是下一层[0, 1, 2, 3, 4, 5, 6, 7]中下标2对应的元素，也就是2。到了这里，就找到了数组中子区间[3, 6]中的第2小的元素值。

---

到了这里，就可以通过O(nlogn)的时间建立划分树并计算left_cnt数组，然后对于每组查询，都在O(logn)的时间内找出指定区间中位数了。不过仅计算中位数还是不够的，因为最终需要计算的是中位数与区间中其他元素之差的绝对值之和。

对于这个问题，可以仿照left_cnt的思路，额外使用一个left_s数组，用来记录每个区间被划分到下一层左半区间的元素的前缀和，另外再使用一个s数组，记录区间的前缀和，这样一来就可以通过这两个数组，分别计算出当前查询的子数组被划分到下一层左半区间的元素之和interval_left_s以及划分到下一层右半区间的元素之和interval_right_s。接下来，依然是递归查询区间第k小值，记为kth。

若kth位于下一层的左半区间，那么就说明区间内所有被划分到下一层右半区间的元素都大于等于kth。一共有interval_in_right个元素，记为v[0]、v[1]、...、v[interval_in_right - 1]，那么这些元素与kth之差的和就是

v[0] - kth + v[1] - kth + ... + v[interval_in_right - 1] - kth

这些v之和就是上面计算的，子区间中划分到下一层右半区间的元素之和，即interval_right_s。从中减去interval_in_right个kth，就是这些元素与这个第k小值之差的和

同样的，若kth位于下一层的右半区间，那么需要计算的元素之差的和就是interval_in_left \* kth - interval_left_s。

需要注意的是，上面计算的只是被划分到另一半子区间中的元素与kth之差的和，而对于同一半子区间中的元素，则需要在递归计算kth的过程中求解，并跟着kth一起向上返回。

最后附上python代码：

```python
class Solution(object):
    def minOperations(self, nums, k, queries):
        """
        :type nums: List[int]
        :type k: int
        :type queries: List[List[int]]
        :rtype: List[int]
        """
        
        sorted_nums = sorted(nums)

        p2 = 1
        height = 1
        while p2 < len(nums):
            p2 += p2
            height += 1
        
        t = [[0] * len(nums) for _ in range(height)]
        s = [[0] * len(nums) for _ in range(height)]
        left_cnt = [[0] * len(nums) for _ in range(height)]
        left_s = [[0] * len(nums) for _ in range(height)]
        t[0] = nums[:]

        def build(level, left, right):
            if left == right:
                return
            
            mid = (left + right) // 2
            mid_v = sorted_nums[mid]
            same = mid - left + 1
            for v in t[level - 1][left: right + 1]:
                if v < mid_v:
                    same -= 1
            
            p, q = left, mid + 1
            for index, v in enumerate(t[level - 1][left: right + 1], left):
                if index > left:
                    s[level - 1][index] = s[level - 1][index - 1]
                    left_cnt[level - 1][index] = left_cnt[level - 1][index - 1]
                    left_s[level - 1][index] = left_s[level - 1][index - 1]

                s[level - 1][index] += v
                if v < mid_v or (v == mid_v and same > 0):
                    t[level][p] = v
                    left_cnt[level - 1][index] += 1
                    left_s[level - 1][index] += v
                    p += 1
                    if v == mid_v:
                        same -= 1
                else:
                    t[level][q] = v
                    q += 1
            
            build(level + 1, left, mid)
            build(level + 1, mid + 1, right)
        
        def find(level, left, right, start, end, k):
            if start == end:
                return t[level][start], 0
            
            mid = (left + right) // 2

            prefix_in_left = 0
            interval_s = s[level][end]
            interval_left_s = left_s[level][end]
            if start > left:
                prefix_in_left = left_cnt[level][start - 1]
                interval_s -= s[level][start - 1]
                interval_left_s -= left_s[level][start - 1]

            interval_in_left = left_cnt[level][end] - prefix_in_left
            interval_in_right = end - start + 1 - interval_in_left

            if interval_in_left >= k:
                nxt_start = left + prefix_in_left
                nxt_end = nxt_start + interval_in_left - 1
                kth, v = find(level + 1, left, mid, nxt_start, nxt_end, k)
                return kth, v + interval_s - interval_left_s - kth * interval_in_right
            else:
                prefix_in_right = start - left - prefix_in_left
                interval_in_right = end - start + 1 - interval_in_left
                nxt_start = mid + 1 + prefix_in_right
                nxt_end = nxt_start + interval_in_right - 1
                kth, v = find(level + 1, mid + 1, right, nxt_start, nxt_end, k - interval_in_left)
                return kth, v + kth * interval_in_left - interval_left_s

        build(1, 0, len(nums) - 1)

        belong = []
        parts = 0
        pre = None
        for v in nums:
            if pre is None or v % k != pre % k:
                parts += 1
            belong.append(parts)
            pre = v
        
        res = []
        for left, right in queries:
            if belong[left] != belong[right]:
                res.append(-1)
            else:
                kth, v = find(0, 0, len(nums) - 1, left, right, (right - left + 1) // 2 + 1)
                res.append(v // k)
        
        return res
```
