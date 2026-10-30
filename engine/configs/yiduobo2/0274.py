def _done(S):
    return sum((S.get('count') or {}).values())


def _cit_color(S, i, v):
    if 'total' in S and 'num' in S:
        return 'cyan' if v >= S['num'] else None
    if 'count' not in S:
        return None
    d = _done(S)
    if S.get('_line') in (5, 6) and i == d:
        return 'yellow'
    if S.get('_line') == 7 and i == d - 1:
        return 'yellow'
    if i < d:
        return 'green'
    return None


def _suffix(S):
    if 'count' not in S or 'citations' not in S:
        return None
    n = len(S['citations'])
    return [S['count'].get(x, 0) for x in range(n + 1)]


def _suf_color(S, i, v):
    if 'total' in S and 'num' in S:
        if i == S['num']:
            return 'yellow'
        if i > S['num']:
            return 'cyan'
    return None


def _info(S):
    if 'total' in S and 'num' in S and S.get('_line') in (10, 11, 12, 13):
        h, t = S['num'], S['total']
        c = S['count'].get(h, 0)
        return f"枚举 `h = {h}`：引用数 `> {h}` 的有 `total = {t}` 篇，引用数 `= {h}` 的有 `{c}` 篇"
    if 'count' in S:
        return f"引用次数 `> {len(S['citations'])}`（文章总数）的，缩减为 `{len(S['citations'])}`"
    return ''


CONFIG = dict(
    num=274, title='H 指数', difficulty='Medium', category='普通数组',
    author='yiduobo', technique='dict 计数 + 从大到小枚举 h（后缀和）',
    tags=['字节30天', '面试经典150'],
    code='''
class Solution(object):
    def hIndex(self, citations):
        count = {}
        for num in citations:
            if num > len(citations):
                num = len(citations)
            count[num] = count.get(num, 0) + 1

        total = 0
        for num in range(len(citations), -1, -1):
            if total + count.get(num, 0) >= num:
                return num
            total += count.get(num, 0)

        return 0
''',
    call='Solution().hIndex([0, 8, 4, 5, 2, 3])',
    expect=3,
    views=[
        dict(type='text', fn=_info, size=26, h=60),
        dict(type='array', var='citations', label='citations（绿 = 已统计；枚举阶段青 = 引用 ≥ h）', cell=90, h=150,
             color=_cit_color),
        dict(type='map', var='count', label='count（dict：引用数 → 文章篇数）', h=100),
        dict(type='array', var=_suffix, label='按引用数排开：count.get(x, 0)，x = 0..n（青 = 已累加进 total）', cell=90,
             color=_suf_color, h=150),
    ],
    watch=[('num', 'num', 'yellow'), ('total', 'total', 'cyan'), ('count.get(num, 0)', 'count.get(num, 0)')],
    captions={
        'count = {}': '`count[x]`：引用数为 x 的文章有多少篇',
        'for num in citations': lambda S, B, ret: (f'下一篇文章：引用 `{S.num}` 次' if _done(S) < len(S.citations)
                                                   else '所有文章都统计完了'),
        'if num > len(citations)': lambda S, B, ret: (
            f'`{S.num} > {len(S.citations)}`：==h 至多为文章总数==，多出来的引用没有意义' if S.num > len(S.citations)
            else f'`{S.num} ≤ {len(S.citations)}`，不用缩减'),
        'num = len(citations)': '缩减：`num = {num}`',
        'count[num] = count.get': '`count[{num}]` +1 → `{count[num]}`',
        'total = 0': '`total`：引用数 ==大于== 当前 h 的文章数（后缀和）',
        'for num in range': lambda S, B, ret: (f'从文章总数开始，==从大到小枚举 h==：`h = {S.num}`' if S.num == len(S.citations)
                                               else f'下一个 `h = {S.num}`'),
        'if total + count.get(num, 0) >= num': lambda S, B, ret: (
            f'引用数 `≥ {S.num}` 的文章 `= total + count[{S.num}] = {S.total} + {S.count.get(S.num, 0)} = {S.total + S.count.get(S.num, 0)}`'
            + (f' `≥ {S.num}` → ==h = {S.num} 满足==' if S.total + S.count.get(S.num, 0) >= S.num else f' `< {S.num}` → 不满足')),
        'return num': '从大到小第一个满足的就是最大的 h：返回 =={ret}==',
        'total += count.get': '`total += count[{B.num}]` → `{total}`：后缀和往下延伸一格',
    },
    cards=dict(
        one_liner='引用数缩到文章总数以内，再从大到小枚举 h，用后缀和判断',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`citations[i]` 是第 i 篇论文的被引次数，求 ==h 指数==',
                 'h 指数：==至少有 h 篇论文被引用了至少 h 次==，取最大的 h',
                 '示例：`[3,0,6,1,5]` → `3`；本视频：`[0,8,4,5,2,3]` → `3`'],
        quote='首先，==h至多为文章的总数==，于是当一篇文章的引用次数多于文章的总数时，我们可以将引用次数置为文章总数。……从文章总数开始，从大到小枚举h，==通过后缀和的方式判断==。',
        quote_src='—— yiduobo 题解原文',
        idea=['引用数 `> n` 的文章缩减为 `n`：所有引用数都落在 `0..n` 里',
              '用 dict `count` 记下每个引用数有几篇文章',
              '`h` 从 `n` 往下枚举，`total` 累加引用数 `> h` 的篇数；`total + count[h] ≥ h` 就找到了'],
        result='h 指数为 `3` ✓',
        summary=['时间 `O(n)`：统计一遍 + 最多枚举 `n + 1` 个 h',
                 '先判断 `total + count[h] ≥ h` 再把 `count[h]` 加进 total：total 始终是「大于 h」的篇数',
                 '`h = 0` 时条件一定成立，最后的 `return 0` 只是兜底',
                 '原文为 Python 2 写法，只删去了类型说明文档字符串，代码未改',
                 '对比灵神：思路相同；灵神用数组计数、先累加再判断，yiduobo 用 dict、先判断再累加'],
    ),
)
