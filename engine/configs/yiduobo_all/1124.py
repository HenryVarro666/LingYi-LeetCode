HOURS = [6, 9, 9, 6, 0, 6, 9, 9]
S_VALS = [-1, 0, 1, 0, -1, -2, -1, 0]


def _txt(S):
    if 's' not in S or 'stack' not in S:
        return '劳累 → 1，不劳累 → -1，求前缀和 `s`，找 `s[i] < s[j]` 且离得最远的一对'
    if 'index' not in S:
        return f'`s = {S["s"]}`'
    return f'`s = {S["s"]}`    栈里的下标 `{S["stack"]}`    res = `{S.get("res", 0)}`'


CONFIG = dict(
    num=1124, title='表现良好的最长时间段', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='前缀和 + 单调栈（候选左端点）',
    tags=['灵神题单·单调栈', '灵神题单·常用数据结构', '难度分 1908'],
    code='''
class Solution(object):
    def longestWPI(self, hours):

        s = [1 if hours[0] > 8 else -1]
        for hour in hours[1:]:
            s.append(s[-1])
            if hour > 8:
                s[-1] += 1
            else:
                s[-1] -= 1
        
        stack = []
        res = 0
        for index in range(len(s)):
            if not stack or s[stack[-1]] > s[index]:
                stack.append(index)
            if s[index] > 0:
                res = max(res, index + 1)

        for index in range(len(s) - 1, -1, -1):
            while stack and s[index] > s[stack[-1]]:
                p = stack.pop()
                if p < index:
                    res = max(res, index - p)
            if not stack:
                break
        
        return res
''',
    call=f'Solution().longestWPI({HOURS!r})',
    expect=7,
    views=[
        dict(type='text', fn=_txt, size=28, h=70),
        dict(type='array', var='hours', label='hours', h=150,
             color=lambda S, i, v: 'pink' if v > 8 else None),
        dict(type='array', var='s', label='s[i]（黄 = 栈里的候选左端点，蓝 = 当前 index）', h=190,
             color=lambda S, i, v: 'blue' if S.get('index') == i else ('yellow' if i in S.get('stack', ()) else None)),
        dict(type='stack', var='stack', label='stack（下标:前缀和，越往上 s 越小）', fmt=lambda i: f'{i}:{S_VALS[i]}', h=120),
    ],
    watch=[('index', 'index', 'blue'), ('stack', 'stack', 'purple'), ('res', 'res', 'green')],
    captions={
        's = [1 if': '第 0 天的前缀和：劳累记 `1`，否则 `-1` → `s = {s}`',
        's.append(s[-1])': '先复制上一个前缀和，再按今天调整',
        's[-1] += 1': '`hour = {hour}` > 8，劳累：`+1` → `{s[-1]}`',
        's[-1] -= 1': '`hour = {hour}` ≤ 8，不劳累：`-1` → `{s[-1]}`',
        'stack = []': '栈保存「可能成为左端点」的下标：只有比之前都更小的 `s` 才有资格',
        'if not stack or': lambda S, B, r: (('栈空，第一个下标直接入栈' if not S.stack else
                                              f'`s[{S.index}] = {S.s[S.index]}` 比栈顶 `s[{S.stack[-1]}] = {S.s[S.stack[-1]]}` ' + ('更小 → 入栈（比它大的右边点不如它当左端点）' if S.s[S.stack[-1]] > S.s[S.index] else '不更小 → 不入栈'))),
        'stack.append(index)': '下标 `{index}` 入栈，栈 `{stack}`',
        'if s[index] > 0': lambda S, B, r: (f'`s[{S.index}] = {S.s[S.index]}` > 0：左端点取 0 就合格，==特殊情况==，长度 `{S.index + 1}`' if S.s[S.index] > 0
                                            else f'`s[{S.index}] = {S.s[S.index]}` ≤ 0，从 0 开头不合格'),
        'res = max(res, index + 1)': '`res = max({B.res}, {index + 1}) = {res}`',
        'for index in range(len(s) - 1, -1, -1)': '换成从右往左枚举右端点 `index`，用栈里最左的候选去配',
        'while stack and s[index] > s[stack[-1]]': lambda S, B, r: (f'`s[{S.index}] = {S.s[S.index]}` 比栈顶 `s[{S.stack[-1]}] = {S.s[S.stack[-1]]}` 大？' + ('是：栈顶就是它能配的最远左端点' if S.s[S.index] > S.s[S.stack[-1]] else '否：停') if S.stack else '栈空，停'),
        'p = stack.pop()': '弹出左端点 `p = {p}`：右边再小的 `index` 配它只会更短，所以只用一次',
        'if p < index': '`p = {p}` < `index = {index}`？{"是，合法" if p < index else "否，左端点在右边，跳过"}',
        'res = max(res, index - p)': '长度 `{index} - {p} = {index - p}`，`res = max({B.res}, {index - p}) = {res}`',
        'if not stack': '栈空：所有候选左端点都用完了，提前结束',
        'return res': '最长表现良好时间段长度 `{res}`',
    },
    cards=dict(
        one_liner='先找所有可能的左端点，再从右往左一个个配对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['一天工作 > 8 小时为劳累日；段内劳累日数 ==严格多于== 不劳累日数才算表现良好',
                 '求表现良好时间段的最大长度',
                 '本视频：`[6,9,9,6,0,6,9,9]` → `7`'],
        quote='对于子段和相关的问题，很自然就想到使用前缀和。我们求这个数组的前缀和，那么问题就进一步转化成了给出一个数组s，需要找出一组下标对(i, j)，其满足s[i] < s[j]且i和j之间的距离最远。',
        quote_src='—— yiduobo 题解原文',
        idea=['只关心是否 > 8：转成 `±1`，求前缀和 `s`',
              '左端点有单调性：若 `i < k` 且 `s[i] < s[k]`，`k` 永远不如 `i`',
              '所以只保留越来越小的 `s` 当候选；再从右往左配对，配上就弹出'],
        summary=['时间 `O(n)`，每个下标最多入栈、出栈一次',
                 '这里 `s[i]` 含第 `i` 天，所以左端点 0 要特判：`s[index] > 0` 时长度为 `index + 1`',
                 '`if p < index` 防止左端点落在右端点右边',
                 '栈空就 break，后面的 `index` 已经没有候选了',
                 '对比灵神：灵神把 `s[0] = 0` 放进栈里，免去特判，还给了 ±1 的哈希写法'],
    ),
)
