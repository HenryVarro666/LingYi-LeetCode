---
title: "941. 有效的山脉数组"
aliases: ["yiduobo的每日leetcode 941.有效的山脉数组"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/358472323"
zhihu_id: "358472323"
zhihu_title: "yiduobo的每日leetcode 941.有效的山脉数组"
question_id: "941"
question: "有效的山脉数组"
problem_url: "https://leetcode.cn/problems/valid-mountain-array/"
created: "2021-03-19T22:50:58+08:00"
updated: "2021-03-19T22:50:58+08:00"
upvotes: 0
comments: 0
---

# 941. 有效的山脉数组

> **[yiduobo的每日leetcode 941.有效的山脉数组](https://zhuanlan.zhihu.com/p/358472323) · 知乎 · 2021-03-19 · 赞同 0**
> 力扣：[941. 有效的山脉数组](https://leetcode.cn/problems/valid-mountain-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

941.有效的山脉数组

[力扣](https://leetcode-cn.com/problems/valid-mountain-array/)

采用一个标记表示当前数组是上升还是下降的，然后一趟遍历考察当前处理的数字arr[index]与arr[index - 1]的大小关系与当前的标记：

1、若arr[index]等于arr[index - 1]，那么arr必然不是山脉数组

2、若此时标记为空，说明此时对比的是arr[0]与arr[1]。若此时arr[0] > arr[1]，说明一开始就出现了下降，那么arr必然不是山脉数组，否则置标记为上升

3、若此时标记为上升，且此时arr[index] \< arr[index - 1]，说明这里就是山脉的顶峰，马上要开始下降了，于是置标记为下降

4、若此时标记为下降，且arr[index] > arr[index - 1]，说明此时出现了上升，但此时应当是下降区间，因此arr必然不是山脉数组

遍历完成后，若此时标记不为下降，说明arr没有下降区间，因此返回false，否则返回true

最后附上python代码：

```python
class Solution(object):
    def validMountainArray(self, arr):
        """
        :type arr: List[int]
        :rtype: bool
        """

        if len(arr) < 3:
            return False
        
        flag = 0
        for index in range(1, len(arr)):
            if arr[index] == arr[index - 1]:
                return False
            if flag == 0:
                if arr[index] < arr[index - 1]:
                    return False
                else:
                    flag = 1
            elif flag == 1:
                if arr[index] < arr[index - 1]:
                    flag = 2
            elif arr[index] > arr[index - 1]:
                    return False

        return flag == 2
```
