---
title: "3318. 计算子数组的x-sum I & 3321. 计算子数组的x-sum II"
aliases: ["yiduobo的每日leetcode 3318.计算子数组的x-sum I && 3321.计算子数组的x-sum II", "3318. 计算子数组的x-sum I", "3321. 计算子数组的x-sum II"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/ordered-set", "leetcode/sliding-window", "leetcode/hard", "题单/常用数据结构", "题单/常用数据结构/五-堆-优先队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2037126048"
zhihu_id: "2037126048"
zhihu_title: "yiduobo的每日leetcode 3318.计算子数组的x-sum I && 3321.计算子数组的x-sum II"
question_id: ["3318", "3321"]
question: ["计算子数组的 x-sum I", "计算子数组的 x-sum II"]
problem_url: ["https://leetcode.cn/problems/find-x-sum-of-all-k-long-subarrays-i/", "https://leetcode.cn/problems/find-x-sum-of-all-k-long-subarrays-ii/"]
difficulty: ["Easy", "Hard"]
rating: 2598
created: "2024-10-20T03:31:53+08:00"
updated: "2024-10-20T03:31:53+08:00"
upvotes: 0
comments: 0
---

# 3318. 计算子数组的x-sum I & 3321. 计算子数组的x-sum II

> **[yiduobo的每日leetcode 3318.计算子数组的x-sum I && 3321.计算子数组的x-sum II](https://zhuanlan.zhihu.com/p/2037126048) · 知乎 · 2024-10-20 · 赞同 0**
> 力扣：[3318. 计算子数组的 x-sum I](https://leetcode.cn/problems/find-x-sum-of-all-k-long-subarrays-i/) · Easy · 灵茶山艾府：[O(nlogk) 非暴力做法（Python/Java/C++/Go）](../3318%20计算子数组的%20x-sum%20I/灵茶山艾府.md)
> 力扣：[3321. 计算子数组的 x-sum II](https://leetcode.cn/problems/find-x-sum-of-all-k-long-subarrays-ii/) · Hard · 灵茶山艾府：[两个有序集合维护前 x 大二元组（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3318.计算子数组的x-sum I

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-x-sum-of-all-k-long-subarrays-i/description/)

3321.计算子数组的x-sum II

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-x-sum-of-all-k-long-subarrays-ii/description/)

题目给出一个有n个整数组成的数组nums，以及另外两个整数k和x。

接下来要求计算nums中所有长度为k的子数组的x-sum，其中x-sum的定义为：

1、统计数组中所有元素出现的次数

2、取出现次数最多的x种元素，若两个元素出现次数相同，则取数值较大的元素

3、计算子数组中这x种元素之和

题目又可以称做滑动窗口的x-sum，因此可以参考之前480题，使用两个堆来求解。

[yiduobo：yiduobo的每日leetcode 480.滑动窗口中位数](https://zhuanlan.zhihu.com/p/246224986)

对于本题，其中一个堆大小为x，其中储存的是频率最大的x种元素以及对应的频率，这个堆为小顶堆，其中元素与频率乘积累加起来就是当前窗口的x-sum；另一个堆中则储存滑动窗口内其他的元素以及对应的频率，这个堆为大顶堆。

首先遍历数组的前k个元素，统一先加入到答案堆中。若此时答案堆的大小大于x，则不断弹出答案堆的堆顶并加入到备选堆中，直到答案堆的大小等于x位置。

接下来从下标k开始向后遍历，对于当前遍历到的index，需要先将左边界对应元素nums[index - k]的频率减去1，然后将新加入的元素nums[index]的频率加上1。

接下来：

1、若答案堆大小超过x，那么将其堆顶弹出并加入到备选堆

2、若答案堆大小小于x，且备选堆非空，则将备选堆堆顶弹出并加入到答案堆中

3、若备选堆非空，还需要对比两个堆堆顶的大小。若答案堆堆顶频率较小，则交换两个堆的堆顶

在维护堆时同时维护对应的x-sum，每一轮操作完毕后只需将对应的x-sum加入到答案中即可。

在具体实现上，因为堆中实际的元素不是定量的，粗略分析感觉这里不太好用延迟删除。为了可以实时删除，在这里只能手动实现一个堆。具体实现上还是采用常见的数组下标模拟，即下标p的左右孩子分别为p \* 2 + 1以及p \* 2 + 2。在这里需要使用val和freq两个数组分别记录堆中元素值以及对应的频率。另外为了适配删除操作，在这里还需要使用一个哈希表index记录每种元素在堆数组中的具体下标位置。

接下来对于每种操作：

1、插入数值v，频率为f：

若v已经在堆中，那么通过index\[v\]找到对应的下标位置，然后将f累加到freq\[index\[v\]\]中。此时频率发生了变化，若堆为小顶堆，那么就应该将节点下移，否则应该将节点上移。

若v没有在堆中，则将v和f分别加入到val和freq的末尾同时更新index[v]，然后将当前节点上移。

无论是哪种情况，都需要将堆中元素之和加上v \* f。

2、删除数值v一次：

首先将堆中元素之和减去v，然后将v的频率，也就是freq\[index\[v\]\]减去1。

若freq\[index\[v\]\]此时等于0，说明窗口中没有v了，此时应该将对应的节点删去。将该节点与堆数组的最后一个节点交换然后弹出，另外被交换过来的节点需要同时尝试上移或者下移，当然根据堆的定义最多只能执行一个方向的移动，但是两边都需要进行检测。

若freq\[index\[v\]\]非0，那么由于此时频率发生了变化，若堆为小顶堆，则应该将节点上移，否则应该将节点下移。

3、上移某个节点p：

p的父节点fa为(p - 1) // 2，若fa存在，则对比p和fa的频率和大小，决定是否需要交换二者。交换时除了val和freq外，对应的index也需要交换。

对比的准则是若堆为小顶堆，则将频率较小的节点放上面，反之将频率较大的节点放上面。

4、下移某个节点p：

p的左右孩子left和right分别为p + p + 1以及p + p + 2。

若left和right都存在，则需要先对比left和right，选择其中更符合条件的作为备选child；若仅有left存在，则只选择left作为备选child。接下来对比p和child的频率和大小，决定是否需要交换二者。

5、移除堆顶：

与删除操作类似，此时只需交换堆顶，也就是堆数组下标为0的元素，与堆数组中最后的元素，然后从堆数组中弹出。对于交换后的堆顶，执行下移操作。最后返回原来的堆顶元素值即可。

最后附上python代码：

```python
class HeapWithFreq(object):
    def __init__(self, root_type = 0):
        self.val = []
        self.freq = []
        self.index = {}
        self.s = 0
        self.size = 0
        self.cmp_func = [self.lt, self.gt]
        self.root_type = root_type

    def insert(self, v, f=1):
        self.s += v * f
        if v not in self.index:
            self.index[v] = self.size
            self.size += 1
            self.val.append(v)
            self.freq.append(f)
            self.up(self.index[v])
        else:
            self.freq[self.index[v]] += f
            if self.root_type == 0:
                self.down(self.index[v])
            else:
                self.up(self.index[v])
    
    def delete(self, v):
        self.s -= v
        self.freq[self.index[v]] -= 1
        if self.freq[self.index[v]] == 0:
            p = self.index[v]
            self.swap(self.size - 1, p)
            self.size -= 1
            self.index.pop(v)
            self.val.pop()
            self.freq.pop()
            if p < self.size:
                self.down(p)
                self.up(p)
        else:
            if self.root_type == 0:
                self.up(self.index[v])
            else:
                self.down(self.index[v])

    def swap(self, i, j):
        self.val[i], self.val[j] = self.val[j], self.val[i]
        self.freq[i], self.freq[j] = self.freq[j], self.freq[i]
        self.index[self.val[i]] = i
        self.index[self.val[j]] = j

    def lt(self, i, j):
        if self.freq[i] == self.freq[j]:
            return self.val[i] < self.val[j]
        return self.freq[i] < self.freq[j]
    
    def gt(self, i, j):
        if self.freq[i] == self.freq[j]:
            return self.val[i] > self.val[j]
        return self.freq[i] > self.freq[j]

    def up(self, p):
        while p > 0:
            fa = (p - 1) // 2
            if self.cmp_func[self.root_type](p, fa):
                self.swap(fa, p)
                p = fa
            else:
                break

    def down(self, p):
        while p + p + 1 < self.size:
            left = p + p + 1
            right = p + p + 2

            child = left
            if right < self.size and self.cmp_func[self.root_type](right, left):
                child = right
            
            if self.cmp_func[self.root_type](child, p):
                self.swap(child, p)
                p = child
            else:
                break
    
    def top(self):
        if not self.val:
            return (None, None)
        return (self.val[0], self.freq[0])
    
    def pop(self):
        res = self.top()
        if res[0] is None:
            return res

        self.swap(self.size - 1, 0)
        self.size -= 1
        self.s -= self.val[-1] * self.freq[-1]

        self.index.pop(self.val[-1])
        self.val.pop()
        self.freq.pop()

        if self.size > 0:
            self.down(0)
        
        return res

    def get_size(self):
        return self.size
    
    def get_sum(self):
        return self.s

    def contained(self, v):
        return v in self.index

    def __str__(self):
        val_str = ', '.join([str(x) for x in self.val])
        freq_str = ', '.join([str(x) for x in self.freq])
        index_str = ', '.join(["{}: {}".format(key, value) for key, value in self.index.items()])
        res = "val: {}\nfreq: {}\nindex: {}\ns: {}\nsize: {}".format(val_str, freq_str, index_str, self.s, self.size)
        return res

class Solution(object):
    def findXSum(self, nums, k, x):
        """
        :type nums: List[int]
        :type k: int
        :type x: int
        :rtype: List[int]
        """
        
        s_heap = HeapWithFreq(0)
        g_heap = HeapWithFreq(1)

        for index in range(k):
            s_heap.insert(nums[index])

        while s_heap.get_size() > x:
            sv, sf = s_heap.pop()
            g_heap.insert(sv, sf)

        res = [s_heap.get_sum()]

        for index in range(k, len(nums)):
            if g_heap.contained(nums[index]):
                g_heap.insert(nums[index])
            else:
                s_heap.insert(nums[index])

            if s_heap.contained(nums[index - k]):
                s_heap.delete(nums[index - k])
            else:
                g_heap.delete(nums[index - k])

            if s_heap.get_size() > x:
                sv, sf = s_heap.pop()
                g_heap.insert(sv, sf)
            
            if s_heap.get_size() < x and g_heap.get_size() > 0:
                gv, gf = g_heap.pop()
                s_heap.insert(gv, gf)

            if g_heap.get_size() > 0:    
                sv, sf = s_heap.top()
                gv, gf = g_heap.top()
                if sf < gf or (sf == gf and sv < gv):
                    s_heap.pop()
                    s_heap.insert(gv, gf)
                    g_heap.pop()
                    g_heap.insert(sv, sf)

            res.append(s_heap.get_sum())
    
        return res
```
