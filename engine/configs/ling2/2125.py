def _ri(S):
    """当前 row 在 bank 中的下标（按对象身份找，避免内容相同的行混淆）"""
    if 'row' not in S or 'bank' not in S:
        return None
    for i, r in enumerate(S['bank']):
        if r is S['row']:
            return i
    return None


def _kept(S, B):
    """已经乘进 ans 的、有设备的行的设备数（去掉全 0 行之后的序列）"""
    i = _ri(S)
    if i is None:
        return []
    done = S['_line'] in (7, 8, 9) or (S['_line'] == 4 and B.get('row') is S['row'])
    upto = i + 1 if done else i
    return [r.count('1') for r in S['bank'][:upto] if r.count('1') > 0]


def _formula(S, B):
    ks = _kept(S, B)
    if not ks:
        return '去掉全 0 的行，剩下的设备数序列：（空）'
    seq = ', '.join(map(str, ks))
    if len(ks) == 1:
        return f'去掉全 0 的行 → `{seq}`；只有一行，还没有激光'
    terms = ' + '.join(f'{a}×{b}' for a, b in zip(ks, ks[1:]))
    tot = sum(a * b for a, b in zip(ks, ks[1:]))
    return f'去掉全 0 的行 → `{seq}`；相邻相乘：`{terms}` = =={tot}=='


def _cap_if(S, B, ret):
    c = S['cnt']
    if c > 0:
        return f'`cnt = {c} > 0`：这一行有设备，它和==上一个有设备的行==之间全是空行 → 两两之间都有激光'
    return '`cnt = 0`：空行对激光没有任何影响，==直接跳过==（相当于把这一行删掉）'


CONFIG = dict(
    num=2125, title='银行中的激光束数量', difficulty='Medium', category='数学',
    author='灵茶山艾府', technique='阅读理解：去掉空行，相邻行相乘',
    tags=['字节6个月'],
    code='''
class Solution:
    def numberOfBeams(self, bank: List[str]) -> int:
        ans = pre_cnt = 0
        for row in bank:
            cnt = row.count('1')
            if cnt > 0:
                ans += pre_cnt * cnt
                pre_cnt = cnt
        return ans
''',
    call='Solution().numberOfBeams(["011001","000000","010100","001000"])',
    expect=8,
    views=[
        dict(type='grid', var='bank', label='bank（1 = 安全设备；左侧数字 = 该行设备数）', h=420, cell=80,
             rows=lambda S: [r.count('1') for r in S['bank']] if 'bank' in S else None,
             color=lambda S, i, j, v: ('yellow' if v == '1' else 'blue') if i == _ri(S)
             else ('green' if v == '1' else None)),
        dict(type='text', fn=_formula, size=30),
    ],
    watch=[('cnt', 'cnt', 'blue'), ('pre_cnt', 'pre_cnt', 'pink'), ('ans', 'ans', 'green')],
    captions={
        'ans = pre_cnt = 0': '`pre_cnt` 记录==上一个有设备的行==有几个设备；一开始没有，记为 0',
        'for row in bank': lambda S, B, ret: (f'从上往下看第 `{_ri(S)}` 行：`"{S["row"]}"`'
                                              if B.get('row') is not S['row'] else '所有行都看完了，循环结束'),
        'cnt = row.count': '数一数这一行的设备：`cnt = {cnt}`',
        'if cnt > 0': _cap_if,
        'ans += pre_cnt * cnt': lambda S, B, ret: ('这是==第一个==有设备的行，上面没有设备可配对：`ans += 0×{}` 仍为 0'.format(S['cnt'])
                                                   if S['pre_cnt'] == 0 else
                                                   '上一个非空行的 `{0}` 个设备 × 这一行的 `{1}` 个，每对之间一束：`ans += {0}×{1}` → =={2}=='.format(S['pre_cnt'], S['cnt'], S['ans'])),
        'pre_cnt = cnt': '这一行成为新的「上一个有设备的行」：`pre_cnt = {pre_cnt}`',
        'return ans': '所有相邻的非空行都乘过了，返回 =={ret}==',
    },
    max_steps=40,
    cards=dict(
        one_liner='去掉没有设备的行，相邻两行的设备数相乘再求和',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`bank[i]` 是第 i 行，`\'1\'` 是安全设备；两设备在==不同行==，且==中间的行全都没有设备==时，之间有一束激光',
                 '求激光束总数',
                 '示例：`["011001","000000","010100","001000"]` → `8`'],
        quote='题意：==去掉没有安全设备的行==，计算==相邻行==之间的激光束的数量之和。',
        quote_src='—— 灵茶山艾府题解',
        idea=['示例 1 每行设备数是 `3, 0, 2, 1`，去掉 0 剩下 `3, 2, 1`',
              '相邻两行的设备两两配对：`3×2 + 2×1 = 8`',
              '遍历时只需记住==上一个非空行==的设备数 `pre_cnt`'],
        summary=['时间 `O(mn)`（每个字符看一次），空间 `O(1)`',
                 '易错：空行==不能更新== `pre_cnt`，否则会把 0 乘进去，把激光“挡断”',
                 '易错：只有相邻的非空行之间有激光，第 0 行和第 3 行之间没有',
                 '本质是“阅读理解”：把题意翻译成「去零 + 相邻乘积」就做完了'],
    ),
)
