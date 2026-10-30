---
title: "3416. 唯一中间众数子序列II"
aliases: ["yiduobo的每日leetcode 3416.唯一中间众数子序列II"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/math", "leetcode/combinatorics"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/32508314796"
zhihu_id: "32508314796"
zhihu_title: "yiduobo的每日leetcode 3416.唯一中间众数子序列II"
question_id: "3416"
question: "唯一中间众数子序列 II"
problem_url: "https://leetcode.cn/problems/subsequences-with-a-unique-middle-mode-ii/"
difficulty: "Hard"
created: "2025-03-25T03:40:45+08:00"
updated: "2025-03-25T03:40:45+08:00"
upvotes: 2
comments: 1
---

# 3416. 唯一中间众数子序列II

> **[yiduobo的每日leetcode 3416.唯一中间众数子序列II](https://zhuanlan.zhihu.com/p/32508314796) · 知乎 · 2025-03-25 · 赞同 2**
> 力扣：[3416. 唯一中间众数子序列 II](https://leetcode.cn/problems/subsequences-with-a-unique-middle-mode-ii/) · Hard · 灵茶山艾府：[O(n) 做法（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3416.唯一中间众数子序列II

[3416. 唯一中间众数子序列 II - 力扣（LeetCode）](https://leetcode.cn/problems/subsequences-with-a-unique-middle-mode-ii/)

题目给出一个整数数组nums，nums的长度小于等于1000。现在要求找出nums中所有长度为5的唯一中间众数序列的数目。

对于一个长度为5的子序列seq，若seq正中间的元素seq[2]是seq的众数，且seq的众数仅为seq[2]，那么就称seq是唯一中间众数序列。

本题的题设与之前的3395题相同，但是数据规模较大，nums的长度可以达到10^5，这也就意味着3395题中O(n^2)的算法不成立了。

[yiduobo：yiduobo的每日leetcode 3395.唯一中间众数子序列I](https://zhuanlan.zhihu.com/p/30523448468)

回顾一下之前3395题的处理方法，可以发现，对于子序列中有5、4、3个x的情况都还是可以照搬过来的，于是可以依然按照枚举中间x的处理方法遍历nums，然后针对两个x的情况进行优化。由于前缀和后缀在这里是对称的，因此在这里对前缀中存在另一个x的情况进行分析：

首先罗列一下之前3395题中已经有的信息，某些是可以复用的。

离线预处理得到的有：

cnt：哈希表，其中cnt[v]表示v在nums中出现的总数，离线预处理得到

prefix_same_pair：数组，其中prefix_same_pair[index]表示从nums[0]到nums[index]这些元素中可以选出的相同元素对数目

suffix_same_pair：数组，其中suffix_same_pair[index]表示从nums[index]到nums[-1]这些元素中可以选出的相同元素对数目

随着遍历的进行实时计算的有：

prefix_cnt：哈希表，其中prefix_cnt[v]表示当前前缀中v出现的次数

prefix_x：前缀中x的数目

suffix_x：后缀中x的数目

prefix_x_pair：前缀中形如xx的元素对的数目

suffix_x_pair：后缀中形如xx的元素对的数目

prefix_other：前缀中非x的数目

suffix_other：后缀中非x的数目

另外设计辅助函数calc_pair(z)，作用是计算从z个元素中选出两个的方案数，也就是z \* (z - 1) // 2

而接下来需要计算的是形如xw_x_yz的子序列的数目，其中w、x、y、z两两之间互不相同。

---

根据之前的suffix_other、suffix_same_pair以及suffix_x_pair，可以先得到形如x_yz的子序列的数目，其中x、y、z两两之间互不相同：

1、从后缀中非x的元素中选出两个的方案是suffix_other \* (suffix_other - 1) // 2，也就是之前的calc_pair(suffix_other)

2、calc_pair(suffix_other)中的元素对可能包含两个元素相同的情况，也就是yy这样的元素对，因此还需要将这些情况去掉

3、suffix_same_pair[index + 1]中包含了所有后缀中相同的元素对数量，但是也包含了形如xx的元素对的数量

那么对于suffix_same_pair[index + 1]中的元素对，减去xx的数量，也就是suffix_x_pair，就是非x的相同元素组成的元素对数目，也就是yy这样的元素对的数目。将这些元素对从calc_pair(suffix_other)中减去，就可以得到x_yz的数目了，也就是

x_yz \= calc_pair(suffix_other) - (suffix_same_pair[index + 1] - suffix_x_pair)

---

得到x_yz后，就可以很快得到形如ax_x_yz的子序列数目：

1、从前缀中选出一个x，方案数为前缀中x的数量，即prefix_x

2、从前缀中选出一个非x的a，方案数为前缀中其他元素的数量，即prefix_other

3、结合x_zy

因此ax_x_yz的数目就是

ax_x_yz \= prefix_x \* prefix_other \* x_zy

---

然而对于ax_x_yz而言，在这里a只是限定了不与x相同，但是依然可能与y或者z相同，也就是说ax_x_yz中存在形如xy_x_yz或者xz_x_yz这样不合法的子序列，需要删去。

接下来的问题就变成了如何计算xy_x_yz的数目。

对于这个问题，可以先考虑计算xy_x_ya的数目，其中a不等于x但是可以等于y。然后从中减去a等于y情况，也就是xy_x_yy的数目，从而得到xy_x_yz的数目。

对于xy_x_ya的数目，由于前缀中的x的数目以及后缀中的a的数目都是很好计算的，那么实际上就是要计算出y_x_y的数目。

同样的，则对于y_x_y的数目，可以先计算a_x_a的数目，这里a可以等于x。然后从中减去a等于y的情况，也就是x_x_x数目就行了。

对于xy_x_yy的数目，如法炮制，考虑计算y_x_yy的数目，然后通过先计算a_x_aa的数目，再减去x_x_xx的数目就可以了。

---

其中x_x_x和x_x_xx的计算方法比较简单，分别是prefix_x \* suffix_x以及prefix_x \* calc_pair(suffix_x)，因此问题就变成了如何求解形如a_x_a以及a_x_aa的数量。

如果想要离线计算的话，如果不枚举前缀和后缀中的每种a，就又需要使用全体减重复的方法来计算，越搞越复杂，因此在这里先尝试随着nums的遍历实时计算。

不妨设当前遍历到nums[index]，只有当index > 0时，才可能会有a_x_a和a_x_aa的出现，因为x的左侧必须有元素存在。不妨设nums[index - 1]为v，那么这里考察的是x从v变为当前的nums[index]的这一过程：

1、对于a_x_a：

相比于之前计算得到的a_x_a，由于这里index的移动，多出了原来的nums[index - 1] \= v可以作为a_x_a左侧的a来用，因此只需计算x右侧，也就是nums[index + 1]到nums[-1]之间v的数量suffix_v_cnt就行了。

对于suffix_v_cnt，可以先使用cnt[v] - prefix_cnt[v]计算出nums[index]到nums[-1]之间v的数量，若nums[index]，也就是x本身也等于v，就将suffix_v_cnt减1。

接下来每个suffix_v_cnt中的v都可以和nums[index - 1]这个v形成一组a_x_a，因此在之前a_x_a的基础上需要加上suffix_v_cnt。

同样的，由于nums[index]这个位置上的x被当做中间元素x使用了，因此其不能再作为a_x_a右侧的a来使用，因此在这里还需要统计nums[0]到nums[index - 2]中所有x的数量prefix_x_cnt。

在这里只需先通过prefix_cnt得到nums[0]到nums[index - 1]中x的数量，然后若x等于nums[index - 1]，也就是x等于v，则再将prefix_x_cnt减1。

接下来每个prefix_x_cnt中的x在之前与nums[index]，以及nums[index - 1]形成的a_x_a都将失效，因此在之前的a_x_a的基础上需要减去prefix_x_cnt。

2、对于a_x_aa：

处理的方法与a_x_a类似。由于index的移动，nums[index - 1] \= v可以作为a_x_aa左侧的v来用，而右侧两个v构成的pair对的数量就是calc_pair(suffix_v_cnt)。

另一方面，由于原来可以作为a_x_aa中x右侧第一个a的nums[index]成为了x，导致这些a_x_aa失效，而失效的a_x_aa的数量可以根据nums[0]到nums[index - 2]中x的数量乘以nums[index + 1]到nums[-1]中x的数量得到。

其中nums[index + 1]到nums[-1]中x的数量suffix_x_cnt又可以通过先计算出nums[index]到nums[-1]中x的数量，也就是cnt[x] - prefix_cnt[x]，然后再减去nums[index]这个x得到，也就是suffix_x_cnt \= cnt[x] - prefix_cnt[x] - 1。

---

根据上面的结论，再得到a_x_a之后，可以通过a_x_a - prefix_x \* suffix_x得到y_x_y。同样的，得到a_x_aa之后，可以通过a_x_aa - prefix_x \* calc_pair(suffix_x)得到y_x_yy。

接下的对于每一组y_x_y，在前缀中添加一个x的方案数是prefix_x，在后缀中添加一个不是x的方案数是n - index - 1 - suffix_x - 1，其中n - index - 1是后缀中元素的总数，从中减去suffix_x个x不能用，另外还需要减去1是因为y_x_y这个形式的三元组中，后面这个y占用了后缀中的一个其他元素。

也就是说，xy_x_ya的数量就等于prefix_x \* y_x_y \* (n - index - 1 - suffix_x - 1)。

另一方面，对于每一组y_x_yy，在前缀中添加一个x的方案数是prefix_x，因此得到xy_x_yy的方案数就是prefix_x \* y_x_yy。

在这里需要特别注意的是，对于xy_x_ya而言，由于y和a是无序的，因此在通过y_x_y拼接得到xy_x_ya的过程中实际上多计算了一次xy_x_yy，因此在通过xy_x_ya中减去xy_x_yy来得到xy_x_yz时，需要将去两倍的xy_x_yy。即xy_x_yz \= xy_x_ya - xy_x_yy \* 2。

---

在得到了xy_x_yz之后，再使用ax_x_yz的数量减去xy_x_yz的数量，就是wx_x_yz的数量。这是x位于前缀中的方案数，按类似的方法逐层拆解，计算形如yz_x_wx的子序列数量即可。

最后附上python代码：

```python
class Solution(object):
    def subsequencesWithMiddleMode(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)

        cnt = {}
        prefix_same_pair = []
        for index in range(n):
            v = nums[index]
            if index == 0:
                prefix_same_pair.append(0)
            else:
                prefix_same_pair.append(prefix_same_pair[-1] + cnt.get(v, 0))
            cnt[v] = cnt.get(v, 0) + 1
        
        cnt = {}
        suffix_same_pair = []
        for index in range(n - 1, -1, -1):
            v = nums[index]
            if index == n - 1:
                suffix_same_pair.append(0)
            else:
                suffix_same_pair.append(suffix_same_pair[-1] + cnt.get(v, 0))
            cnt[v] = cnt.get(v, 0) + 1
        suffix_same_pair.reverse()

        def calc_pair(cnt):
            if cnt < 2:
                return 0
            return cnt * (cnt - 1) // 2

        mod = 10 ** 9 + 7
        n = len(nums)
        res = 0
        prefix_cnt = {}
        a_x_a = 0
        aa_x_a = 0
        a_x_aa = 0

        for index, x in enumerate(nums):
            if index > 0:
                v = nums[index - 1]
                suffix_v_cnt = cnt[v] - prefix_cnt[v]
                if x == v:
                    suffix_v_cnt -= 1
                a_x_a += suffix_v_cnt

                prefix_x_cnt = prefix_cnt.get(x, 0)
                if x == v:
                    prefix_x_cnt -= 1
                a_x_a -= prefix_x_cnt

                suffix_x_cnt = cnt[x] - prefix_cnt.get(x, 0) - 1

                a_x_aa += calc_pair(suffix_v_cnt)
                a_x_aa -= prefix_x_cnt * suffix_x_cnt

                prefix_v_cnt = prefix_cnt[v] - 1
                suffix_x_cnt = cnt[x] - prefix_cnt.get(x, 0) - 1
                aa_x_a += prefix_v_cnt * suffix_v_cnt 
                aa_x_a -= calc_pair(prefix_x_cnt)

            if index < 2:
                prefix_cnt[x] = prefix_cnt.get(x, 0) + 1
                continue
            if index > n - 3:
                break
            
            prefix_x = prefix_cnt.get(x, 0)
            suffix_x = cnt[x] - 1 - prefix_x
            prefix_other = index - prefix_x
            suffix_other = n - index - 1 - suffix_x

            prefix_x_pair = calc_pair(prefix_x)
            suffix_x_pair = calc_pair(suffix_x)

            res = (res + prefix_x_pair * suffix_x_pair) % mod

            res = (res + prefix_x_pair * suffix_x * suffix_other) % mod
            res = (res + suffix_x_pair * prefix_x * prefix_other) % mod

            res = (res + prefix_x_pair * calc_pair(suffix_other)) % mod
            res = (res + suffix_x_pair * calc_pair(prefix_other)) % mod
            res = (res + prefix_x * suffix_x * prefix_other * suffix_other) % mod

            y_x_y = a_x_a - prefix_x * suffix_x
            y_x_yy = a_x_aa - prefix_x * calc_pair(suffix_x)
            yy_x_y = aa_x_a - calc_pair(prefix_x) * suffix_x

            if suffix_other >= 2:
                x_yz = calc_pair(suffix_other) - (suffix_same_pair[index + 1] - suffix_x_pair)
                res = (res + prefix_x * prefix_other * x_yz) % mod
                res = (res - prefix_x * (y_x_y * (n - index - 1 - suffix_x - 1) - y_x_yy * 2) % mod + mod) % mod

            if prefix_other >= 2:
                yz_x = calc_pair(prefix_other) - (prefix_same_pair[index - 1] - prefix_x_pair)
                res = (res + suffix_x * suffix_other * yz_x) % mod
                res = (res - suffix_x * (y_x_y * (index - prefix_x - 1) - yy_x_y * 2) % mod + mod) % mod
            
            prefix_cnt[x] = prefix_cnt.get(x, 0) + 1

        return res
```
