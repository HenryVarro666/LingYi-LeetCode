W = [5, 3, 12, 14, 1, 2, 3, 2, 10, 6, 6, 9, 7, 8, 7, 10, 8, 9, 6, 9, 9, 8, 3, 7, 7, 2]


def _txt(S):
    if 'w' not in S:
        return ''
    if 'r' in S and S['_line'] >= 10:
        return f"`s = {S['s']}`，`r = 25 - s = {S['r']}`，`chr({S['r']} + 97)` = =={chr(S['r'] + 97)}=="
    return f"当前单词 `{S['w']!r}`，权重和 `s = {S.get('s', 0)}`"


def _wcolor(S, i, v):
    c = S.get('c')
    if c is None or S['_line'] > 8:
        return None
    return 'blue' if i == ord(c) - 97 else None


CONFIG = dict(
    num=3838, title='带权单词映射', difficulty='Easy', category='字符串',
    author='yiduobo', technique='模拟 · 取模后 25 − s',
    tags=[],
    code='''
class Solution(object):
    def mapWordWeights(self, words, weights):
        
        res = []
        for w in words:
            s = 0
            for c in w:
                s += weights[ord(c) - 97]
            s %= 26

            r = 25 - s
            res.append(chr(r + 97))
        
        return ''.join(res)
''',
    call=f'Solution().mapWordWeights(["abcd", "def", "xyz"], {W})',
    expect='rij',
    views=[
        dict(type='string', var='w', label='当前单词 w（蓝 = 正在累加的字母 c）', cell=84, h=130,
             color=lambda S, i, v: 'blue' if S.get('c') is not None and S.get('w') is not None and S['_line'] <= 9 and S['w'].find(S['c'], 0) == i else None),
        dict(type='array', var='weights', label='weights（蓝 = weights[ord(c) - 97]）', cell=36, h=150, index=False, color=_wcolor),
        dict(type='text', h=110, size=30, fn=_txt),
        dict(type='array', var='res', label='res（已映射的字符）', cell=84, h=150),
    ],
    watch=[('w', 'w', 'blue'), ('c', 'c', 'cyan'), ('s', 's', 'orange'), ('r', 'r', 'pink'), ('res', 'res', 'green')],
    captions={
        'res = []': '`res` 收集每个单词映射后的字符',
        'for w in words': lambda S, B, r: (f'取下一个单词 `w = {S.w!r}`，权重和从 0 开始' if 'w' not in B or S.w != B.w or S.res != B.res else '所有单词处理完'),
        's = 0': '`s` 累计单词 `{w!r}` 的权重，先清零',
        'for c in w': lambda S, B, r: ('这个单词的字母都处理完了' if S.get('s') and S.get('c') == B.get('c') and S.get('s') == B.get('s') else f'取单词里的字母 `c = {S.c!r}`'),
        's += weights': '`ord({c!r}) - 97 = {ord(c) - 97}` 是字母在 `weights` 里的下标，加上权重 `{weights[ord(c) - 97]}` → `s = {s}`',
        's %= 26': '权重对 26 取模：`s = {s}`',
        'r = 25 - s': '倒序映射：`s` 的倒序映射 == `r = 25 - s` 的正序映射 → `r = {r}`',
        'res.append': '`r + 97` 是字母 ascii 码，转成字符 `{res[-1]!r}` 加入 `res`',
        'return': '连接所有字符，返回 `{ret!r}`',
    },
    max_steps=70,
    cards=dict(
        one_liner='倒序映射：`s` 的倒序等于 `25 − s` 的正序',
        complexity='时间 `O(L)`，空间 `O(1)`',
        problem=['单词权重 = 各字母权重之和，对 26 取模',
                 '按 `0->z, 1->y, ..., 25->a` 映射为一个字母',
                 '本视频：`["abcd","def","xyz"]` → `"rij"`'],
        quote='将s对26取模，接下来令r = 25 - s，理由是s的倒序映射，就相当于r的正序映射。最后，将r加上字母\'a\'的ascii码，就得到了w结果操作后得到字符的ascii码。',
        quote_src='—— yiduobo 题解原文',
        idea=['用 `ord(c) - 97` 定位字母在 `weights` 的下标，累加到 `s`',
              '`s %= 26` 后令 `r = 25 - s`，倒序就变成了正序',
              '`chr(r + 97)` 得到字母，追加到 `res`'],
        summary=['时间 `O(L)`，空间 `O(1)`',
                 '易错：必须先取模再算 `25 - s`，否则 `r` 可能为负',
                 '`97` 就是 `ord(\'a\')`，字母和下标互转的常用写法',
                 '原文为 Python 2 风格，仅 `class ...(object)` 写法，Python 3 直接可运行，代码未改',
                 '对比灵神：灵神直接用 `ord_z - s % 26`，yiduobo 先算 `25 - s`'],
    ),
)
