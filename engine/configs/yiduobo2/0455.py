def _gcolor(S, k, v):
    i = S.get('i')
    if i is None or 'res' not in S:
        return None
    if k < i:
        return 'green'
    if S.get('j', 0) >= len(S['s']) and k >= i:
        return 'red'
    return 'blue' if k == i else None


def _scolor(S, k, v):
    j = S.get('j')
    if j is None or 'res' not in S:
        return None
    return 'pink' if k == j else None


def _cmp(S):
    i, j = S.get('i'), S.get('j')
    if 'res' not in S or i is None or j is None:
        return ''
    g, s = S['g'], S['s']
    if i >= len(g) or j >= len(s):
        return f'`i = {i}`，`j = {j}`：' + ('孩子已经全部满足' if i >= len(g) else '饼干已经全部用完') + '，循环结束'
    return (f'孩子 `g[{i}] = {g[i]}` vs 饼干 `s[{j}] = {s[j]}` → '
            + ('==刚好够==，配对' if g[i] <= s[j] else '==不够==，换下一块更大的饼干'))


def _cap_while(S, B, ret):
    i, j, g, s = B['i'], B['j'], B['g'], B['s']
    if i < len(g) and j < len(s):
        return f'`i = {i} < {len(g)}` 且 `j = {j} < {len(s)}`：孩子和饼干都还有，继续配对'
    if i >= len(g):
        return f'`i = {i}`：所有孩子都分到了饼干，结束'
    return f'`j = {j} = len(s)`：饼干扫描完了，剩下的孩子只能饿着'


def _cap_if(S, B, ret):
    i, j, g, s = S['i'], S['j'], S['g'], S['s']
    if g[i] <= s[j]:
        return f'`g[{i}] = {g[i]} <= s[{j}] = {s[j]}`：当前孩子可以被当前饼干满足 → ==配对=='
    return f'`g[{i}] = {g[i]} > s[{j}] = {s[j]}`：这块饼干满足不了他，后面的孩子胃口更大，==也用不了它=='


CONFIG = dict(
    num=455, title='分发饼干', difficulty='Easy', category='贪心算法',
    author='yiduobo', technique='两个数组排序 + 双指针配对',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution(object):
    def findContentChildren(self, g, s):

        g = sorted(g)
        s = sorted(s)

        i = 0
        j = 0
        res = 0
        while i < len(g) and j < len(s):
            if g[i] <= s[j]:
                res += 1
                i += 1
            j += 1

        return res
''',
    call='Solution().findContentChildren([1, 2, 5, 3], [1, 4, 2, 1])',
    expect=3,
    views=[
        dict(type='text', fn=_cmp, h=60),
        dict(type='array', var='g', label='g（孩子的胃口，排序后；绿 = 已满足，红 = 没分到）', pointers={'i': 'blue'},
             color=_gcolor, h=230, cell=110),
        dict(type='array', var='s', label='s（饼干大小，排序后；灰 = 已经考察过）', pointers={'j': 'pink'},
             color=_scolor, dim=lambda S, k, v: 'res' in S and k < S['j'], h=230, cell=110),
    ],
    watch=[('i', 'i', 'blue'), ('j', 'j', 'pink'), ('res', 'res', 'green')],
    captions={
        'g = sorted(g)': '优先满足==需求少==的孩子 → 胃口从小到大排序：`g = {g}`',
        's = sorted(s)': '尽量用==刚好够==的饼干 → 饼干也排序：`s = {s}`',
        'i = 0': '指针 `i` 从 g 的头部开始扫描（当前孩子）',
        'j = 0': '指针 `j` 从 s 的头部开始扫描（当前饼干）',
        'res = 0': '`res` 记录配对成功的孩子数',
        'while i < len(g)': _cap_while,
        'if g[i] <= s[j]': _cap_if,
        'res += 1': '配对成功：`res` → {res}',
        'i += 1': '考察下一个孩子：`i` → {i}',
        'j += 1': '不论刚才配没配上，饼干 `s[{B.j}]` 都考察完了 → `j` → {j}',
        'return res': '一共满足了 =={ret}== 个孩子',
    },
    cards=dict(
        one_liner='胃口小的孩子先吃，每次用刚好够的那块饼干',
        complexity='时间 `O(n log n + m log m)`，空间 `O(n + m)`',
        problem=['每个孩子最多一块饼干；饼干 `s[j] >= g[i]` 才能满足孩子 `i`',
                 '问==最多能满足多少个孩子==',
                 '示例：`g = [1,2,5,3]`，`s = [1,4,2,1]` → `3`'],
        quote='应该优先满足对饼干需求少的孩子……对于某个孩子而言，使用刚刚好能满足这个孩子的饼干数是性价比最高的，因此也可以对饼干数进行排序，然后尽量用少的饼干去满足孩子。',
        quote_src='—— yiduobo 知乎题解',
        idea=['g 和 s 都从小到大排序，两个指针分别从头部往后扫描',
              '若 `g[i] <= s[j]`：当前孩子可以被当前饼干满足 → ==配对==，考察下一个孩子',
              '否则：这块饼干太小，`j` 往后移动，考察==下一份饼干=='],
        summary=['时间 `O(n log n + m log m)`；`sorted` 生成新数组，空间 `O(n + m)`',
                 '`j += 1` 写在 if 外面：==不论配没配上，这块饼干都考察完了==',
                 '循环条件两个都要判：孩子分完或饼干用完都该停',
                 '原文为 Python 2 风格，已删去类型文档字符串，代码未改'],
    ),
)
