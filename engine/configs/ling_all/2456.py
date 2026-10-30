def _cur(S):
    if 'name' not in S or 'view' not in S:
        return '遍历每个视频，哈希表 `m[创作者] = [播放总和, 最大播放量, 最大播放量的 id]`'
    return f"当前视频：创作者 `{S['name']}`，id `{S['id']}`，播放 =={S['view']}=="


def _fmt(k, v):
    return f'{k}: 总和 {v[0]} · 最大 {v[1]} · id {v[2]}'


CONFIG = dict(
    num=2456, title='最流行的视频创作者', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表 · 一次遍历记总和/最大值',
    tags=[],
    code='''
class Solution:
    def mostPopularCreator(self, creators: List[str], ids: List[str], views: List[int]) -> List[List[str]]:
        m, max_view_sum = {}, 0
        for name, id, view in zip(creators, ids, views):
            if name in m:
                t = m[name]
                t[0] += view
                if view > t[1] or view == t[1] and id < t[2]:
                    t[1], t[2] = view, id
            else: m[name] = [view, view, id]
            max_view_sum = max(max_view_sum, m[name][0])
        return [[name, id] for name, (view_sum, _, id) in m.items() if view_sum == max_view_sum]
''',
    call='Solution().mostPopularCreator(["alice","bob","alice","chris"], ["one","two","three","four"], [5,10,5,4])',
    expect=[["alice", "one"], ["bob", "two"]],
    views=[
        dict(type='text', fn=_cur, size=28, h=90),
        dict(type='array', var='creators', label='creators（蓝 = 当前视频的创作者）', cell=108, h=225,
             color=lambda S, i, v: 'blue' if 'view' in S and i == [k for k in range(len(S['creators'])) if S['ids'][k] == S['id']][0] else None),
        dict(type='array', var='views', label='views', cell=108, h=225,
             color=lambda S, i, v: 'blue' if 'view' in S and S['ids'][i] == S['id'] else None),
        dict(type='map', var='m', label='m：创作者 → [播放总和, 最大播放量, id]', fmt=_fmt, font=30, h=230),
        dict(type='text', fn=lambda S: f"当前最高总播放量 `max_view_sum` = =={S['max_view_sum']}==" if 'max_view_sum' in S else '', size=28, h=70),
    ],
    watch=[('name', 'name', 'blue'), ('id', 'id', 'pink'), ('view', 'view', 'orange'), ('max_view_sum', 'max_view_sum', 'green')],
    captions={
        'm, max_view_sum = {}, 0': '`m` 记录每个人的数据；`max_view_sum` 记录目前最高的总播放量',
        'for name, id, view in zip': lambda S, B, r: f'下一个视频：`{S.name}` 的 `{S.id}`，播放 {S.view}' if 'name' in S and (S.name, S.id) != (B.get('name'), B.get('id')) else '视频全部处理完',
        'if name in m': lambda S, B, r: (f'`{S.name}` 以前出现过 → 更新他的数据' if S.name in S.m else f'`{S.name}` 第一次出现 → 新建记录'),
        't = m[name]': '`t` 就是 `{name}` 的记录 `{t}`（列表，改 `t` 就是改 `m`）',
        't[0] += view': '总和累加 `{view}` → `{t[0]}`',
        'if view > t[1]': lambda S, B, r: (
            f'`{S.view} > {S.t[1]}`：播放量更大 → 更新最佳视频' if S.view > S.t[1]
            else (f'播放量相同，`{S.id!r} < {S.t[2]!r}`：id 字典序更小 → 更新' if S.view == S.t[1] and S.id < S.t[2]
                  else (f'播放量相同，但 `{S.id!r}` 字典序不更小 → 不更新' if S.view == S.t[1]
                        else f'`{S.view} < {S.t[1]}`：不如已有最佳 → 不更新'))),
        't[1], t[2] = view, id': '最佳视频改为 `{id!r}`，播放量 `{view}`',
        'else: m[name]': '第一次出现：总和 = 最大 = `{view}`，最佳视频 = `{id!r}` → `m[{name!r}] = {m[name]}`',
        'max_view_sum = max': '`{name}` 的总和是 `{m[name][0]}`：`max_view_sum = max({B.max_view_sum}, {m[name][0]})` = =={max_view_sum}==',
        'return [[name': lambda S, B, r: f'遍历 `m`，保留总和等于 `{S.max_view_sum}` 的创作者（并列最高都要）→ `{r}`',
    },
    max_steps=60,
    cards=dict(
        one_liner='哈希表记每人总播放、最大播放和对应 id',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['流行度 = 创作者所有视频播放量之和；找出流行度==最高==的创作者（可并列）',
                 '每人还要给出播放量最大的视频 id，并列时取字典序最小的',
                 '示例：alice 总 10（最佳 one）、bob 总 10（最佳 two）→ `[["alice","one"],["bob","two"]]`'],
        quote='遍历，哈希表统计每个人的：播放量的总和 viewSum；最大播放量 maxView；最大播放量对应的视频 id。最后遍历哈希表，得到答案。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`m[name] = [总和, 最大播放量, id]`，每个视频进来就更新三项',
              '更新 id 的条件：播放量更大，或 ==播放量相同且 id 字典序更小==',
              '遍历时顺便维护 `max_view_sum`，最后一次推导式筛出所有并列最高的人'],
        summary=['时间 `O(n)`，空间 `O(n)`（字符串长度视为常数）',
                 '易错：并列最高的创作者都要返回，不能只取一个',
                 '易错：同播放量时 id 要比字典序，不是比先后',
                 '`t = m[name]` 取到的是列表引用，改 `t` 就等于改 `m[name]`'],
    ),
)
