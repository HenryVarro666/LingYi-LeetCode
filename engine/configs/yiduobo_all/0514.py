RING, KEY = 'goddi', 'gdi'


def _cell(S, ii, jj, v):
    if 'k' not in S or 'j' not in S or 'i' not in S or S.get('k') is None:
        return None
    i, j, k = S['i'], S['j'], S['k']
    if (ii, jj) == (i, j):
        return 'yellow'
    if i > 0 and (ii, jj) == (i - 1, k):
        return 'blue'
    return None


def _need(c):
    if not c:
        raise ValueError('loop end')
    return None


def _formula(S):
    if 'j' not in S or 'k' not in S or 'dis' not in S:
        return '`f[i][j]` = 拼完 `key[0..i]`、盘面停在 `ring[j]` 的最少步数（含按按钮）'
    i, j, k, d = S['i'], S['j'], S['k'], S['dis']
    if i == 0:
        return f'起点 0 → 位置 {j}：`dis = {d}`，`f[0][{j}] = {d} + 1`'
    return f'`f[{i - 1}][{k}] + dis({k}→{j}) + 1 = {S["f"][i - 1][k]} + {d} + 1`，和旧的 `f[{i}][{j}]` 取小'


CONFIG = dict(
    num=514, title='自由之路', difficulty='Hard', category='动态规划',
    author='yiduobo', technique='二维 DP · 按位置列表转移',
    tags=['动态规划', '其他线性 DP', '难度分 2400'],
    code='''
class Solution(object):
    def findRotateSteps(self, ring, key):

        pos_dict = {}
        for index, char in enumerate(ring):
            if char not in pos_dict:
                pos_dict[char] = []
            pos_dict[char].append(index)

        f = [[None] * len(ring) for _ in range(len(key))]

        for i in range(len(key)):
            if i == 0:
                pos_list = [0]
            else:
                pos_list = pos_dict[key[i - 1]]
            for j in pos_dict[key[i]]:
                for k in pos_list:
                    dis = min((j - k + len(ring)) % len(ring) , (k - j + len(ring)) % len(ring))
                    if i == 0:
                        f[i][j] = dis + 1
                    elif f[i][j] is None or f[i][j] > f[i - 1][k] + dis + 1:
                        f[i][j] = f[i - 1][k] + dis + 1
        
        res = None
        for pos in pos_dict[key[-1]]:
            if res is None or res > f[-1][pos]:
                res = f[-1][pos]
        return res
''',
    call=f'Solution().findRotateSteps({RING!r}, {KEY!r})',
    expect=6,
    skip=['for index, char', 'if char not in pos_dict', 'pos_dict[char] = []', 'pos_dict[char].append', 'pos_list = [0]', 'pos_list = pos_dict[key[i - 1]]', 'else:', 'for i in range', 'for j in pos_dict', 'for k in pos_list'],
    max_steps=80,
    views=[
        dict(type='array', var=lambda S: list(S['ring']), label='ring（环形）：j = 目标位置，k = 上一个字母所在位置', h=190, cell=84,
             pointers={'k': 'pink', 'j': 'blue'},
             color=lambda S, p, v: ('blue' if p == S.get('j') and 'dis' in S else 'pink' if p == S.get('k') and 'dis' in S else None)),
        dict(type='text', fn=_formula, size=26, h=60),
        dict(type='table', var='f', label='f[i][j]：行 = key 第 i 个字母，列 = 停在 ring[j]（黄=在算，蓝=来源）', h=260, cell=84,
             rows=lambda S: [f'{k}{c}' for k, c in enumerate(S['key'])], cols=lambda S: [f'{k}{c}' for k, c in enumerate(S['ring'])],
             color=_cell),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('k', 'k', 'cyan'), ('dis', 'dis', 'orange'), ('res', 'res', 'green')],
    captions={
        'pos_dict = {}': '`pos_dict[字符]` = 这个字符在表盘上的所有位置（同一字母可能出现多次）',
        'f = [[None]': '`f[i][j]`：完成前 `i` 位、表盘停在第 `j` 个字符时的==最少步数==；`None` = 到不了',
        'for i in range': lambda S, B, r: (_need(S.get('i') != B.get('i')) or f'开始拼 `key[{S.i}]` = `{S.key[S.i]}`，它在表盘上的位置：{S.pos_dict[S.key[S.i]]}' ),
        'for j in pos_dict': lambda S, B, r: _need(S.get('j') != B.get('j')) or f'目标位置 `j = {S.j}`（`ring[{S.j}] = {S.ring[S.j]}`）',
        'for k in pos_list': lambda S, B, r: _need(S.get('k') != B.get('k') or S.get('j') != B.get('j')) or (f'上一个字母停在 `k = {S.k}`' + ('（起点固定在 0）' if S.i == 0 else f'：来自 `f[{S.i - 1}][{S.k}] = {S.f[S.i - 1][S.k]}`')),
        'dis = min': lambda S, B, r: f'从 `{S.k}` 转到 `{S.j}`：顺时针 `{(S.j - S.k + len(S.ring)) % len(S.ring)}` 步，逆时针 `{(S.k - S.j + len(S.ring)) % len(S.ring)}` 步 → 取小 `dis = {S.dis}`',
        13: lambda S, B, r: f'拼 `key[{S.i}]` = `{S.key[S.i]}`：' + ('第一位，出发点固定在 0' if S.i == 0 else f'出发点 = 上一个字母 `{S.key[S.i-1]}` 的所有位置 {S.pos_list}') + f'；目标位置 {S.pos_dict[S.key[S.i]]}',
        20: lambda S, B, r: (f'拼 `key[{S.i}]` = `{S.key[S.i]}`：第一个字母，直接从起点 0 转到 `{S.j}`' if S.i == 0 else f'拼 `key[{S.i}]` = `{S.key[S.i]}`：从上一个字母的位置 `k={S.k}`（`f[{S.i-1}][{S.k}] = {S.f[S.i-1][S.k]}`）转到 `j={S.j}`'),
        'f[i][j] = dis + 1': '`f[0][{j}] = {dis} + 1 = {f[i][j]}`（+1 是按按钮）',
        'elif f[i][j] is None': lambda S, B, r: (f'`f[{S.i}][{S.j}]` 还是空 → 新路线 `{S.f[S.i-1][S.k]} + {S.dis} + 1` 直接采用' if S.f[S.i][S.j] is None else f'旧值 `{S.f[S.i][S.j]}` 比新路线 `{S.f[S.i-1][S.k] + S.dis + 1}` {"大 → 更新" if S.f[S.i][S.j] > S.f[S.i-1][S.k] + S.dis + 1 else "不大 → 不更新"}'),
        'f[i][j] = f[i - 1][k] + dis + 1': '`f[{i}][{j}] = f[{i-1}][{k}] + {dis} + 1` = =={f[i][j]}==',
        'res = None': '答案在最后一行：对最后一个字母的所有位置取最小',
        'if res is None or res >': lambda S, B, r: f'`f[-1][{S.pos}] = {S.f[-1][S.pos]}`，当前 `res = {S.res}` → 取小',
        'res = f[-1][pos]': '`res` 更新为 =={res}==',
        'return res': '最少步数 =={ret}==',
    },
    cards=dict(
        one_liner='key 一位一位输入：f[i][j] = 拼完前 i 位、停在 j 的最少步数',
        complexity='时间 `O(m · c²)`（c 为同一字母的出现次数），空间 `O(m·n)`',
        problem=['`ring` 是环形表盘，12:00 方向最初对着 `ring[0]`',
                 '每转一格 1 步，对齐 `key[i]` 后按按钮也算 1 步，求拼出 `key` 的最少步数',
                 '示例：`ring="godding"`，`key="gd"` → `4`；本视频用 `goddi` / `gdi`'],
        quote='题目要求一位一位输入密码，天然就给分好了状态。由于同一个字母可能出现多次，因此需要使用二维状态f[i][j]。',
        quote_src='—— yiduobo 题解原文',
        idea=['`pos_dict` 记录每个字母在表盘上的位置列表',
              '转移：枚举上一个字母的位置 `k` 和这一个字母的位置 `j`',
              '`dis` 取顺/逆时针较小者，`+1` 是按按钮；最后在最后一行取最小'],
        summary=['时间 `O(m · c²)`，c 为同一字母出现次数；空间 `O(m·n)`',
                 '`dis` 要取顺/逆时针的较小值，别忘了加上按按钮的 1 步',
                 '第 0 位的起点固定是位置 0，不是上一个字母的位置',
                 '对比灵神：灵神只转到左/右最近的目标字母（2 种选择），yiduobo 枚举所有出现位置',
                 '原文已是 Python 3 可运行写法，逐字照搬'],
    ),
)
