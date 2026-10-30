SETUP = '''
import sys


class Seq(list):
    """和 list 完全一样，只是被题解代码 for 遍历时把当前下标记在 pos 上（方便动画画出 for x in s 的位置）"""
    def __iter__(self):
        if sys._getframe(1).f_code.co_filename != '<solution>':
            return list.__iter__(self)
        return self._walk()

    def _walk(self):
        for k in range(len(self)):
            self.pos = k
            yield self[k]
        self.pos = len(self)
'''


def _j(S):
    """当前饼干在 s 里的下标；遍历结束后为 None"""
    s = S.get('s')
    k = getattr(s, 'pos', None)
    if k is None or k >= len(s) or 'x' not in S:
        return None
    return k


def _gcolor(S, k, v):
    i = S.get('i')
    if i is None:
        return None
    if k < i:
        return 'green'
    s = S.get('s')
    if getattr(s, 'pos', 0) >= len(s):
        return 'red'  # 饼干用完了，剩下的孩子吃不饱
    if k == i:
        return 'blue'
    return None


def _scolor(S, k, v):
    j = _j(S)
    if j is None:
        return None
    if k == j:
        return 'pink'
    return None


def _cmp(S):
    if _j(S) is None:
        return ''
    i, n, g, x = S['i'], S['n'], S['g'], S['x']
    if S.get('_line') == 9:
        i -= 1
    if i >= n:
        return f'`i = {i} = n`：所有孩子都已满足，剩下的饼干用不上'
    ok = g[i] <= x
    return (f'最小胃口 `g[{i}] = {g[i]}` vs 当前饼干 `x = {x}` → '
            + ('==能满足==，分给他' if ok else '==太小==，谁都喂不饱，跳过'))


def _cap_if(S, B, ret):
    i, n, g, x = B['i'], B['n'], B['g'], B['x']
    if i >= n:
        return f'`i = {i}`，孩子都分完了 → 这块饼干没用'
    if g[i] <= x:
        return f'`g[{i}] = {g[i]} <= {x}`：最小的饼干给==胃口最小==的孩子，不浪费'
    return f'`g[{i}] = {g[i]} > {x}`：连胃口最小的孩子都不够 → ==这块饼干给谁都没用==，丢掉'


CONFIG = dict(
    num=455, title='分发饼干', difficulty='Easy', category='贪心算法',
    author='灵茶山艾府', technique='排序 + 双指针',
    tags=['字节3个月', '字节6个月'],
    code='''
class Solution:
    def findContentChildren(self, g: List[int], s: List[int]) -> int:
        g.sort()
        s.sort()
        n = len(g)
        i = 0
        for x in s:
            if i < n and g[i] <= x:
                i += 1
        return i
''',
    setup=SETUP,
    call='Solution().findContentChildren(Seq([2, 3, 7, 4]), Seq([5, 1, 3, 2]))',
    expect=3,
    views=[
        dict(type='text', fn=_cmp, h=60),
        dict(type='array', var='g', label='g（孩子的胃口，绿 = 已满足，红 = 吃不饱，i 指向下一个要满足的）', pointers={'i': 'blue'},
             color=_gcolor, h=230, cell=110),
        dict(type='array', var='s', label='s（饼干尺寸，从小到大遍历）', pointers={'s.pos if s.pos < len(s) else None': 'pink'},
             pointer_labels={'s.pos if s.pos < len(s) else None': 'x'},
             color=_scolor, dim=lambda S, k, v: k < getattr(S['s'], 'pos', -1), h=230, cell=110),
    ],
    watch=[('n', 'n'), ('x（当前饼干）', 'x', 'pink'), ('i（已满足的孩子数）', 'i', 'blue')],
    captions={
        'g.sort()': '把胃口==从小到大排序==：`g = {g}`',
        's.sort()': '饼干也从小到大排序：`s = {s}`',
        'n = len(g)': '`n = {n}` 个孩子',
        'i = 0': '`i` 指向==胃口最小的未满足孩子==，同时也是已满足的人数',
        'for x in s': lambda S, B, ret: (f'考虑当前==最小==的饼干 `x = {S["x"]}`' if _j(S) is not None else '饼干全部考虑完，循环结束'),
        'if i < n and': _cap_if,
        'i += 1': '饼干分给孩子 `{i - 1}`，`i` → {i}：下一个孩子胃口更大',
        'return i': '`i` 增加的次数就是满足的孩子数：返回 =={ret}==',
    },
    cards=dict(
        one_liner='最小的饼干，要么谁都喂不饱，要么给胃口最小的孩子',
        complexity='时间 `O(n log n + m log m)`，空间 `O(1)`',
        problem=['每个孩子最多分一块饼干；孩子 `i` 胃口 `g[i]`，饼干 `j` 尺寸 `s[j]`',
                 '`s[j] >= g[i]` 时孩子 `i` 被满足，求==最多能满足几个孩子==',
                 '示例：`g = [2,3,7,4]`，`s = [5,1,3,2]` → `3`（胃口 7 的孩子吃不饱）'],
        quote='想一想，尺寸最小的饼干，应该给哪个孩子？如果这个饼干的尺寸 x 比最小的 g[i] 还小，那么无法给任何孩子。否则，这个饼干应该给最小的 g[i]。',
        quote_src='—— 灵茶山艾府题解',
        idea=['交换论证：若 `x` 配了大胃口孩子、更大的 `y` 配了最小胃口孩子，==交换后仍成立==',
              '所以总能让最小饼干 `x` 去配胃口最小的孩子',
              '排序后：外层遍历饼干 `x`，指针 `i` 指向胃口，能喂饱就 `i += 1`'],
        summary=['时间 `O(n log n + m log m)`，瓶颈在排序；空间 `O(1)`',
                 '易错：先判 `i < n` 再访问 `g[i]`，否则孩子都满足后会越界',
                 '`i` 既是指针也是答案，不用另开计数器',
                 '同类：2410 运动员和训练师的最大匹配数（完全相同）'],
    ),
)
