def _col(S, i, v):
    if S.get('_line', 0) < 20 or 'first' not in S or 'v' not in S:
        return None
    if S['first'].get(S['v']) == i or S['last'].get(S['v']) == i:
        return 'green'
    return None


CONFIG = dict(
    num=1788, title='最大化花园的美观度', difficulty='Hard', category='常用数据结构',
    author='yiduobo', technique='首尾下标 + 非负前缀和',
    tags=['前缀和'],
    code='''
class Solution(object):
    def maximumBeauty(self, flowers):

        first = {}
        last = {}
        n = len(flowers)
        s = []
        for index, v in enumerate(flowers):
            if v not in first:
                first[v] = index
            last[v] = index
            
            v = max(v, 0)
            if index == 0:
                s.append(v)
            else:
                s.append(v + s[-1])
        
        res = -20001
        for v in first:
            if last[v] != first[v]:
                res = max(res, s[last[v] - 1] - s[first[v]] + v + v)
        
        return res
''',
    call='Solution().maximumBeauty([1,2,-3,1,2])',
    expect=5,
    views=[
        dict(type='array', var='flowers', h=170, label='flowers（绿=当前颜色的最左/最右）',
             color=lambda S, i, v: _col(S, i, v)),
        dict(type='array', var='s', h=170, label='s：只累加非负数的前缀和'),
        dict(type='map', var='first', h=110, label='first（颜色 → 最左下标）'),
        dict(type='map', var='last', h=110, label='last（颜色 → 最右下标）'),
    ],
    watch=['index', 'v', ('res', 'res', 'green')],
    skip=['n = len'],
    captions={
        'first = {}': '`first[v]` 记颜色 v 第一次出现的位置，`last[v]` 记最后一次——只有最外层的同色花才可能是最优端点',
        'if v not in first': '颜色 `{v}` {"还没出现过" if v not in first else "已出现过"}',
        'first[v] = index': '第一次见到颜色 `{v}`，记下最左位置 `{index}`',
        'last[v] = index': '`last[{v}] = {index}`：每次遇到都覆盖，最后留下最右位置',
        'v = max(v, 0)': '负数花不能放在区间两端，但中间可以不选 → 前缀和里按 `max(v, 0)` 算，得到 `{v}`',
        'if index == 0': lambda S, B, ret: ('第一朵花：前缀和就是它自己（负数按 0 计）' if S['index'] == 0 else '不是第一朵：前缀和要接在上一项后面'),
        's.append(v)': '`s` 末尾加入 `{v}`，现在 `s` 为 `{s}`',
        's.append(v + s[-1])': '`s` 末尾加入 `{v} + {B.s[-1]} = {s[-1]}`（累计的非负花美观度）',
        'res = -20001': '`res` 初始为题目允许的最小值下界 `-20001`',
        'for v in first': lambda S, B, ret: ('颜色都枚举完了' if B.get('v') == S['v'] and 'res' in B else f"枚举颜色 `{S['v']}`，最左 `{S['first'][S['v']]}`，最右 `{S['last'][S['v']]}`"),
        'if last[v] != first[v]': '颜色 `{v}` {"出现至少两次，可以作为两端" if last[v] != first[v] else "只出现一次，不能作为两端，跳过"}',
        'res = max(res': '区间内取非负：`s[{last[v]-1}] - s[{first[v]}] = {s[last[v]-1] - s[first[v]]}`，再加两端 `{v} + {v}` → 候选 `{s[last[v]-1] - s[first[v]] + v + v}`，取大后 `res` 为 =={res}==',
        'return res': '所有颜色比较完，最大美观度 =={ret}==',
    },
    cards=dict(
        one_liner='同色花取最外侧两朵，中间只保留非负的花',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`flowers[i]` 是第 i 朵花的美观度，要删花使花园「有效」：至少两朵，且首尾美观度相同',
                 '求有效花园的最大美观度总和',
                 '示例：`[1,2,-3,1,2]` → 保留 `2,1,2` = `5`'],
        quote='l 一定是花园中最左侧的 v，r 则是花园中最右侧的 v，理由是如果外侧还存在其他的 v，那么就可以将 l 和 r 向外侧移动。',
        quote_src='—— yiduobo 题解',
        idea=['同色的端点越靠外越好：多出来的花只留非负的，不会变差',
              '一趟遍历记录每种颜色 `first` / `last`，同时算「非负数前缀和」`s`',
              '候选值 = `s[last-1] - s[first]`（中间非负花） + 两端 `v + v`'],
        summary=['复杂度：`O(n)`',
                 '易错点：两端花即使是负数也必须选，所以单独加 `v + v`',
                 '只出现一次的颜色不能做端点',
                 '前缀和里的负数按 0 计，因为中间的负花可以删掉',
                 '原文已是 Python 3 写法，未做修改'],
    ),
)
