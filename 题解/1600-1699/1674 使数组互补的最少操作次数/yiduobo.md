---
title: "1674. 使数组互补的最少操作次数"
aliases: ["yiduobo的每日leetcode 1674.使数组互补的最少操作次数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "题单/常用数据结构", "题单/常用数据结构/二-差分"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/444026308"
zhihu_id: "444026308"
zhihu_title: "yiduobo的每日leetcode 1674.使数组互补的最少操作次数"
question_id: "1674"
question: "使数组互补的最少操作次数"
problem_url: "https://leetcode.cn/problems/minimum-moves-to-make-array-complementary/"
difficulty: "Medium"
rating: 2333
created: "2021-12-11T14:51:55+08:00"
updated: "2021-12-11T14:51:55+08:00"
upvotes: 0
comments: 0
---

# 1674. 使数组互补的最少操作次数

> **[yiduobo的每日leetcode 1674.使数组互补的最少操作次数](https://zhuanlan.zhihu.com/p/444026308) · 知乎 · 2021-12-11 · 赞同 0**
> 力扣：[1674. 使数组互补的最少操作次数](https://leetcode.cn/problems/minimum-moves-to-make-array-complementary/) · Medium · 灵茶山艾府：[差分数组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1674.是数组互补的最少操作次数

[力扣](https://leetcode-cn.com/problems/minimum-moves-to-make-array-complementary/)

首先考虑贪心的做法。一个很直观的想法就是哪种组合出现的次数最多，就让其他组合往那种组合靠拢。但是这样做有一个问题就是若这种组合靠近边界，那么其他组合可能需要操作两次才能变成出现次数最多的那种组合。

不妨设现在有三种组合a、b、c，出现次数分别为cnt_a、cnt_b以及cnt_c。其中a变成b或者b变成a需要1次操作，a变成c或者c变成a需要两次操作，b变成c和c变成b需要1次操作。

若此时cnt_c最大，那么按上面贪心的做法，就要将a和b都变成c，一共需要的操作次数就是

cnt_a \* 2 + cnt_b

而如果将a和c都变成b，那么需要的操作次数则是

cnt_a + cnt_c

也就是说只要cnt_a + cnt_b > cnt_c，上面贪心的做法就是不成立的。

贪心的做法行不通，只能换一种思路。

对于一组数对(x, y)而言:

1、其不变的情况下对应的和s \= x + y

2、若对其进行一次操作，那么对应的和s的取值范围就满足

x + 1 \<\= s \<\= x + limit

或者

y +1 \<\= s \<\= y + limit

综合起来就是

min(x, y) + 1 \<\= s \<\= max(x, y) + limit

3、若对其进行两次操作，那么对应的和s可以覆盖到2到limit + limit中的任何数

可以发现，如果将s可能到达的数按2到limit + limit列出来的话，其操作次数的分布就是

2, 2, 2, ..., 2, 1, 1, 1, ..., 1, 0, 1, 1, 1, ..., 1, 2, 2, 2, ..., 2

对于数组中的每一组(x, y)都可以写出上面这种操作次数的分布。如果将这些分布全部叠加起来，那么每个位置上值就是将数组中每一组(x, y)的和转化到该位置表示的那个数的操作次数之和。很明显，题目的答案就是其中的最小值。

对于这些操作分布而言，如果从区间操作的角度来看这个问题，就可以转化成下面几种操作：

1、先将区间所有数置为2

2、将区间min(x, y) + 1到max(x, y) + limit中的数全部减1

3、再将x + y这个位置上的数减1

到了这里，问题就转化成了一个区间最小值的问题。常规的线段树或者树状数组都是可以解决的，不过这里是先操作，后求解的静态区间最小值问题，那么使用差分数组是更好的选择。

差分数组简单来说就是对于一个区间操作将区间[x, y]中的数减去1来说，可以设置一个入口标记left[x]以及出口标记right[y + 1]。接下来从头开始遍历区间的每个下标index，并记录当前下标位置上的值now。若当前位置存在标记left[index]，说明触发了一次以x为左边界的区间减一操作，那么就将now减去1；类似的，若当前位置存在标记right[index]，说明之前某一次区间减一操作的右边界为y，那么从index开始这个减1操作就结束了，因此需要将now加上1。一趟扫描下来，就可以求出区间中每个位置的值了。

根据上面的结论，可以先遍历所有的数对(x, y)，每一组(x, y)可以形成两组区间标记，分别为left[min(x, y) + 1], right[max(x, y) + limit]以及left[x + y], right[x + y + 1]。

区间每个位置上的初始值都是n，因为这里一共是n / 2组数，每组数对应区间的初始值都是2，因此需要初始化now为n。

然后从2到limit \* 2开始遍历下标index，使用差分数组更新now并使用当前位置上的now来更新答案即可。

最后附上python代码：

```python
class Solution(object):
    def minMoves(self, nums, limit):
        """
        :type nums: List[int]
        :type limit: int
        :rtype: int
        """

        n = len(nums)
        left = [0] * (limit + limit + 1)
        right = [0] * (limit + limit + 1)

        for index in range(n / 2):
            x = nums[index]
            y = nums[n - index - 1]
            left[min(x, y) + 1] += 1
            if max(x, y) + 1 <= limit:
                right[max(x, y) + limit + 1] += 1
            
            left[x + y] += 1
            if x + y + 1 <= limit + limit:
                right[x + y + 1] += 1
        
        now = n
        res = now
        for target in range(2, limit + limit + 1):
            now += right[target] - left[target]
            res = min(res, now)
        
        return res
```
