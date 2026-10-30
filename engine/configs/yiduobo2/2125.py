def _ri(S):
    """当前 line 在 bank 中的下标（按对象身份找）"""
    if 'line' not in S or 'bank' not in S:
        return None
    for i, r in enumerate(S['bank']):
        if r is S['line']:
            return i
    return None


def _counted(S, i, j):
    """当前行里第 j 格的 '1' 是否已经被 now 数过"""
    if i != _ri(S) or 'now' not in S or S.get('_line') == 6:
        return False
    row = S['bank'][i]
    k = row[:j + 1].count('1')
    return row[j] == '1' and k <= S['now']


def _color(S, i, j, v):
    ri = _ri(S)
    if i == ri:
        if v == '1':
            return 'yellow' if _counted(S, i, j) else 'orange'
        return 'blue'
    return 'green' if v == '1' else None


def _cap_if(S, B, ret):
    now = S['now']
    if now > 0:
        if S['last'] == 0:
            return f'`now = {now} > 0`：这是==第一个==有设备的行，上面没有可配对的设备'
        return f'`now = {now} > 0`：它和上一个有设备的行（{S["last"]} 个）之间==没有别的有设备的行== → 会产生激光'
    return '`now = 0`：没有设备的行和激光==完全没有关联==，直接跳过，`last` 不变'


def _cap_for(S, B, ret):
    if B.get('line') is S['line']:
        return '所有行都遍历完了'
    return f'从上往下遍历第 `{_ri(S)}` 行：`"{S["line"]}"`'


CONFIG = dict(
    num=2125, title='银行中的激光束数量', difficulty='Medium', category='数学',
    author='yiduobo', technique='记录上一个有设备的行 last',
    tags=['字节6个月'],
    code='''
class Solution(object):
    def numberOfBeams(self, bank):

        last = 0
        res = 0
        for line in bank:
            now = 0
            for char in line:
                if char == '1':
                    now += 1
            if now > 0:
                res += last * now
                last = now

        return res
''',
    call='Solution().numberOfBeams(["011001","000000","010100","001000"])',
    expect=8,
    views=[
        dict(type='grid', var='bank', label='bank（当前行：黄 = 已数过的 1，橙 = 还没数到）', h=420, cell=80,
             rows=lambda S: list(range(len(S['bank']))) if 'bank' in S else None, color=_color),
        dict(type='text', size=30,
             fn=lambda S: (f'本行和上一个有设备的行：`last × now = {S["last"]} × {S["now"]}` = =={S["last"] * S["now"]}== 束'
                           if S.get('_line') == 12 else
                           (f'正在数第 {_ri(S)} 行的设备：`now = {S["now"]}`' if 'now' in S and _ri(S) is not None and S.get('_line') != 6 else ''))),
    ],
    watch=[('now', 'now', 'blue'), ('last', 'last', 'pink'), ('res', 'res', 'green')],
    captions={
        'last = 0': '`last` 记录==上一个有激光设备的行==中的设备数量，初始化为 0',
        'res = 0': '`res` 累计激光束总数',
        'for line in bank': _cap_for,
        'now = 0': '统计当前行的设备数量 `now`，先清零',
        'now += 1': '数到一个 `\'1\'`：`now = {now}`',
        'if now > 0': _cap_if,
        'res += last * now': lambda S, B, ret: (f'`res += {S["last"]} × {S["now"]} = 0`（上面还没有设备）' if S['last'] == 0 else
                                                f'两行之间激光数 = ==两行设备数的乘积==：`res += {S["last"]} × {S["now"]}` → =={S["res"]}=='),
        'last = now': '把 `last` 更新为 `now = {now}`，供下一个有设备的行使用',
        'return res': '遍历结束，返回 =={ret}==',
    },
    skip=['for char in line', "if char == '1'"],
    max_steps=50,
    cards=dict(
        one_liner='用 last 记住上一个有设备的行，每遇到非空行就累加 last × now',
        complexity='时间 `O(mn)`，空间 `O(1)`',
        problem=['`bank[i]` 是第 i 行，`\'1\'` 是安全设备；两设备在==不同行==，且==中间的行全都没有设备==时，之间有一束激光',
                 '求激光束总数',
                 '示例：`["011001","000000","010100","001000"]` → `8`'],
        quote='对于没有激光设备的行来说，激光束与这些行==完全没有关联==……激光束的计算方法也很简单，就是==这两行激光设备的乘积==。',
        quote_src='—— yiduobo 知乎题解',
        idea=['用变量 `last` 记录上一个有激光设备的行中设备的数量，初始化为 0',
              '从上往下遍历每一行，逐个字符统计当前行的设备数 `now`',
              '`now == 0` 直接跳过；否则 `res += last * now`，再把 `last` 更新为 `now`'],
        summary=['时间 `O(mn)`（逐个字符数 1），空间 `O(1)`',
                 '易错：`now == 0` 的行不能更新 `last`，否则会把激光“挡断”',
                 '`last` 初始为 0，第一行有设备时乘出来正好是 0，不用特判',
                 '原文为 Python 2 风格（类型写在文档字符串里），已删去文档字符串，代码未改'],
    ),
)
