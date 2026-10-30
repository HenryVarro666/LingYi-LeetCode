CONFIG = dict(
    num=1850, title='邻位交换的最小次数', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='下一个排列 + 贪心换最近',
    tags=[],
    code='''
class Solution(object):
    def getMinSwaps(self, num, k):

        now = list(num)
        n = len(now)
        for _ in range(k):
            for index in range(n - 2, -1, -1):
                if now[index] < now[index + 1]:
                    p = index + 1
                    while p < n and now[p] > now[index]:
                        p += 1
                    p -= 1
                    now[index], now[p] = now[p], now[index]
                    l = index + 1
                    r = n - 1
                    while l < r:
                        now[l], now[r] = now[r], now[l]
                        l += 1
                        r -= 1
                    break
        
        origin = list(num)
        res = 0
        for index in range(n):
            if origin[index] != now[index]:
                p = index + 1
                last = now[index]
                res += 1
                while p < n and now[p] != origin[index]:
                    now[p], last = last, now[p]
                    p += 1
                    res += 1
                now[p] = last

        return res
''',
    call='Solution().getMinSwaps("112", 2)',
    expect=2,
    skip=['l += 1', 'r -= 1', 'l = index + 1', 'r = n - 1', 'p = index + 1', 'res = 0'],
    views=[
        dict(type='text', h=70, fn=lambda S: ('阶段二：把 `origin` 换成目标排列 `now`，统计相邻交换' if 'origin' in S else '阶段一：连续 k 次求「下一个排列」，得到目标 `now`')),
        dict(type='array', var='now', label='now（目标排列）', pointers={'index': 'blue', 'p': 'pink', 'l': 'cyan', 'r': 'orange'}, h=200),
        dict(type='array', var='origin', label='origin（原排列）', pointers={'index': 'blue'}, h=200,
             color=lambda S, i, v: 'green' if 'now' in S and i < len(S['now']) and S['now'][i] == v and 'index' in S and i < S['index'] else None),
    ],
    watch=['k', 'index', 'p', 'last', ('res', 'res', 'green')],
    captions={
        'now = list(num)': '`now` 先拷贝原排列，下面把它原地推进成「之后第 k 个排列」',
        'for _ in range(k)': '重复 `k` 次，每次 `O(n)` 求下一个排列（n 不大，不必用康托展开）',
        'for index in range(n - 2': '`index` 从右往左扫：{"取到 index = " + str(index) if index is not None else ""}',
        'for index in range(n)': '从左到右逐位对齐：{"当前 index = " + str(index)}',
        'if now[index] < now[index + 1]': '从右往左找第一个「升序对」：`now[{index}]={now[index]}` 与 `now[{index+1}]={now[index+1]}` → {"找到了" if now[index] < now[index+1] else "还是降序，继续左移"}',
        'while p < n and now[p] > now[index]': '在右侧降序段里找最后一个比 `now[index]` 大的数',
        'p -= 1': '`p` 退回一步，指向最后一个比 `now[index]` 大的数：`p = {p}`',
        'now[index], now[p] = now[p], now[index]': '交换 `index` 与 `p`：当前位变大一点点 → `{now}`',
        'while l < r': '右侧还是降序，翻转成升序才是最小的后缀：`l = {l}`，`r = {r}`',
        'now[l], now[r] = now[r], now[l]': '翻转后缀：交换 `now[{l}]` 与 `now[{r}]` → `{now}`',
        'break': '下一个排列已得到：`{now}`，结束这一轮',
        'origin = list(num)': '目标排列 `now` 已定。再拷贝原排列到 `origin`，开始统计交换次数',
        'if origin[index] != now[index]': '`origin[{index}]={origin[index]}` vs `now[{index}]={now[index]}` → {"相同，不用动" if origin[index] == now[index] else "不同，要把后面最近的同字符换过来"}',
        'last = now[index]': '`last` 暂存目标位置的字符 `{last}`，它要被逐位后推',
        'res += 1': '至少要有一次邻位交换：`res = {res}`',
        'while p < n and now[p] != origin[index]': '往后找最近的、等于 `origin[{index}]={origin[index]}` 的字符（最近 = 交换最少）',
        'now[p], last = last, now[p]': '`last` 后推一位（相当于一次邻位交换）：`now = {now}`',
        'p += 1': '`p` → {p}',
        'now[p] = last': '找到了最近的相同字符，把 `last` 放到这里：`now = {now}`',
        'return res': '最少需要 `{res}` 次邻位交换',
    },
    max_steps=110,
    cards=dict(
        one_liner='先求之后第 k 个排列，再贪心地从最近处换字符',
        complexity='时间 `O(k·n + n²)`，空间 `O(n)`',
        problem=['`num` 是数字串，「美丽整数」是它的重排且比 `num` 大，求第 `k` 小的美丽整数',
                 '返回把 `num` 变成它所需的==最少相邻交换次数==',
                 '示例：`"11112"`，`k = 4` → `"21111"`，答案 `4`；本视频用 `"112"`，`k = 2` → `"211"`，答案 `2`'],
        quote='若原排列中的某个位置上的字符与之后第k个排列上对应的字符不同，那么就需要将后面的某个相同字符交换过来。一个直观的想法就是将最近的相同字符交换过来。',
        quote_src='—— yiduobo 题解原文',
        idea=['康托展开要 1000 阶乘的高精度，太麻烦；`k` 次 `O(n)` 的「下一个排列」就够了',
              '再从头扫：位置不同就把==最近的相同字符==换过来，不换最近的会多出无用交换',
              '原文提到可用树状数组算位置，但这里直接 `O(n²)` 模拟'],
        summary=['时间 `O(k·n + n²)`，空间 `O(n)`',
                 '下一个排列：从右找升序对 → 与右侧刚好更大的数交换 → 翻转后缀',
                 '贪心换最近的相同字符，每次推移一位计 1 次交换',
                 '原文为 Python 2 风格，本题代码无需改动（`num` 是字符串）'],
    ),
)
