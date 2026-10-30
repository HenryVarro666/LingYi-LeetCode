def _formula(S):
    if 'res' not in S or 'index' not in S or 'p' not in S or 'tot' not in S or 'cnt' not in S or 's' not in S:
        return '先统计每个值的下标总和 `s[v]` 与个数 `tot[v]`，再从头扫一遍，边扫边累计前缀'
    i = S['index']
    v = S['v']
    if not S['res'] or len(S['res']) <= i and S.get('_line', 0) < 18:
        return f'位置 `{i}`（值 {v}）：前缀 `p[{v}]` 和个数 `cnt[{v}]` 正在更新'
    c, pp, ss, t = S['cnt'][v], S['p'][v], S['s'][v], S['tot'][v]
    return (f'前半 `{c}×{i} − {pp}` = =={c * i - pp}==，后半 `({ss} − {pp}) − ({t} − {c})×{i}` = =={(ss - pp) - (t - c) * i}==')


CONFIG = dict(
    num=2615, title='等值距离和', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='按值累计前缀和',
    tags=['前缀和', '难度分 1793'],
    code='''
class Solution(object):
    def distance(self, nums):

        s = {}
        tot = {}
        for index, v in enumerate(nums):
            s[v] = s.get(v, 0) + index
            tot[v] = tot.get(v, 0) + 1
        
        res = []
        p = {}
        cnt = {}
        for index, v in enumerate(nums):
            p[v] = p.get(v, 0) + index
            cnt[v] = cnt.get(v, 0) + 1
            res.append(cnt[v] * index - p[v] + (s[v] - p[v]) - (tot[v] - cnt[v]) * index)

        return res
''',
    call='Solution().distance([1,3,1,1,3])',
    expect=[5, 3, 3, 4, 3],
    views=[
        dict(type='array', var='nums', label='nums', h=190, pointers={'index': 'blue'}),
        dict(type='text', fn=lambda S: '总量（第一趟）  `s` = ' + str(S.get('s', {})) + '   `tot` = ' + str(S.get('tot', {})), h=50),
        dict(type='text', fn=lambda S: '已扫过（第二趟）  `p` = ' + str(S.get('p', {})) + '   `cnt` = ' + str(S.get('cnt', {})), h=50),
        dict(type='array', var='res', label='res', h=130),
        dict(type='text', fn=_formula, h=60),
    ],
    watch=['index', 'v', ('res', 'res', 'green')],
    captions={
        's = {}': '`s[v]`：值为 v 的所有下标之和（总和）',
        'tot = {}': '`tot[v]`：值为 v 的下标个数（总数）',
        's[v] = s.get': '位置 `{index}` 值 `{v}`：`s[{v}]` = {s[v]}',
        'tot[v] = tot.get': '`tot[{v}]` = {tot[v]}',
        'res = []': '第一趟统计完毕：总和 `s = {s}`，总数 `tot = {tot}`',
        'p = {}': '`p[v]`：从左往右已扫过的、值为 v 的下标之和（前缀和）',
        'cnt = {}': '`cnt[v]`：已扫过的、值为 v 的个数（含当前位置）',
        'p[v] = p.get': '边扫边累计：`p[{v}]` = 到当前位置为止，值 {v} 的下标之和 = {p[v]}',
        'cnt[v] = cnt.get': '`cnt[{v}]` = 到当前位置为止（含自己）值 {v} 的个数 = {cnt[v]}',
        'res.append': lambda S, B, r: (f'前半（左边）`cnt×i − p` = `{S.cnt[S.v]}×{S.index} − {S.p[S.v]}` = {S.cnt[S.v] * S.index - S.p[S.v]}；'
                                       f'后半（右边）`(s−p) − (tot−cnt)×i` = {(S.s[S.v] - S.p[S.v]) - (S.tot[S.v] - S.cnt[S.v]) * S.index}'
                                       f' → ==res 末尾加入 {S.res[-1]}=='),
        'return res': '每个位置的距离和都算好了：`{res}`',
    },
    cards=dict(
        one_liner='拆掉绝对值：一个乘法减前缀和，加后缀和减乘法',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`arr[i]` = 所有同值且 `j≠i` 的 `|i−j|` 之和，没有则为 `0`',
                 '示例：`[1,3,1,1,2]` → `[5,0,3,4,0]`',
                 '本视频：`[1,3,1,1,3]` → `[5,3,3,4,3]`'],
        quote='对于前面的这些项，拆掉绝对值之后就是 p[i] * (i + 1) - sum(p[0: i + 1])，即一个乘法与一个前缀和之差。',
        quote_src='—— yiduobo 题解原文',
        idea=['只有==值相同==的位置互相影响，按值各自处理',
              '同值下标升序：比自己小的拆成 `p[i]×个数 − 前缀和`，比自己大的拆成 `后缀和 − p[i]×个数`',
              '前缀和 + 后缀和 = 总和，所以先扫一趟存总和与总数，再扫一趟边累计边算'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '不用先分组存下标：用 `s/tot` 记总量，`p/cnt` 记已扫过的量，`后缀 = s − p`',
                 '`cnt` 含自己，所以前半 `cnt×i − p` 里自己那项恰好是 0',
                 '对比灵神：灵神先分组再前缀和；yiduobo 两趟扫描直接出结果'],
    ),
)
