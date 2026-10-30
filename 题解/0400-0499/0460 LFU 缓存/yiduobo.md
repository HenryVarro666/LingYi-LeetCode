---
title: "460. LFU缓存"
aliases: ["yiduobo的每日leetcode 460.LFU缓存"]
tags: ["leetcode", "yiduobo", "leetcode/hard", "leetcode/hash-table", "leetcode/linked-list", "leetcode/doubly-linked-list", "题单/常用数据结构", "题单/链表-二叉树与回溯", "题单/常用数据结构/编程能力强化训练", "题单/链表-二叉树与回溯/一-链表"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/220517020"
zhihu_id: "220517020"
zhihu_title: "yiduobo的每日leetcode 460.LFU缓存"
question_id: "460"
question: "LFU 缓存"
problem_url: "https://leetcode.cn/problems/lfu-cache/"
difficulty: "Hard"
created: "2020-09-06T22:54:25+08:00"
updated: "2020-09-06T22:54:25+08:00"
upvotes: 0
comments: 0
---

# 460. LFU缓存

> **[yiduobo的每日leetcode 460.LFU缓存](https://zhuanlan.zhihu.com/p/220517020) · 知乎 · 2020-09-06 · 赞同 0**
> 力扣：[460. LFU 缓存](https://leetcode.cn/problems/lfu-cache/) · Hard · 灵茶山艾府：[【图解】一张图秒懂 LFU！（Python/Java/C++/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

460.LFU缓存<https://leetcode-cn.com/problems/lfu-cache/>

这一题乍一看跟之前做过的432题很像（传送门在这里[yiduobo：yiduobo的每日leetcode 432.全O(1)的数据结构](https://zhuanlan.zhihu.com/p/196788507)），但是有一个重要的区别是，这一题的删除操作必然是插入操作引发的，而在删除频率最小的节点之后，新插入的节点频率必然为1，即此时的最小频率必然是1，因此相比432题，这一题可以省略竖直链表的部分，同时使用一个min_freq来储存当前最小的频率值。

于是现在的做法就变成了维护若干条双向链表，每条链表的中节点的freq都相同。然后维护一个key_dict与一个head_dict，前者为key到链表中节点的映射，而后者为freq到链表中头部节点的映射。那么对于题目要求的两种操作：

1、get操作。若此时key存在于key_dict中，那么通过key_dict找出对应的节点node，然后提取出node的频率freq。接下来就需要将node从当前双向链表中删去，然后将freq加一，再将node插入到freq + 1对应的双向链表中。

首先是删除，先通过freq与head_dict定位到freq对应链表的头部节点head：

1)若node不是head：此时之间将node的左右节点链接上即可。

2)若node就是head，且head的左侧还是head：说明此时freq对应的链表中只有node这一个节点，于是直接从head_dict中pop掉freq即可。

3)若node就是head，且head的左侧还有其他节点：此时应该将node我的左右节点链接上，同时freq对应链表的新头部节点应该是node的右侧节点，于是将head_dict[freq]指向到head.right即可。

接下来是插入：

1)若freq + 1不存在于head_dict中：说明此时还没有freq + 1对应的链表，于是将node的左右指向自身，同时将head_dict[freq + 1]指向到node即可。

2)若freq + 1存在于head_dict中：此时node是freq + 1这条链表中最新操作过的，因此应该将其作为freq + 1这条链表的新头部节点。于是先通过head_dict与freq + 1找出头部节点head，然后将node插入到head节点的左侧，最后将head_dict[freq + 1]指向到node即可。

完成上述操作之后，需要判断当前的min_freq是否恰好就是node的freq。若相等，且此时freq不存在于head_dict中，说明此时碰到了删除中的情况2)，即唯一的频率为freq的节点node，其频率升级到了freq + 1，因此此时应该将min_freq同步升级到freq + 1。

2、put操作。若此时put的key存在于key_dict中，那么其具体操作与get操作完全一致。若key不存在于key_dict中，那么有两种情况：

1)现有节点数不到capacity：那么就新增一个节点，freq为1，并将其插入到freq为1对应的链表中。插入操作的细节与get操作中一致。

2)现有节点数已经到了capacity：此时就应该删除min_freq对应链表中的最右侧节点node，该节点可以通过head_dict与min_freq定位到head节点，而head.right即为要删除的节点node。从链表中删除完成后，可以将node的key与val重置为要插入的key与val，并将其freq重置为1，再将其插入到freq为1对应的链表中去。删除与插入操作的细节与get操作中一致。

无论是那种情况，都新插入了一个freq为1的节点，因此需要将min_freq置为1。

至此，就可以在O(1)的时间复杂度内完成题目要求的两种操作了。

最后附上python代码：

```python
class ListNode(object):

    def __init__(self, key, val):
        self.left = None
        self.right = None
        self.key = key
        self.val = val
        self.freq = 1

class LFUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.capacity = capacity
        self.min_freq = None
        self.key_dict = {}
        self.head_dict = {}

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if key not in self.key_dict:
            return -1
        
        node = self.key_dict[key]
        freq = node.freq
        head = self.head_dict[freq]
        if node == head:
            if head.left == head:
                self.head_dict.pop(freq)
            else:
                head.left.right = head.right
                head.right.left = head.left
                self.head_dict[freq] = head.right
        else:
            node.left.right = node.right
            node.right.left = node.left

        node.freq += 1
        if node.freq in self.head_dict:
            head = self.head_dict[node.freq]
            head.left.right = node
            node.left = head.left
            node.right = head
            head.left = node
        else:
            node.left = node.right = node
        self.head_dict[node.freq] = node

        if self.min_freq == freq and freq not in self.head_dict:
            self.min_freq += 1

        return node.val

    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: None
        """
        
        if key in self.key_dict:
            node = self.key_dict[key]
            freq = node.freq
            head = self.head_dict[freq]
            if node == head:
                if node.left == head:
                    self.head_dict.pop(freq)
                else:
                    head.left.right = head.right
                    head.right.left = head.left
                    self.head_dict[freq] = head.right
            else:
                node.left.right = node.right
                node.right.left = node.left

            node.freq += 1
            if node.freq in self.head_dict:
                head = self.head_dict[node.freq]
                head.left.right = node
                node.left = head.left
                node.right = head
                head.left = node
            else:
                node.left = node.right = node
            self.head_dict[node.freq] = node

            if self.min_freq == freq and freq not in self.head_dict:
                self.min_freq += 1

            node.val = value

        else:
            if len(self.key_dict) < self.capacity:
                node = ListNode(key, value)
            elif self.capacity > 0:
                head = self.head_dict[self.min_freq]
                node = head.left
                if node == head:
                    self.head_dict.pop(self.min_freq)
                else:
                    node.left.right = node.right
                    node.right.left = node.left
                self.key_dict.pop(node.key)

                node.key = key
                node.val = value
                node.freq = 1
            else:
                return
            
            if 1 not in self.head_dict:
                self.min_freq = 1
                node.left = node.right = node
            else:
                head = self.head_dict[1]
                head.left.right = node
                node.left = head.left
                node.right = head
                head.left = node
            self.head_dict[1] = node
            self.key_dict[key] = node

# Your LFUCache object will be instantiated and called as such:
# obj = LFUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
```
