---
title: "3302. 字典序最小的合法序列"
aliases: ["yiduobo的每日leetcode 3302.字典序最小的合法序列"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/greedy", "leetcode/string", "题单/滑动窗口与双指针", "题单/动态规划", "题单/滑动窗口与双指针/四-双序列双指针", "题单/动态规划/专题-前后缀分解"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1002369123"
zhihu_id: "1002369123"
zhihu_title: "yiduobo的每日leetcode 3302.字典序最小的合法序列"
question_id: "3302"
question: "字典序最小的合法序列"
problem_url: "https://leetcode.cn/problems/find-the-lexicographically-smallest-valid-sequence/"
difficulty: "Medium"
rating: 2474
created: "2024-10-14T03:26:54+08:00"
updated: "2024-10-14T03:26:54+08:00"
upvotes: 1
comments: 0
---

# 3302. 字典序最小的合法序列

> **[yiduobo的每日leetcode 3302.字典序最小的合法序列](https://zhuanlan.zhihu.com/p/1002369123) · 知乎 · 2024-10-14 · 赞同 1**
> 力扣：[3302. 字典序最小的合法序列](https://leetcode.cn/problems/find-the-lexicographically-smallest-valid-sequence/) · Medium · 灵茶山艾府：[前后缀分解 + 子序列匹配 + 贪心（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3302.字典序最小的合法序列

[. - 力扣（LeetCode）](https://leetcode.cn/problems/find-the-lexicographically-smallest-valid-sequence/)

题目给出两个字符串word1和word2，要求找出一个字典序最小的下标序列，满足这个下标序列在word1中对应的子序列形成的字符串与word2几乎相等。

几乎相等的定义为，如果一个字符串x修改至多一个字符可以变成y，那么就称x与y几乎相等。

题目中关于几乎相等的定义为不修改或者仅修改一个字符，那么在这里不妨先考虑简单的情况，即不修改时应该如何选取这个下标序列。对于这个问题，只需对word2进行一趟遍历，尽量使用word1中靠前的字符来匹配word2当前遍历遍历到达的字符就行了，这样做的理由是既保留了尽量多的字符留给后续的匹配使用，同时又满足了字典序最小的要求。

接下来考虑允许替换一个字符时应该如何处理。不妨设替换后的字符与word2[index]匹配，那么对于word2[0 : index]这个前缀，最优的匹配方式依然不变，因此在这里可以先按照不替换的方式计算一次最优的匹配位置，记为数组left供后续使用。另一方面，对于word2[index + 1:]这个后缀，则应该从word1中被修改的那个下标加1，也就是left[index - 1] + 1开始，重新执行上面的算法来为这个后缀选取匹配的子序列。在这里需要特别注意的是，如果修改的是word2[0]对应的下标，那么在这里就不存在left[index - 1]了，此时则应该修改word1[0]。

由于选取子序列的算法是O(n)的，在这里如果枚举修改哪个字符的话时间复杂度就会来到O(n^2)了，因此在这里就需要先想办法确定好修改的下标，然后再计算出对应的匹配子序列得到最终答案。

不妨设现在需要修改的是word2[index]对应的下标，那么在这里就需要满足：

1、left[index] > index：

理由很简单。如果left[index] \= index的话，说明目前的word2[:index + 1]是word1的前缀，而当前的left已经是按照最优的方式在与word2进行匹配了，无需修改。特别的，如果left[-1] \= len(word2) - 1，说明word2整个字符串都是word1的前缀，此时直接返回left数组即可。

2、index \= 0或者left[index - 1]存在：

index \= 0的情况上面已经讨论过了，而对于index > 0的情况，如果left[index - 1]不存在，说明到word2[index - 1]这里就已经无法找出可以匹配的子序列了，此时修改word2[index]的匹配项无济于事

3、在满足以上两点的前提下，index应该尽量小：

题目要求答案的字典序最小，那么就应该尽量让答案靠前的位置上变小，因此index越小越好

4、word1从修改位置开始的后缀中存在子序列可以匹配上word2[index + 1:]：

题目虽然是要找最优的匹配，但是在这里只要能确认了存在可行的匹配，那么接下来就可以通过一趟遍历找出最优的匹配并直接返回答案。为了适配这一点，在这里可以通过反向遍历，记录从word1中反向选出子序列来匹配word2的后缀的下标序列right，那么只需要满足right[index + 1]大于修改点，就说明存在可用的子序列了

根据以上的结论，就可以先正反两趟遍历，以尽可能匹配为准则得到在不修改时的最优前缀下标序列left以及最优后缀下标序列right。接下来若left[-1] \= len(word2) - 1，则直接返回left，否则从0到len(word2) - 1进行一趟遍历，找出最靠前的可修改位置。

对于当前遍历到的下标index，首先需要满足left[index] !\= index，接下来若index \= 0，记修改位置change_point \= 0，否则若left[index - 1]存在，那么记change_point \= left[index - 1] + 1。若都不满足，则继续向后考虑index + 1。

在得到change_point后，若当前的index \= len(word2) - 1，即当前修改的是word2最后的字符匹配的位置，或者right[index + 1] > change_point，即word1中从change_point + 1开始的后缀中存在子序列可以匹配word2[index + 1]，那么说明change_point就是应该选择的修改点。此时只需要从change_point + 1开始往后遍历，尽量匹配word2[index + 1]中的字符就行了。得到的子序列与left[:index]已经change_point拼接起来即为最终答案。

最后附上python代码：

```python
class Solution(object):
    def validSequence(self, word1, word2):
        """
        :type word1: str
        :type word2: str
        :rtype: List[int]
        """

        left = []
        p = 0
        for char in word2:
            while p < len(word1) and word1[p] != char:
                p += 1
            
            if p == len(word1):
                break
            
            left.append(p)
            p += 1
        
        left.extend([-1] * (len(word2) - len(left)))
    
        if left[-1] == len(word2) - 1:
            return left

        right = []
        p = len(word1) - 1
        for char in word2[::-1]:
            while p >= 0 and word1[p] != char:
                p -= 1
            
            if p < 0:
                break
            
            right.append(p)
            p -= 1
        
        right.extend([-1] * (len(word2) - len(right)))
        right.reverse()

        for index in range(len(word2)):
            if left[index] == index:
                continue
                
            if index == 0:
                change_point = 0
            elif left[index - 1] == -1:
                break
            else:
                change_point = left[index - 1] + 1

            if change_point < len(word1) and (index == len(word2) - 1 or right[index + 1] > change_point):
                res = left[:index] + [change_point]
                p = change_point + 1
                for char in word2[index + 1:]:
                    while word1[p] != char:
                        p += 1
                    res.append(p)
                    p += 1
                
                return res

        return []
```
