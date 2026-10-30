---
title: "3508. 设计路由器"
aliases: ["yiduobo的每日leetcode 3508.设计路由器"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/queue", "leetcode/hash-table", "leetcode/binary-search", "题单/二分算法", "题单/常用数据结构", "题单/二分算法/一-二分查找", "题单/常用数据结构/四-队列"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1902171355966862662"
zhihu_id: "1902171355966862662"
zhihu_title: "yiduobo的每日leetcode 3508.设计路由器"
question_id: "3508"
question: "设计路由器"
problem_url: "https://leetcode.cn/problems/implement-router/"
difficulty: "Medium"
rating: 1851
created: "2025-05-04T01:43:00+08:00"
updated: "2025-05-04T01:43:00+08:00"
upvotes: 1
comments: 0
---

# 3508. 设计路由器

> **[yiduobo的每日leetcode 3508.设计路由器](https://zhuanlan.zhihu.com/p/1902171355966862662) · 知乎 · 2025-05-04 · 赞同 1**
> 力扣：[3508. 设计路由器](https://leetcode.cn/problems/implement-router/) · Medium · 灵茶山艾府：[哈希表 + 队列 + 二分查找（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3508.设计路由器

[3508. 设计路由器 - 力扣（LeetCode）](https://leetcode.cn/problems/implement-router/description/)

题目要求设计一个数据结构来管理网络路由器中的数据包。每个数据包包含：

source：生成该数据包的机器的唯一标识符

destinacetion：目标机器的唯一标识符

timestamp：该数据包到达路由器的时间戳

现在要求实现Router类：

1、构造函数Router(memoryLimit)：

初始化路由器对象，设置固定的内存限制memoryLimit。其中memoryLimit表示路由器在任意时间点可以储存的最大数据包数量

若某一时刻添加一个新数据包将超过memoryLimit，那么需要移除最老的数据包以腾出空间

2、addPacket(source, destination, timestamp)：

将具有给定属性的数据包添加到路由器中。若路由器中已经存在重复的数据包，则添加失败，返回false，否则添加成功，返回true。

题目保证addPacket操作会按照timestamp的递增顺序进行。

3、forwardPacket()：

以先进先出的顺序转发下一个数据包。需要从路由器中移除掉对应的数据包，并返回这个数据包的[source, destination, timestamp]三元组。若不存在数据包，则返回空数组

4、getCount(destination, startTime, endTime)：

返回当前储存在路由器中，且目的地址为指定的destination，同时时间戳在时间区间[startTime, endTime]内的数据包数量

逐个分析题目中的操作：

1、构造函数Router(memoryLimit)：

首先需要记录memoryLimit。另一方面，由于题目说明了数据包是先进先出的，因此需要使用一个队列q来维护当前在路由器中的数据包

2、addPacket(source, destination, timestamp)：

对于添加操作，题目有了去重的要求，因此需要一个集合packet_set储存目前在路由器中的数据包。key可以直接设置成(source, destination, timestamp)的三元素。

那么若当前添加的数据包的(source, destination, timestamp)不在packet_set中，那么就将其加入到packet_set中，同时将其加入到队列q中。若添加后队列q的大小超过了memoryLimit，则还需要将队首元素从队列中弹出，同时将其从packet_set中移除。

3、forwardPacket()：

若q非空，则弹出队首元素(source, destination, timestamp)，将其从packet_set中删除然后转化为list后返回即可，否则返回空数组。

4、getCount(destination, startTime, endTime)：

在这里需要找出目的地址为特定的destination的数据包中，时间戳处于[startTime, endTime]之间的数据包。在这里就可以使用一个哈希表des_hash单独储存每种destination对应的数据包队列。由于题目保证了addPacket是按照时间戳递增的顺序来的，因此des_hash中储存的数据包的timestamp也必然是单调递增的，在这里就可以在其中二分，找出最小的，且timestamp大于等于startTime的数据包下标，以及最大的，且timestamp小于等于endTime的数据包下标，二者相减即为符合条件的数据包数量。

在具体实现上，由于不确定python中的deque的下标访问是O(n)的还是O(1)的，所以在这里还是采用了数组模拟队列的处理方法，因此在这里还需要额外维护一个哈希表des_left，其中des_left[destination]表示在des_hash[destination]这个数据list中最小的还未被转发的数据包的下标，以这个des_left作为二分的下界。当某个数据包过期或者被转发时，需要将对应的des_left[destination]加上1。

最后附上python代码：

```python
class Router(object):

    def __init__(self, memoryLimit):
        """
        :type memoryLimit: int
        """
        
        self.q = deque()
        self.memoryLimit = memoryLimit
        self.packet_set = set()
        self.des_hash = {}
        self.des_left = {}

    def addPacket(self, source, destination, timestamp):
        """
        :type source: int
        :type destination: int
        :type timestamp: int
        :rtype: bool
        """
        
        key = (source, destination, timestamp)
        if key not in self.packet_set:
            self.packet_set.add(key)
            self.q.append(key)
            if destination not in self.des_hash:
                self.des_hash[destination] = []
                self.des_left[destination] = 0
            self.des_hash[destination].append(timestamp)
            
            if self.memoryLimit < len(self.q):
                rm_key = self.q.popleft()
                self.packet_set.remove(rm_key)
                self.des_left[rm_key[1]] += 1

            return True

        return False

    def forwardPacket(self):
        """
        :rtype: List[int]
        """
        
        res = []
        if self.q:
            key = self.q.popleft()
            res = list(key)
            self.packet_set.remove(key)
            self.des_left[key[1]] += 1
        
        return res

    def getCount(self, destination, startTime, endTime):
        """
        :type destination: int
        :type startTime: int
        :type endTime: int
        :rtype: int
        """
        
        if destination not in self.des_hash:
            return 0
        
        timestamps = self.des_hash[destination]
        left = self.des_left[destination]
        right = len(timestamps) - 1
        if left > right:
            return 0

        if timestamps[-1] < startTime:
            return 0

        if timestamps[left] > endTime:
            return 0
        
        while left < right:
            mid = (left + right) // 2
            if timestamps[mid] < startTime:
                left = mid + 1
            else:
                right = mid
        
        start_index = left

        left = self.des_left[destination]
        right = len(timestamps) - 1
        while left < right:
            mid = (left + right + 1) // 2
            if timestamps[mid] <= endTime:
                left = mid
            else:
                right = mid - 1
        
        end_index = left

        return end_index - start_index + 1
                

# Your Router object will be instantiated and called as such:
# obj = Router(memoryLimit)
# param_1 = obj.addPacket(source,destination,timestamp)
# param_2 = obj.forwardPacket()
# param_3 = obj.getCount(destination,startTime,endTime)
```
