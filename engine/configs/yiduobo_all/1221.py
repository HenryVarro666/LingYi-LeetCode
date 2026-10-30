def _states(s):
    cnt = res = 0
    out = []
    for ch in s:
        before = (ch, cnt, res)
        cnt += 1 if ch == 'L' else -1
        mid = (ch, cnt, res)
        if cnt == 0:
            res += 1
        out.append((before, mid, (ch, cnt, res)))
    return out


def _col(S, i, v):
    p = _pos(S)
    if p is None:
        return None
    if i == p:
        return 'blue'
    if i < p and _states(S['s'])[i][2][1] == 0:
        return 'green'
    return None


def _pos(S):
    """当前正在处理的下标：由 (char, cnt, res) 与行号反推"""
    if 'char' not in S:
        return None
    ln = S['_line']
    k = 0 if ln <= 7 else (1 if ln <= 11 else 2)
    t = (S['char'], S['cnt'], S['res'])
    for p, st in enumerate(_states(S['s'])):
        if st[k] == t:
            return p
    return None


CONFIG = dict(
    num=1221, title='分割平衡字符串', difficulty='Easy', category='贪心与思维',
    author='yiduobo', technique='差值计数 · 归零就切一刀',
    tags=['灵神题单', '贪心算法'],
    code='''
class Solution(object):
    def balancedStringSplit(self, s):

        cnt = 0
        res = 0
        for char in s:
            if char == 'L':
                cnt += 1
            else:
                cnt -= 1
            if cnt == 0:
                res += 1
            
        return res
''',
    call="Solution().balancedStringSplit('RLRRLLRLRL')",
    expect=4,
    views=[
        dict(type='text', fn=lambda S: (f"`cnt` = L 的个数 − R 的个数 = =={S['cnt']}==" if 'cnt' in S else ''), size=34, h=90),
        dict(type='string', var='s', h=300, label='s',
             color=_col, dim=lambda S, i, v: _pos(S) is not None and i > _pos(S)),
    ],
    watch=['char', ('cnt', 'cnt', 'blue'), ('res', 'res', 'green')],
    captions={
        'cnt = 0': '`cnt` 记录当前这段里 `L` 比 `R` 多几个',
        'res = 0': '`res` 统计平衡子串个数',
        'for char in s': '读到 `{char}`',
        "char == 'L'": "`char = '{char}'` → {'是 L，cnt 要加 1' if char == 'L' else '是 R，cnt 要减 1'}",
        'cnt += 1': '遇到 `L`：`cnt` = {cnt}',
        'cnt -= 1': '遇到 `R`：`cnt` = {cnt}',
        'if cnt == 0': '`cnt = {cnt}` → {\'==L 和 R 一样多==，刚好切出一个平衡串\' if cnt == 0 else \'还没平衡，继续往后读\'}',
        'res += 1': '切一刀：`res` = =={res}==，`cnt` 已是 0，下一段从头数',
        'return res': '最多能切成 `{res}` 个平衡字符串',
    },
    cards=dict(
        one_liner='L 记 +1、R 记 −1，差值回到 0 就是一个平衡串',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['平衡字符串：`L` 和 `R` 的数量相等',
                 '把字符串 `s` 分割成尽可能多的平衡子串，返回最大数量',
                 '示例：`RLRRLLRLRL` → `4`'],
        quote='从头开始一趟扫描，使用一个变量cnt统计当前字符串中l和r的差值。若当前字符为L，则将cnt加上1，若当前字符为R，则将cnt减去1。',
        quote_src='—— yiduobo 题解原文',
        idea=['`cnt` 为 0 说明刚读过的这一段 L、R 一样多',
              '一出现 0 就立刻切，切得越早，段数越多',
              '切完 `cnt` 自然是 0，不用重置'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '原文为 Python 3 兼容写法，无需改动',
                 '易错：别用「L 总数等于 R 总数」，要在每次归零时计数',
                 '同类：括号匹配、前缀和为 0 的计数'],
    ),
)
