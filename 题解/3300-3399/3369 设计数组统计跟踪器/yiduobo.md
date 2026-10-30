---
title: "3369. 设计数组统计跟踪器"
aliases: ["yiduobo的每日leetcode 3369.设计数组统计跟踪器"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/28239232650"
zhihu_id: "28239232650"
zhihu_title: "yiduobo的每日leetcode 3369.设计数组统计跟踪器"
question_id: "3369"
question: "设计数组统计跟踪器"
problem_url: "https://leetcode.cn/problems/design-an-array-statistics-tracker/"
created: "2025-03-05T23:46:48+08:00"
updated: "2025-03-05T23:46:48+08:00"
upvotes: 1
comments: 0
---

# 3369. 设计数组统计跟踪器

> **[yiduobo的每日leetcode 3369.设计数组统计跟踪器](https://zhuanlan.zhihu.com/p/28239232650) · 知乎 · 2025-03-05 · 赞同 1**
> 力扣：[3369. 设计数组统计跟踪器](https://leetcode.cn/problems/design-an-array-statistics-tracker/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3369.设计数组统计跟踪器

[3369. 设计数组统计跟踪器 - 力扣（LeetCode）](https://leetcode.cn/problems/design-an-array-statistics-tracker/description/)

题目要求设计一种数据结构，可以实现一下功能：

1、addNumber(number)：作用是将number添加到数据结构中

2、removeFirstAddedNumber()：作用是从数据结构中删去最早添加的数字

3、getMedian()：作用是返回数据结构中数字向下取整的平均值

4、getMedian()：作用是返回数据结构中数字的中位数

5、getMode()：作用是返回数据结构中数字的众数。若由多少，则返回值最小的那个。

题目保证数值不超过10^9，总的操作数不超过10^5，且后面4种操作调用时数据结构不为空。

题目的数据规模不小，必须高效实现每种操作。

接下来对各种操作进行分析：

1、addNumber(number)：

无法通过添加操作决定应该使用哪种数据结构。实际上，应该是通过其他操作决定使用哪种数据结构，再决定如何实现添加操作，所以添加操作的具体实现方法放在最后再回头来看。

2、removeFirstAddedNumber()：

由于需要删除最早添加的元素，说明在这里就需要一个队列q，利用先进先出的特性来进行适配。

除此之外，对于其他操作所需的删除操作同样需要最后再回头来看。

3、getMedian()：

计算平均数是比较好做的，只需使用一个变量s记录当前数据结构中的元素之和，然后再利用q的长度得到数据结构中元素的数目，二者相除就是平均数。s的更新应该在addNumber和removeFirstAddedNumber中完成。

4、getMedian()：

计算中位数是最复杂的部分。对于本题，可以参考之前480题的处理方法，使用两个堆big_heap以及small_heap分别储存当前数据结构中值较大的一半元素和值较小的另一半元素，其中big_heap是小顶堆，small_heap为大顶堆。在这里只需保证big_heap的大小big_size大于等于small_heap的大小small_size，且big_size最多比small_size多出1，就能保证big_heap的堆顶元素就是数据结构中元素的中位数。

[yiduobo：yiduobo的每日leetcode 480.滑动窗口中位数](https://zhuanlan.zhihu.com/p/246224986)

与480题不同的是，480题每次窗口滑动都将带来一次add和remove操作，但是本题中的add和remove不是绑定的，因此需要时刻根据两个堆的大小来维护这两个堆。

另外需要注意的是，python的heapq里面的堆是不支持删除指定元素操作的，所以在这里要么自己手搓一个，要么采用懒删除的方法，将需要删除的元素记录下来，当堆顶元素是需要删除的元素时再执行删除操作。我在这里选择的是后面这种懒删除的做法，因此还需两个哈希表big_removed和small_removed记录两个堆中应该删去的元素以及对应的删除次数。

5、getMode()：

对于众数操作，首先需要一个哈希表freq记录每种元素在堆中出现的次数。除此之外，为了高效得到次数最多且数值最小的元素，则还需要一个堆freq_heap，以出现次数为第一关键字，数值为第二关键字来维护每种元素出现的次数。另外对于删除操作，在这里可以通过对比freq中元素出现的次数与堆顶元素出现次数是否一致，来变相实现懒删除的功能。

---

综合上面几点可以发现，需要：

一个队列q记录元素加入数据结构的顺序，用来得到最早加入数据结构中的元素

一个整数变量s记录数据结构中的元素和，用来计算平均数

一个小顶堆big_heap和一个大顶堆small_heap，用来记录数据结构中较大的一半元素以及较小的另一半元素。另外还需要big_size、small_size记录堆的大小，以及懒删除使用的哈希表big_removed、small_removed。通过上面这些组件来维护数据结构的中位数。

一个哈希表freq记录元素出现次数，以及一个堆freq_heap，用来获取众数。

---

到了这里，还有最开始没有讨论完的addNumber(number)以及removeFirstAddedNumber()操作。

对于addNumber(number)：

先将number加入q中，然后将number累加到s中。

接下来先清理两个堆顶已经被删除的元素，然后根据number与big_heap堆顶元素的大小关系判断number应该加入到哪个堆中，并修正对应堆的大小，然后维护两个堆大小的平衡。

最后更新number在freq中出现的次数，然后将新的次数freq[number]以及number加入到freq_heap中。

而对于removeFirstAddedNumber()：

先获取需要删除的元素，也就是q的最左侧元素，在这里记为number。

得到number后，先将number中s中减去。

接下来先清理两个堆顶已经被删除的元素，然后根据number与big_heap堆顶元素的大小关系判断number当前处于哪个堆中，并修改对应的removed哈希表，同时修正对应堆的大小，然后维护两个堆大小的平衡。

最后更新number在freq中出现的次数，然后将新的次数freq[number]以及number加入到freq_heap中。

最后附上python代码：

```python
class StatisticsTracker(object):

    def __init__(self):
        self.q = deque()

        self.s = 0

        self.big_heap = []
        self.big_size = 0
        self.big_removed = {}
        self.small_heap = []
        self.small_size = 0
        self.small_removed = {}

        self.freq = {}
        self.freq_heap = []

    def remove(self):
        while self.small_heap and self.small_removed.get(-self.small_heap[0], 0) > 0:
            self.small_removed[-self.small_heap[0]] -= 1
            heapq.heappop(self.small_heap)
        
        while self.big_heap and self.big_removed.get(self.big_heap[0], 0) > 0:
            self.big_removed[self.big_heap[0]] -= 1
            heapq.heappop(self.big_heap)

    def maintainHeap(self):
        if self.small_size <= self.big_size <= self.small_size + 1:
            return

        if self.small_size > self.big_size:
            from_heap = self.small_heap
            to_heap = self.big_heap
            self.small_size -= 1
            self.big_size += 1
        else:
            from_heap = self.big_heap
            to_heap = self.small_heap
            self.small_size += 1
            self.big_size -= 1

        heapq.heappush(to_heap, -heapq.heappop(from_heap))

    def addNumber(self, number):
        """
        :type number: int
        :rtype: None
        """
        self.q.append(number)
        self.s += number

        self.remove()
        if self.big_size == 0 or number >= self.big_heap[0]:
            heapq.heappush(self.big_heap, number)
            self.big_size += 1
        else:
            heapq.heappush(self.small_heap, -number)
            self.small_size += 1
        self.maintainHeap()
        
        self.freq[number] = self.freq.get(number, 0) + 1
        heapq.heappush(self.freq_heap, (-self.freq[number], number))

    def removeFirstAddedNumber(self):
        """
        :rtype: None
        """
        number = self.q.popleft()
        self.s -= number

        self.remove()
        if self.big_heap[0] <= number:
            self.big_size -= 1
            self.big_removed[number] = self.big_removed.get(number, 0) + 1
        else:
            self.small_size -= 1
            self.small_removed[number] = self.small_removed.get(number, 0) + 1
        
        self.maintainHeap()
        
        self.freq[number] -= 1
        heapq.heappush(self.freq_heap, (-self.freq[number], number))

    def getMean(self):
        """
        :rtype: int
        """
        return self.s // len(self.q)

    def getMedian(self):
        """
        :rtype: int
        """
        
        self.remove()
        return self.big_heap[0]

    def getMode(self):
        """
        :rtype: int
        """
        
        while self.freq[self.freq_heap[0][1]] != -self.freq_heap[0][0]:
            heapq.heappop(self.freq_heap)
        return self.freq_heap[0][1]

# Your StatisticsTracker object will be instantiated and called as such:
# obj = StatisticsTracker()
# obj.addNumber(number)
# obj.removeFirstAddedNumber()
# param_3 = obj.getMean()
# param_4 = obj.getMedian()
# param_5 = obj.getMode()
```
