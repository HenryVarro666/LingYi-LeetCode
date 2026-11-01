def _skip(S, B, ret):
    if S.i >= S.n:
        return f'`i = {S.i}` 走到末尾，没有可突变的位'
    d = int(S.s[S.i])
    if S.change[d] <= d:
        return f'`s[{S.i}] = {d}`，`change[{d}] = {S.change[d]}` <= {d} → ==换了不赚==，跳过，继续往右'
    return f'`change[{d}] = {S.change[d]}` > {d} → ==找到突变起点，换了变大==；高位变大最划算'


def _swap(S, B, ret):
    if S.i >= S.n:
        return f'`i = {S.i}` 走到末尾，后缀全部突变完'
    d = int(S.s[S.i])
    if S.change[d] >= d:
        return f'`change[{d}] = {S.change[d]}` >= {d} → ==换了不亏==，继续突变'
    return f'`change[{d}] = {S.change[d]}` < {d} → ==换了变小，停止突变=='


CONFIG = dict(
    num=1946, title='子字符串突变后可能得到的最大整数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='字符串贪心 · 两段循环（Go 原文转写）',
    tags=['灵神题单', '贪心与思维', '难度分 1445'],
    code='''
class Solution:
    def maximumNumber(self, num: str, change: List[int]) -> str:
        s = list(num)
        i, n = 0, len(s)
        while i < n and change[ord(s[i]) & 15] <= ord(s[i]) & 15:
            i += 1
        while i < n and change[ord(s[i]) & 15] >= ord(s[i]) & 15:
            s[i] = chr(ord('0') + change[ord(s[i]) & 15])
            i += 1
        return ''.join(s)
''',
    call='Solution().maximumNumber("3214", [9,8,5,0,3,6,4,2,6,8])',
    expect='3584',
    views=[
        dict(type='text', fn=lambda S: (f"`s[{S['i']}] = {S['s'][S['i']]}` → `change = {S['change'][int(S['s'][S['i']])]}`" if 'i' in S and S['i'] < len(S['s']) and S['s'][S['i']].isdigit() else '突变一段子串：先找起点，再尽量往右延伸'), size=28),
        dict(type='array', var='s', pointers={'i': 'pink'}, h=200,
             color=lambda S, idx, v: 'green' if 'i' in S and idx < S['i'] and S['_line'] >= 7 and ''.join(S['s']) != S['num'] and S['s'][idx] != S['num'][idx] else None),
        dict(type='array', var='change', h=200, label='change（下标 d → 映射值）'),
    ],
    watch=['num', ('i', 'i', 'pink'), ('s', "''.join(s)", 'green')],
    captions={
        's = list(num)': '转成字符列表 `s`，方便原地改某一位',
        'i, n = 0, len': '`i` 从最高位开始',
        'while i < n and change[ord(s[i]) & 15] <=': _skip,
        'while i < n and change[ord(s[i]) & 15] >=': _swap,
        "s[i] = chr": '把 `s[{i}]` 改成映射后的数字 `{s[i]}`',
        'i += 1': '`i` → {i}',
        "return ''.join": '拼回字符串 =={ret}==',
    },
    cards=dict(
        one_liner='跳过换了不赚的高位，从第一个变大的位开始一路换到变小为止',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`num` 是大整数字符串，`change[d]` 表示数字 `d` 突变后的值',
                 '可以选一个连续子串全部突变（也可以不突变），求能得到的最大整数',
                 '示例：`"132"`，`change = [9,8,5,0,3,6,4,2,6,8]` → `"832"`'],
        quote='for ; i < n && byte(change[s[i]&15]) <= s[i]&15; i++ {}  // 先跳过换了不赚的位  |  for ; i < n && byte(change[s[i]&15]) >= s[i]&15; i++ { s[i] = ... }  // 再突变',
        quote_src='—— 灵茶山艾府题解（原文只有 Go 代码）',
        idea=['数值比较先看高位：第一个能变大的位决定了起点',
              '起点之前换了不赚（`<=`）的位，不如不换，直接跳过',
              '起点之后只要不变小（`>=`）就继续换，变相等也无妨；一变小就停'],
        summary=['原文为 Go，已按原逻辑逐行转写为 Python（`& 15` 取字符对应的数字）',
                 '时间 `O(n)`，空间 `O(n)`',
                 '易错点：第一个循环用 `<=`（相等的位不能当起点），第二个用 `>=`（相等的位可以顺带换）',
                 '只突变一段连续子串，遇到变小就必须停'],
    ),
)
