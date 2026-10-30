def _win(S):
    if 'index' not in S or 'res' not in S:
        return []
    i, k, n = S['index'], S['k'], S['n']
    if k > 0:
        return [(i + j) % n for j in range(1, k + 1)]
    return [(i - j) % n for j in range(1, -k + 1)]


def _ccol(S, i, v):
    if 'index' in S and i == S['index'] and 'res' in S:
        return 'blue'
    return 'cyan' if i in _win(S) else None


def _txt(S):
    w = sorted(_win(S))
    if not w:
        return '`s[j]` = `code[0] + … + code[j]`（前缀和）'
    vals = ' + '.join(str(S['code'][j]) for j in _win(S))
    return f"`index = {S['index']}` 前面 `{-S['k']}` 个（循环）：`{vals}` = =={sum(S['code'][j] for j in w)}=="


CONFIG = dict(
    num=1652, title='拆炸弹', difficulty='Easy', category='滑动窗口与双指针',
    author='yiduobo', technique='前缀和 · 分越界讨论',
    tags=['灵神核心路线', '灵神题单·滑动窗口与双指针'],
    code='''
class Solution(object):
    def decrypt(self, code, k):

        n = len(code)
        if k == 0:
            return [0] * n

        s = [code[0]]
        for num in code[1:]:
            s.append(s[-1] + num)

        res = []
        for index in range(n):
            if k > 0:
                if index + k < n:
                    res.append(s[index + k] - s[index])
                else:
                    offset = k - (n - 1 - index) - 1
                    res.append(s[-1] - s[index] + s[offset])
            elif k < 0:
                if index + k > 0:
                    res.append(s[index - 1] - s[index + k - 1])
                else:
                    offset = n - (-k - index) - 1
                    res.append(s[-1] - s[offset])
                    if index > 0:
                        res[-1] += s[index - 1]

        return res
''',
    call='Solution().decrypt([2,4,9,3,5], -2)',
    expect=[8, 7, 6, 13, 12],
    views=[
        dict(type='array', var='code', label='code（蓝 = 当前 index，青 = 要求和的前 |k| 个）', h=210, cell=100,
             color=_ccol),
        dict(type='array', var='s', label='s：前缀和（含当前位置）', h=190, cell=100),
        dict(type='array', var='res', label='res', h=180, cell=100, min_slots=5),
        dict(type='text', h=80, size=28, fn=_txt),
    ],
    watch=['n', 'k', ('index', 'index', 'blue'), ('offset', 'offset', 'orange')],
    captions={
        'n = len': '`n = {n}`',
        'if k == 0': '`k = {k} ≠ 0`，需要真正计算',
        's = [code[0]]': '前缀和 `s[0] = code[0] = {s[0]}`（==含当前位置==的前缀和）',
        'for num in code[1:]': lambda S, B, ret: ('前缀和算完了' if len(S.s) == S.n else f'取 `num = {S.num}`'),
        's.append(s[-1] + num)': '`s` 末尾加入 `{s[-2]} + {num}` = `{s[-1]}`',
        'res = []': '`res`：答案列表',
        'for index in range': lambda S, B, ret: (f'计算位置 `index = {S.index}`' if 'index' not in B or S.index != B.index
                                                else '每个位置都算完了'),
        'if k > 0': '`k = {k} < 0`：要的是==前面== {-k} 个数之和',
        'elif k < 0': '`k < 0` 分支：只可能越过==左边界==',
        'if index + k > 0': lambda S, B, ret: (f'`index + k = {S.index + S.k} > 0`：不越界，直接用前缀和相减' if S.index + S.k > 0
                                               else f'`index + k = {S.index + S.k} ≤ 0`：越过左边界 → ==一段后缀 + 一段前缀=='),
        'res.append(s[index - 1] - s[index + k - 1])': '`s[{index - 1}] − s[{index + k - 1}]` = `{s[index - 1]} − {s[index + k - 1]}` = =={res[-1]}==',
        'offset = n - (-k - index) - 1': lambda S, B, ret: (f'前面只有 `{S.index}` 个数，还差 `{-S.k - S.index}` 个从末尾补：`offset = {S.offset}`'
                                                            if -S.k - S.index > 0 else
                                                            f'`index + k = 0`：当成==长度为 0 的后缀== + 前缀，`offset = {S.offset}`'),
        'res.append(s[-1] - s[offset])': '后缀和 `s[-1] − s[{offset}]` = `{s[-1]} − {s[offset]}` = `{res[-1]}`',
        'if index > 0': lambda S, B, ret: (f'`index = {S.index} > 0`：还要加上前缀 `s[{S.index - 1}]`' if S.index > 0
                                           else '`index = 0`：前面没有数，前缀和为 0，不用加'),
        'res[-1] += s[index - 1]': '加上前缀 `s[{index - 1}] = {s[index - 1]}` → =={res[-1]}==',
        'return res': '解密结果 `{res}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='静态区间和用前缀和；环形越界时拆成后缀 + 前缀',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['循环数组 `code` 和密钥 `k`：`k > 0` 把每个数换成==后面== k 个数之和',
                 '`k < 0` 换成==前面== |k| 个数之和，`k = 0` 换成 0；所有数同时替换',
                 '示例：`[2,4,9,3], k = -2` → `[12,5,6,13]`；本视频 `[2,4,9,3,5], k = -2`'],
        quote='对于静态区间和问题，一种常见的做法就是使用前缀和来替代。……发生越界时，原始的区间和就变成了==一个前缀和加上一个后缀和==。',
        quote_src='—— yiduobo 题解原文',
        idea=['`k > 0` 只可能越过右边界；`k < 0` 只可能越过左边界',
              '不越界：两个前缀和相减',
              '越界：后缀和 `s[-1] − s[offset]` + 前缀和 `s[index − 1]`'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '这里 `s[j]` 含 `code[j]`，所以 `index = 0` 时前缀和要特判为 0',
                 '易错：越界长度的计算，`-k - index` 个数要从末尾补',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需改动',
                 '对比灵神：灵神发现窗口总是向右滑，直接用 `% n` 定长滑窗'],
    ),
)
