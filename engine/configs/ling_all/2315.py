def _split_view(S):
    s = S.get('s')
    if s is None:
        return ''
    ps = s.split('|')
    ev = [p for p in ps[::2]]
    return '切开：' + '  ,  '.join(f'`{p or "空"}`' for p in ps) + f'    →  取下标 0,2,4…：' + ' , '.join(f'=={p or "空"}==' for p in ev)


def _cnt(S):
    s = S.get('s')
    if s is None:
        return ''
    ps = s.split('|')[::2]
    return '各段星号数：' + ' + '.join(str(p.count('*')) for p in ps) + f' = =={sum(p.count("*") for p in ps)}=='


def _color(S, i, v):
    s = S['s']
    k = s[:i].count('|')
    if v == '|':
        return 'orange'
    if k % 2 == 1:
        return None
    return 'green' if v == '*' else None


CONFIG = dict(
    num=2315, title='统计星号', difficulty='Easy', category='字符串',
    author='灵茶山艾府', technique='按竖线切分 + 取偶数段',
    code='''
class Solution:
    def countAsterisks(self, s: str) -> int:
        return sum(t.count('*') for t in s.split('|')[::2])
''',
    call="Solution().countAsterisks('l|*e*et|c**o|*de|')",
    expect=2,
    views=[
        dict(type='string', var='s', label='s（橙 = 竖线，绿 = 不在竖线对之间的星号）', cell=40, h=200,
             dim=lambda S, i, v: S['s'][:i].count('|') % 2 == 1 and v != '|',
             color=_color),
        dict(type='text', fn=_split_view, size=30),
        dict(type='text', fn=_cnt, size=34),
    ],
    watch=[],
    captions={
        'return sum': '`s.split("|")` 把字符串按竖线切开：下标 0、2、4… 的段在竖线对==外面==，1、3、5… 的段在对里面。只数偶数段里的 `*`：总共 =={ret}==',
    },
    cards=dict(
        before=[dict(heading='先手动切一遍', lines=['`l|*e*et|c**o|*de|` 按 `|` 切成 5 段：',
                                              '`l` , `*e*et` , `c**o` , `*de` , 空串',
                                              '下标 0、2、4 的段：`l`、`c**o`、空串 → ==在对外面==',
                                              '下标 1、3 的段含 4 个星号，在对里面，不算'])],
        one_liner='按竖线切开，只数下标为偶数的那几段',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['竖线 `|` 两两成对：第 1、2 个一对，第 3、4 个一对…',
                 '返回==不在竖线对之间==的 `*` 的个数',
                 '示例：`l|*e*et|c**o|*de|` → `2`'],
        quote='代码只有一行：对 s.split(\'|\') 取下标为偶数的段，累加每段里 \'*\' 的个数。',
        quote_src='—— 灵茶山艾府题解代码',
        idea=['`split(\'|\')` 之后，第 0 段在第一对竖线之前',
              '第 1 段在第一对里面，第 2 段在第一对和第二对之间……',
              '所以==偶数下标的段在对外面==，`[::2]` 一次取出，再数星号'],
        after=[dict(heading='结果怎么来的', lines=['偶数段 `l`、`c**o`、空串 的星号数：`0 + 2 + 0`',
                                           '`sum(...)` 把它们加起来 → ==2==',
                                           '整道题一行代码：思路全在 `split` 和 `[::2]` 上'])],
        summary=['时间 `O(n)`，空间 `O(n)`（切分出的段）',
                 '题目保证竖线个数为偶数，所以每个竖线恰好属于一对，奇偶规律成立',
                 '`[::2]` 取偶数下标：别写成 `[1::2]`（那是对里面的段）',
                 '对比 yiduobo：他用布尔标记 flag 一趟扫描，空间 `O(1)`'],
    ),
)
