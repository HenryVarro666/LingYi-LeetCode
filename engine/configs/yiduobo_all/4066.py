def _idx(S):
    return S.get('index')


def _color(S, i, v):
    k = S.get('index')
    return 'yellow' if k is not None and i in (k - 1, k) else None


def _txt(S):
    if 'pair' not in S:
        return ''
    best = max(S['pair'].values(), default=0)
    if S['_line'] >= 17:
        return f'答案 = 相等对 `res` + 最大不等对次数 = {S["res"] - best} + {best} = =={S["res"]}=='
    return f'`res` = ==本来就相等的对数== {S["res"]}，不等的对里出现最多的有 =={best}== 次'


CONFIG = dict(
    num=4066, title='至多一次替换后的最大相邻相等元素对数', difficulty='Medium', category='模拟',
    author='yiduobo', technique='哈希表记录不等对 + 取最大', tags=[],
    code='''
class Solution(object):
    def maxEqualAdjacentPairs(self, nums):
        
        res = 0
        pair = {}
        for index in range(1, len(nums)):
            ma = max(nums[index], nums[index - 1])
            mi = min(nums[index], nums[index - 1])

            if ma == mi:
                res += 1
            else:
                key = (ma, mi)
                pair[key] = pair.get(key, 0) + 1
        
        if pair:
            res += max(pair.values())
        
        return res
''',
    call='Solution().maxEqualAdjacentPairs([1,1,2,3,2,2,3])',
    expect=5,
    views=[
        dict(type='array', var='nums', label='nums（黄 = nums[index-1] 与 nums[index]）', h=190, pointers={'index': 'blue'}, color=_color),
        dict(type='map', var='pair', label='pair：不相等的相邻对 (大, 小) → 次数', fmt=lambda k, v: f'{k}: {v}', h=250, font=30),
        dict(type='text', h=110, size=28, fn=_txt),
    ],
    watch=[('index', 'index', 'blue'), ('ma', 'ma', 'pink'), ('mi', 'mi', 'cyan'), ('res', 'res', 'green')],
    captions={
        'res = 0': '`res` 先记下本来就相等的相邻对',
        'pair = {}': '`pair` 记录本来不相等的相邻对出现的次数',
        'for index in range': '看 `nums[{index - 1}]` 和 `nums[{index}]` 这一对',
        'ma = max': '较大的那个：`ma = {ma}`',
        'mi = min': '较小的那个：`mi = {mi}`',
        'if ma == mi': lambda S, B, r: (f'`ma == mi = {S.ma}`：这一对本来就相等' if S.ma == S.mi else f'`{S.ma} != {S.mi}`：这一对不相等，需要记下来'),
        'res += 1': '本来相等的对，无论怎么替换都还相等（要么没动，要么一起被换）→ `res` = {res}',
        'key = (ma, mi)': '按「大, 小」做 key，`({ma}, {mi})` 和 `({mi}, {ma})` 就算同一种',
        'pair[key] = ': '不等对 `{key}` 出现 =={pair[key]}== 次：把其中一个值换成另一个，这些对都会变相等',
        'if pair': '遍历完了，看有没有不等的对',
        'res += max(pair.values())': '只能替换一种，选出现最多的：`res` += {max(pair.values())} → =={res}==',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='本来相等的对不会变，再加上出现最多的那种不等对',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['选两个不同的值 `x`、`y`，把所有 `x` 换成 `y`（也可以不换），求相邻相等对最多多少',
                 '示例：`[1,2,3,2]` → `2`',
                 '本视频：`[1,1,2,3,2,2,3]` → `5`'],
        quote='对于一组本来就相等的相邻元素，那么无论怎样修改，这一组元素依然相等。……为了使得答案最大，那么显然应该选择出现次数最多的不同元素对，将其中一个元素修改为另一个元素。',
        quote_src='—— yiduobo 题解原文',
        idea=['先分两类：本来相等的对（修改后仍相等）、本来不等的对',
              '只有不等的对可能被「救回」，且一次只能救一种 `(x, y)`',
              '用哈希表数每种不等对的次数，累加最大值'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '易错：key 用「大, 小」排序，`(1,2)` 与 `(2,1)` 算同一种',
                 '没有不等对时 `pair` 为空，不能直接 `max`，所以先判断 `if pair`',
                 '对比灵神：灵神用 `pairwise` + `defaultdict`，这里手写下标 + `dict.get`'],
    ),
)
