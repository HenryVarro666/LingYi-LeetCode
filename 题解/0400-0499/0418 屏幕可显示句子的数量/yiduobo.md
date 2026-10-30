---
title: "418. 屏幕可显示句子的数量"
aliases: ["yiduobo的每日leetcode 418.屏幕可显示句子的数量"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/599141758"
zhihu_id: "599141758"
zhihu_title: "yiduobo的每日leetcode 418.屏幕可显示句子的数量"
question_id: "418"
question: "屏幕可显示句子的数量"
problem_url: "https://leetcode.cn/problems/sentence-screen-fitting/"
created: "2023-01-15T04:02:16+08:00"
updated: "2023-01-15T04:02:16+08:00"
upvotes: 0
comments: 2
---

# 418. 屏幕可显示句子的数量

> **[yiduobo的每日leetcode 418.屏幕可显示句子的数量](https://zhuanlan.zhihu.com/p/599141758) · 知乎 · 2023-01-15 · 赞同 0**
> 力扣：[418. 屏幕可显示句子的数量](https://leetcode.cn/problems/sentence-screen-fitting/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题解

418.屏幕可显示句子的数量

[力扣](https://leetcode.cn/problems/sentence-screen-fitting/)

首先，注意到题目中的单词不能跨行，因此不能直接使用除法，而是需要使用枚举或者二分来处理单词跨行的情况。另一方面，对于不跨行的情况，则必须使用除法来计算，因此列的取值范围较大，必须使用除法快速计算出在不跨行的情况下当前行可以容纳多少个完成的句子。

我在这里采用的是模拟加哈希的方式来处理跨行的句子，因为句子自身是固定的，也就意味着固定了句子的起点后，其重点也同样是固定的，因此可以将所有模拟跨行的结果都以句子的起始位置为key储存起来，在后续遇到相同情况时就可以直接定位到句子的终点了。

另外，由于非首次填充时都要与上一个单词之间用一个空格来进行分隔，因此可以使用一个标记变量first来表示当前是否为首次填充。当first为false时，在计算单词或句子占据空间时需要额外加上1，表示用来间隔的空格占据的空间。

根据上面两个结论，就得到了一种算法：

1、首先遍历句子中的单词，若其中某个单词的长度超过了列宽，那么答案就必然为0，否则统计所有单词的长度之和，记为s。得到s之后，由于句子的单词之间必须有空格分隔，因此一个句子实际占据的长度应该是s加上空格的数量，也就是单词数组的长度减1，使用这个值来更新s。

2、接下来开始进行填充。使用两个变量x和y分别表示当前填充操作进行到了第几行第几列。当x还没到达屏幕底部时：

2-1）首先考虑不跨行的整句填充。

若当前的y + s + delta \<\= cols，那么说明可以从y开始进行至少一次不跨行的整句填充。其中delta表示间隔空格占用的位置，也就是上面提到的first转化而来的值。

这种情况下，应该首先进行一次整句填充，将y移动到s + y + delta，同时将答案加上1，并置first为false。接下来，尝试更多的整句填充，这里就要用到除法了。从此时的y开始，每次不跨行整句填充的代价都是s + 1，因此接下来可以填充的整句数量就是tmp \= (cols - y) / (s + 1)，此时应该将其累加到res，同时将y向后移动到y + tmp \* (s + 1)。

2-2）接下来，当前行剩余的空格已经无法在进行不跨行的整句填充的，但是剩余的位置可能还能容纳一些单词，因此需要开始枚举哪些单词可以被填充进来。在这里可以使用上面提到的模拟加哈希的方式。

若当前的y已经出现在了哈希表f中，那么就从中取出填充整个句子需要的行数偏移量以及填充完之后列的位置。将行数偏移量累加至x，同时将y更新为填充后的列的位置。若此时x超出了边界，说明已经无法再进行填充，那么直接返回res，反之若x还没有超出边界，那么就将x加上1，然后回到上面的2-1

若y还没有出现在哈希表中，那么就需要枚举每个单词逐个进行填充。具体实现上，计算填充当前枚举到的单词后y的位置，若y没有越界，那么就可以进行填充，否则需要将x加上1，然后将y置为当前单词的长度。需要注意的是，在这里同样需要考虑间隔符的影响，也就是需要将first考虑进来。同样的，这种情况下如果x超出了边界，那么就直接返回res，否则就将x加上1，然后继续考虑下一个单词。在填充完所有单词后，需要将填充开始前的y作为key，当前的x与填充开始前的x之差以及当前的y作为value加入到哈希表中，提高后续计算的效率。

最后附上python代码：

```python
class Solution(object):
    def wordsTyping(self, sentence, rows, cols):
        """
        :type sentence: List[str]
        :type rows: int
        :type cols: int
        :rtype: int
        """

        s = 0
        for word in sentence:
            if len(word) > cols:
                return 0
            s += len(word)
        
        s += len(sentence) - 1

        x = 0
        y = 0
        first = True
        f = {}
        res = 0
        while x < rows:
            if first:
                delta = 0
            else:
                delta = 1

            if s + y + delta <= cols:
                y += s + delta
                res += 1
                first = False
            
                tmp = (cols - y) / (s + 1)
                res += tmp
                y += tmp * (s + 1)

            if y in f:
                x += f[y][0]
                y = f[y][1]
                if x >= rows:
                    return res
                else:
                    res += 1
                
                continue
            
            last_x, last_y = x, y
            for word in sentence:
                if first:
                    delta = 0
                else:
                    delta = 1

                if y + len(word) + delta <= cols:
                    y += len(word) + delta
                else:
                    x += 1
                    if x == rows:
                        return res
                    y = len(word)

                first = False

            res += 1
            f[last_y] = [x - last_x, y]

        return res
```
