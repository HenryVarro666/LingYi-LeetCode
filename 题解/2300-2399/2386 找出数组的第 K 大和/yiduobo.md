---
title: "2386. 找出数组的第K大和"
aliases: ["yiduobo的每日leetcode 2386.找出数组的第K大和"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/depth-first-search", "leetcode/binary-search", "leetcode/heap-priority-queue", "题单/二分算法", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/二分算法/二-二分答案", "题单/常用数据结构/五-堆-优先队列", "题单/链表-二叉树与回溯/四-回溯"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/565534466"
zhihu_id: "565534466"
zhihu_title: "yiduobo的每日leetcode 2386.找出数组的第K大和"
question_id: "2386"
question: "找出数组的第 K 大和"
problem_url: "https://leetcode.cn/problems/find-the-k-sum-of-an-array/"
difficulty: "Hard"
rating: 2648
created: "2022-09-18T02:24:11+08:00"
updated: "2022-09-18T02:24:11+08:00"
upvotes: 0
comments: 0
---

# 2386. 找出数组的第K大和

> **[yiduobo的每日leetcode 2386.找出数组的第K大和](https://zhuanlan.zhihu.com/p/565534466) · 知乎 · 2022-09-18 · 赞同 0**
> 力扣：[2386. 找出数组的第 K 大和](https://leetcode.cn/problems/find-the-k-sum-of-an-array/) · Hard · 灵茶山艾府：[两种方法：二分答案+暴搜/最小堆（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日一题，争取不卡题吧。

2386.找出数组的第K大和

[力扣](https://leetcode.cn/problems/find-the-k-sum-of-an-array/)

题目中n非常大，处理起来会比较麻烦，但是k相对是比较小的，那么不妨从最大的组合开始逐个向下找，直到找到第k大和为止。

首先消除0的影响。不妨设当前数组中有cnt个0，那么对于任意一种非0数的组合，这cnt个0就可以带来2^cnt个相同的值，那么在这里可以先将0都从数组中剔除，然后问题查找的步长从1变成2^cnt。

接下来开始进行构造。

数组的最大和显然就是数组中所有正数之和，当没有正数时则为0。对于次大和，就可以选择从最大值中剔除最小的正数，或者加入一个最大负数。方便起见，在这里不妨将所有负数取相反数，那么每次操作就都相当于从当前和中减去最小的正数了。

第三大和只能是最大和减去数组中第二小的正数，但对于后面的和就有变数了。

第四大和可能是最大和减去第三小的正数，也可能是第二大和减去第二小的正数，越往后则可能性越多。为了高效得到当前要找的和，可以使用一个堆来维护当前的候选和。

另外需要注意两点：

第一是当某个和减去某个数得到的结果还没有成为正式的第若干大值之前，没有必要尝试让这个和减去更大的数。例如上面说的第四大和，若最大和减去第三小的正数不是第四大和，那么暂时就没有比较将最大和减去第四小的正数纳入候选集了，因为最大和减去第三小的整数还没有被用到。

第二是为了避免重复，可以规定每个值减数的时候只会选择比得到当前值那一轮减去的数更大的数来进行操作。例如对上面说的第三大和进行操作，那么就不应该让第三大和再减去最小的正数，因为这样就会与第二大和减去第二小的正数出现重复了。

根据上面两个结论，就可以在构造出和的同时记录下一个可用的数组下标p，那么对于当前的第m大和(now, p)：

1、可以从now开始继续向后构造，因此可以将(now - nums[p], p + 1)加入到堆中

2、构造出now的值为now + nums[p - 1]，由于now被消耗掉了，那么就应该从now + nums[p - 1]这里再向后继续构造一个值加入到堆中，也就是轮到了now + nums[p - 1] - nums[p]，因此还需要将(now + nums[p - 1] + nums[p], p + 1)加入到堆中

重复若干轮，每轮使用k减去2^cnt，直到k小于等于0为止。停止时堆中的最大值就是最终答案。

由于python中的堆默认是小根堆，因此在这里需要将数组和取相反数，对应的在更新时，运算符也都需要取反。

最后附上python代码：

```python
class Solution(object):
    def kSum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        """

        non_zero_list = []
        zero_cnt = 0
        s = 0
        for num in nums:
            if num > 0:
                non_zero_list.append(num)
                s += num
            elif num < 0:
                non_zero_list.append(-num)
            else:
                zero_cnt += 1
        
        non_zero_list.sort()

        same_cnt = 1
        for _ in range(zero_cnt):
            same_cnt += same_cnt
            if same_cnt >= k:
                break

        k -= same_cnt
        heap = [[-s, 0]]
        while k > 0:
            now, pos = heapq.heappop(heap)
            if pos < len(non_zero_list):
                heapq.heappush(heap, [now + non_zero_list[pos], pos + 1])
                
                if pos > 0:
                    heapq.heappush(heap, [now - non_zero_list[pos - 1] + non_zero_list[pos], pos + 1])
        
            k -= same_cnt

        return -heap[0][0]
```
