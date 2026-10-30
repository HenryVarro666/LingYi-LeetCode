_NM = {0: '初始', 1: '见过小写', 2: '小写后见大写 ✓', -1: '作废'}


def _states(S):
    if 'state' not in S:
        return ''
    st = S['state']
    items = [(chr(96 + i), st[i]) for i in range(1, 27) if st[i] != 0]
    if not items:
        return '各字母状态都是 0（初始）'
    return '　'.join(f"`{k}` = =={v}==" for k, v in items)


def _cur(S):
    if 'c' not in S or 'x' not in S:
        return ''
    c = S['c']
    return f"当前 `{chr(c)}`（{'小写' if c & 32 else '大写'}），字母 `{chr(96 + S['x'])}` 的状态 = =={S['state'][S['x']]}=="


CONFIG = dict(
    num=3121, title='统计特殊字母的数量 II', difficulty='Medium', category='位运算',
    author='灵茶山艾府', technique='状态机 · 一次遍历', tags=[],
    code='''
class Solution:
    def numberOfSpecialChars(self, word: str) -> int:
        ans = 0
        state = [0] * 27
        for c in map(ord, word):
            x = c & 31  # 转成数字 1~26
            if c & 32:  # 小写字母
                if state[x] == 0:
                    state[x] = 1
                elif state[x] == 2:  # 大写的后面不能有小写
                    state[x] = -1
                    ans -= 1
            else:  # 大写字母
                if state[x] == 0:  # 还没遇到小写，就先遇到大写了
                    state[x] = -1
                elif state[x] == 1:
                    state[x] = 2
                    ans += 1
        return ans
''',
    call='Solution().numberOfSpecialChars("aAbBaAcC")',
    expect=2,
    views=[
        dict(type='string', var='word', h=220, cell=100,
             color=lambda S, i, v: 'blue' if 'c' in S and 'ans' in S and v == chr(S['c']) else None),
        dict(type='text', fn=_cur, h=70),
        dict(type='text', fn=_states, h=110),
        dict(type='text', fn=lambda S: '状态：0 初始　1 见过小写　2 小写后见大写（计入答案）　-1 作废' , h=60, size=26),
    ],
    watch=[('c', "c", 'blue'), ('ans', 'ans', 'green')],
    captions={
        'state = [0]': '每个字母一个状态，下标 1~26，初始都是 0',
        'for c in': lambda S, B, r: (f'取出下一个字符 `{chr(S.c)}`' if S.c != B.get('c') or S.c == 97 and B.get('c') is None else '遍历结束'),
        'x = c & 31': '`c & 31` = {x}：大小写同一个编号，`{chr(c)}` 对应状态 `state[{x}]`',
        'if c & 32': lambda S, B, r: f"`c & 32` = {S.c & 32}：{'小写字母' if S.c & 32 else '大写字母'}",
        'if state[x] == 0:': lambda S, B, r: f"`state[{S.x}]` = {S.state[S.x]}，{'是 0 → 还没见过这个字母' if S.state[S.x] == 0 else '不是 0'}",
        'elif state[x] == 2': lambda S, B, r: f"`state[{S.x}]` = {S.state[S.x]}，{'已经见过大写，现在又来小写 → 违规' if S.state[S.x] == 2 else '不是 2'}",
        'elif state[x] == 1': lambda S, B, r: f"`state[{S.x}]` = {S.state[S.x]}，{'先有小写，现在见到大写 → 合格' if S.state[S.x] == 1 else '不是 1'}",
        'state[x] = 1': '第一次见小写 `{chr(c)}`：状态 0 → ==1==',
        'state[x] = -1': lambda S, B, r: ('大写之后又出现小写：状态 → ==-1==（永远作废）' if S.c & 32 else '没见小写就先来大写：状态 → ==-1==（永远作废）'),
        'ans -= 1': '之前算过的这个字母要撤销：`ans` → =={ans}==',
        'state[x] = 2': '先小写后大写：状态 1 → ==2==',
        'ans += 1': '字母 `{chr(c)}` 合格，`ans` → =={ans}==',
        'return': '状态为 2 的字母共 ==`{ret}`== 个',
    },
    skip=[],
    cards=dict(
        one_liner='给每个字母配一个小状态机：先小写、后大写才算数',
        complexity='时间 `O(n+|Σ|)`，空间 `O(|Σ|)`，|Σ| = 26',
        problem=['字母 `c` 的小写、大写都出现，且==所有小写都在第一个大写之前==才算特殊字母', '返回特殊字母的数量',
                 '示例：`"aAbBaAcC"` → `2`（a 的大写后面又出现了小写 a）'],
        quote='对于同一种字母，一定要先遍历到其小写形式，再遍历到其大写形式，且遇到大写形式后，不能再遍历到其小写形式。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每个字母四个状态：0 初始、1 见过小写、2 小写后见大写、-1 作废',
              '状态 1 + 大写 → 2，答案 +1；状态 2 + 小写 → -1，答案 -1',
              '最后状态为 2 的字母种数就是答案'],
        summary=['时间 `O(n+|Σ|)`，空间 `O(|Σ|)`',
                 '==状态 2 遇到小写要把 ans 减回去==，别忘了 `ans -= 1`',
                 '没见小写就先见大写 → 直接 -1，之后怎么来都不变',
                 '题解另给了位运算写法：lower、upper、invalid 三个集合，最后算 `lower & upper & ~invalid`'],
    ),
)
