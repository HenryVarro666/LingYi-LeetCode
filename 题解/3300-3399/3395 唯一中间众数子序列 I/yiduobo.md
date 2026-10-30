---
title: "3395. 唯一中间众数子序列I"
aliases: ["yiduobo的每日leetcode 3395.唯一中间众数子序列I"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/math", "leetcode/combinatorics", "leetcode/enumeration", "题单/数学算法", "题单/贪心算法", "题单/数学算法/二-组合数学", "题单/贪心算法/五-思维题"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/30523448468"
zhihu_id: "30523448468"
zhihu_title: "yiduobo的每日leetcode 3395.唯一中间众数子序列I"
question_id: "3395"
question: "唯一中间众数子序列 I"
problem_url: "https://leetcode.cn/problems/subsequences-with-a-unique-middle-mode-i/"
difficulty: "Hard"
rating: 2800
created: "2025-03-16T01:29:36+08:00"
updated: "2025-03-16T01:29:36+08:00"
upvotes: 0
comments: 0
---

# 3395. 唯一中间众数子序列I

> **[yiduobo的每日leetcode 3395.唯一中间众数子序列I](https://zhuanlan.zhihu.com/p/30523448468) · 知乎 · 2025-03-16 · 赞同 0**
> 力扣：[3395. 唯一中间众数子序列 I](https://leetcode.cn/problems/subsequences-with-a-unique-middle-mode-i/) · Hard · 灵茶山艾府：[两种方法，从 O(n^2) 到 O(n)](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3395.唯一中间众数子序列I

[3395. 唯一中间众数子序列 I - 力扣（LeetCode）](https://leetcode.cn/problems/subsequences-with-a-unique-middle-mode-i/description/)

题目给出一个整数数组nums，nums的长度小于等于1000。现在要求找出nums中所有长度为5的唯一中间众数序列的数目。

对于一个长度为5的子序列seq，若seq正中间的元素seq[2]是seq的众数，且seq的众数仅为seq[2]，那么就称seq是唯一中间众数序列。

题目要求找出所有长度为5的唯一中间众数子序列数目，那么一个自然的想法就是枚举nums中的每个元素nums[index]作为这个中间众数，计算合法的子序列数目，然后累加起来即为最终答案。

那么对于当前遍历到的nums[index]，方便起见记x \= nums[index]，那么：

---

1、子序列中5个元素全部都是x：

此时要求从nums[0]到nums[index - 1]之间选出两个x，从nums[index + 1]到nums[-1]之间选出另外两个x。

为了高效计算，在这里可以先一趟遍历，计算出nums中每种元素出现的次数，记为cnt，其中cnt[x]表示x在nums中一共出现了cnt[x]次。

另外在遍历过程中，计算前缀计数哈希表prefix_cnt，其中prefix_cnt[x]表示x在当前前缀中的出现次数。在当前的上下文中，prefix_cnt[x]表示的就是nums[0]到nums[index - 1]之间x出现的次数。

方便起见，记nums[0]到nums[index - 1]之间x的数量prefix_cnt[x]为prefix_x，那么从nums[index + 1]到nums[-1]之间x的数量就是cnt[x] - 1 - prefix_x，中间的减一是减去当前的nums[index]这个x。

那么从前缀中选出两个x的方案数prefix_x_pair就是prefix_x \* (prefix_x - 1) // 2，而从后缀中选出两个x的方案数suffix_x_pair则为suffix_x \* (suffix_x - 1) // 2。

因此总的答案数就是prefix_x_pair \* suffix_x_pair。

另外由于后面会多次计算从若干个相同元素中选出两个的方案数，在这里记calc_pair(z)表示从z个相同元素中选出两个的方案数，即z \* (z - 1) // 2。

---

2、子序列中有4个x：

这4个x中除了中间nums[index]这个x外，还有其他3个x需要分配，可以是前2后1或者前1后2。

对于前2后1这种情况，前缀中选出两个x的方案数就是情况1中的prefix_x_pair，而后缀中选出一个x的方案数则是从后缀中所有x的数目suffix_x，另外还需要选出一个不是x的元素。后缀中一共有n - 1 - (index + 1) + 1 \= n - index - 1个元素，其中x的数目为suffix_x，那么非x的元素suffix_other就是n - index - 1 - suffix_x。

因此前2后1的情况数就是prefix_x_pair \* suffix_x \* suffix_other。

前1后2的情况是完全对称的。前缀中一共有index - 1 - 0 + 1 \= index个元素，其中x的数目为prefix_x，那么非x的元素prefix_other就是index - prefix_x。

因此前1后2的情况数就是suffix_x_pair \* prefix_x \* prefix_other。

---

3、子序列中有3个x：

这3个x中除了中间的x之外，还有两个x需要分配，可以是前2后0、前1后1、前0后2。

对于前2后0这种情况，前缀中的方案数依然是prefix_x_pair，而后缀则可以从非x元素中随意选出两个，因此方案数就是calc_pair(suffix_other)。

因此前2后0的情况数就是prefix_x_pair \* calc_pair(suffix_other)。

对于前0后2这种情况，与上面对称，方案数为suffix_x_pair \* calc_pair(prefix_other)。

最后对于前1后1这种情况，前缀中选出一个x和一个非x，后缀中也一样，因此方案数为prefix_x \* suffix_x \* prefix_other \* suffix_other

---

4、子序列中有2个x：

这2个x种除了中间的x之外，剩下的x可以在前缀或者后缀中。但是这里还有一个条件是必须保证x是唯一众数。对于上面的三种情况，x一定是众数，但是对于当前这种情况，需要保证除了这两个x之外的三个元素两两不同，否则x就不是唯一众数了。

直接计算可选方案数是比较麻烦的，不过好在本题的数据规模可以接受O(n^2)的算法，因此在这里可以考虑枚举其中的另一个元素y，然后再统计剩下两个元素的可行方案。

我在选择的是枚举x同一侧的元素，以x在前缀中的情况进行说明：

目前已有的信息是子序列的正中间是x，而前缀中需要选出一个x和一个非x的元素。接下来枚举所有非x的元素y，那么前缀中y的数目prefix_y就是prefix_cnt[y]，而后缀中y的数目suffix_y就是cnt[y] - prefix_y。

接下来还需要判断从后缀中选出两个不同的元素，且这两个元素不等于x也不等于y的方案数。

可以明确的是，后缀中不等于x也不等于y的元素数量就是suffix_other - suffix_y，那么从中选出两个元素的方案数就是calc_pair(suffix_other - suffix_y)。

需要注意，这种选取方案中依然可能选出两个相同的元素，需要将这部分从中去除掉。我在这里采用的方法是额外计算一个后缀计数数组suffix_same_pair，其中suffix_same_pair[index]表示从nums[index]到nums[-1]这些元素中可以选出的相同元素对的数目。那么在当前场景下，后缀中选出两个元素且二者相同的方案数就是suffix_same_pair[index + 1]，但是其中也包含了相同的x以及相同的y的方案，还需要从中减去calc_pair(suffix_x)以及calc_pair(suffix_y)

综合起来，从后缀中选出两个不同的元素，且这两个元素不等于x也不等于y的方案数suffix_pair就是

calc_pair(suffix_other - suffix_y) - (suffix_same_pair[index + 1] - calc_pair(suffix_x) - calc_pair(suffix_y))

而总的方案数就是

prefix_x \* prefix_y \* suffix_pair

接下来就是如何计算suffix_same_pair。对于suffix_same_pair[index]而言，其在suffix_same_pair[index + 1]的基础上，nums[index]还可以与nums[index + 1]到nums[-1]中所有值为nums[index]的元素形成pair对，因此可以从后往前遍历nums，使用一个哈希表cnt记录当前遍历过的后缀中每种元素出现的次数，那么对于nums[index]：

若index等于n - 1，那么就有suffix_same_pair[index] \= 0。

否则就有suffix_same_pair\[index\] \= suffix_same_pair\[index + 1\] + cnt\[nums\[index\]\]。

无论是哪种情况，都应该将cnt\[nums\[index\]\]加上1，然后继续向前遍历。

以上为另一个x在前缀中的方案数的计算过程，而对于另一个x在后缀中的方案数则与之对称，先正序遍历预处理出前缀计数数组prefix_same_pair，其中prefix_same_pair[index]表示从nums[0]到nums[index]这些元素中可以选出的相同元素对的数目，计算方法与suffix_same_pair类似。

那么从前缀中选出两个不同的元素，且这两个元素不等于x也不等于y的方案数prefix_pair就是

calc_pair(prefix_other - prefix_y) - (prefix_same_pair[index - 1] - calc_pair(prefix_x) - calc_pair(prefix_y))

总的方案数就是

suffix_x \* suffix_y \* prefix_pair

---

到了这里，每种合法的情况就都讨论完了。根据上面的结论，需要先正反两趟遍历，预处理出prefix_same_pair以及suffix_same_pair，同时在过程中也可以顺便将每种元素出现的次数数组cnt计算好。

接下来对nums进行一趟遍历，一边使用上面4种情况中描述的方法计算合法的子序列数目，一边更新前缀计数数组prefix_cnt即可。

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
        for index, x in enumerate(nums):
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

            for y in cnt:
                if x == y:
                    continue
                    
                prefix_y = prefix_cnt.get(y, 0)
                suffix_y = cnt[y] - prefix_y

                if prefix_y > 0 and suffix_other - suffix_y >= 2:
                    suffix_pair = calc_pair(suffix_other - suffix_y)
                    suffix_pair -= suffix_same_pair[index + 1]
                    suffix_pair += calc_pair(suffix_x) + calc_pair(suffix_y)
                    res = (res + prefix_x * prefix_y * suffix_pair) % mod
                    
                if suffix_y > 0 and prefix_other - prefix_y >= 2:
                    prefix_pair = calc_pair(prefix_other - prefix_y)
                    prefix_pair -= prefix_same_pair[index - 1]
                    prefix_pair += calc_pair(prefix_x) + calc_pair(prefix_y)
                    res = (res + suffix_x * suffix_y * prefix_pair) % mod
            
            prefix_cnt[x] = prefix_cnt.get(x, 0) + 1

        return res
```
