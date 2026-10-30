---
title: 本地 py 与 Hot100 对照复核
tags: [leetcode, hot100, review]
---

# 本地 py 与 Hot100 对照复核

## 第二轮结果

- 已有精确匹配：18 个 py 文件 / 14 条题目映射记录
- 第二轮新增精确匹配：0 个
- 第二轮策略：读取函数名、注释、标题关键词，只在高置信度下才认定为同题。

## 第二轮新增精确匹配

- 无。剩余文件里没有发现足够可靠的“同一道 Hot100 题”证据。

## 相关变体（非同题，不强行并入 Hot100 题解）

- [167.py](obsidian://open?vault=Leetcode&file=167.py) → [1. 两数之和](001-1-两数之和.md) · 题型接近：twoSum，有序数组的双指针变体 · defs: `twoSum`
- [92.py](obsidian://open?vault=Leetcode&file=92.py) → [206. 反转链表](023-206-反转链表.md) · 题型接近：reverseBetween，属于反转链表的区间反转变体 · defs: `reverseBetween`

## 可按分类参考的本地练习（非精确匹配）

### [二叉树](categories/二叉树.md)

- [100.py](obsidian://open?vault=Leetcode&file=100.py) · defs: `isSameTree / isSameTree / isSameTree`
- [110.py](obsidian://open?vault=Leetcode&file=110.py) · defs: `isBalanced / get_height / isBalanced / get_height / isBalanced`
- [111.py](obsidian://open?vault=Leetcode&file=111.py) · defs: `minDepth / dfs / minDepth / dfs / minDepth`
- [2236.py](obsidian://open?vault=Leetcode&file=2236.py) · defs: `checkTree / checkTree / checkTree`

### [滑动窗口](categories/滑动窗口.md)

- [209.py](obsidian://open?vault=Leetcode&file=209.py) · defs: `minSubArrayLen / minSubArrayLen`
- [713.py](obsidian://open?vault=Leetcode&file=713.py) · defs: `numSubarrayProductLessThanK / numSubarrayProductLessThanK`

### [链表](categories/链表.md)

- [237.py](obsidian://open?vault=Leetcode&file=237.py) · defs: `deleteNode`
- [707.py](obsidian://open?vault=Leetcode&file=707.py) · defs: `__init__ / __init__ / get / addAtHead / addAtTail`
- [86.py](obsidian://open?vault=Leetcode&file=86.py) · defs: `partition / partition / reverseList / reverseList`

### [二分查找](categories/二分查找.md)

- [852.py](obsidian://open?vault=Leetcode&file=852.py) · defs: `peakIndexInMountainArray`

### [矩阵](categories/矩阵.md)

- [363.py](obsidian://open?vault=Leetcode&file=363.py) · defs: `maxSumSubmatrix`
- [867.py](obsidian://open?vault=Leetcode&file=867.py) · defs: `transpose`

## 工具/辅助文件

- [ListNode.py](obsidian://open?vault=Leetcode&file=ListNode.py) · defs: `无明显函数名`
- [doubly_linked_list.py](obsidian://open?vault=Leetcode&file=doubly_linked_list.py) · defs: `__init__ / createDoublyLinkedList / __init__ / __init__ / add_last`
- [singly_linked_list.py](obsidian://open?vault=Leetcode&file=singly_linked_list.py) · defs: `__init__ / __init__ / __init__ / createLinkedList / __init__`

## 仍未归类

- [1281.py](obsidian://open?vault=Leetcode&file=1281.py) · defs: `subtractProductAndSum`
- [1422.py](obsidian://open?vault=Leetcode&file=1422.py) · defs: `maxScore / maxScore / maxScore`
- [1470.py](obsidian://open?vault=Leetcode&file=1470.py) · defs: `shuffle`
- [1486.py](obsidian://open?vault=Leetcode&file=1486.py) · defs: `xorOperation / xorOperation`
- [1512.py](obsidian://open?vault=Leetcode&file=1512.py) · defs: `numIdenticalPairs / numIdenticalPairs / numIdenticalPairs / numIdenticalPairs`
- [1534.py](obsidian://open?vault=Leetcode&file=1534.py) · defs: `countGoodTriplets / countGoodTriplets / countGoodTriplets`
- [2235.py](obsidian://open?vault=Leetcode&file=2235.py) · defs: `sum`
- [231.2.py](obsidian://open?vault=Leetcode&file=231.2.py) · defs: `isPowerOfTwo / isPowerOfTwo`
- [2413.py](obsidian://open?vault=Leetcode&file=2413.py) · defs: `smallestEvenMultiple / smallestEvenMultiple / smallestEvenMultiple`
- [2469.py](obsidian://open?vault=Leetcode&file=2469.py) · defs: `convertTemperature`
- [258.py](obsidian://open?vault=Leetcode&file=258.py) · defs: `addDigits / addDigits`
- [2586.py](obsidian://open?vault=Leetcode&file=2586.py) · defs: `vowelStrings`
- [263.py](obsidian://open?vault=Leetcode&file=263.py) · defs: `isUgly`
- [303.py](obsidian://open?vault=Leetcode&file=303.py) · defs: `无明显函数名`
- [326.3.py](obsidian://open?vault=Leetcode&file=326.3.py) · defs: `isPowerOfThree / isPowerOfThree`
- [445.py](obsidian://open?vault=Leetcode&file=445.py) · defs: `无明显函数名`
- [709.py](obsidian://open?vault=Leetcode&file=709.py) · defs: `toLowerCase`
