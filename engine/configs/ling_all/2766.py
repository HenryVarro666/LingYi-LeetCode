CONFIG = dict(
    num=2766, title='重新放置石块', difficulty='Medium', category='常用数据结构',
    author='灵茶山艾府', technique='哈希集合维护石块位置',
    tags=[],
    code='''
class Solution:
    def relocateMarbles(self, nums: List[int], moveFrom: List[int], moveTo: List[int]) -> List[int]:
        st = set(nums)
        for f, t in zip(moveFrom, moveTo):
            st.remove(f)
            st.add(t)
        return sorted(st)
''',
    call='Solution().relocateMarbles([1,6,7,8], [1,7,2], [2,9,5])',
    expect=[5, 6, 8, 9],
    views=[
        dict(type='array', var='moveFrom', label='moveFrom（蓝 = 当前这次的起点 f）', h=170,
             color=lambda S, i, v: 'blue' if 'f' in S and v == S['f'] and S['_line'] in (6, 7) else None),
        dict(type='array', var='moveTo', label='moveTo（粉 = 当前这次的终点 t）', h=170,
             color=lambda S, i, v: 'pink' if 't' in S and v == S['t'] and S['_line'] in (6, 7) else None),
        dict(type='set', var='st', label='st：现在有石块的位置', h=260, fmt=lambda x: str(x)),
    ],
    watch=[('f', 'f', 'blue'), ('t', 't', 'pink')],
    captions={
        'st = set(nums)': '用集合存位置：只关心==有没有==石块，不关心有几块。`st = {st}`',
        'for f, t in zip': lambda S, B, r: ('所有操作做完了' if 'f' in B and S.f == B.f and S.t == B.t
                                            else f'这一步：把位置 `{S.f}` 的石块全部搬到 `{S.t}`'),
        'st.remove(f)': '`{f}` 处的石块全搬走（题目保证那里有石块），`{f}` 从集合里去掉',
        'st.add(t)': '搬到 `{t}`：加入集合。若 `{t}` 本来就有石块，集合自动去重 → `st = {st}`',
        'return sorted': '集合无序，从小到大排序返回 `{sorted(st)}`',
    },
    cards=dict(
        one_liner='每次操作：去掉起点，加上终点；最后排序',
        complexity='时间 `O(n log n + m)`，空间 `O(n)`',
        problem=['`nums` 是石块初始位置，第 `i` 次把 `moveFrom[i]` 处==所有==石块移到 `moveTo[i]`',
                 '最后按升序返回有石块的位置',
                 '示例：`[1,6,7,8]`，`[1,7,2]→[2,9,5]` → `[5,6,8,9]`'],
        quote='这个过程并不关心每个位置有多少石块。所以只需用哈希集合来维护这些石头的位置，不需要维护每个位置有多少石块。',
        quote_src='—— 灵茶山艾府题解',
        idea=['同一位置的石块总是一起走，所以数量无关紧要',
              '集合里放位置：先 `remove(f)` 再 `add(t)`',
              '最后 `sorted(st)` 得到升序结果'],
        summary=['时间 `O(n log n + m)`，排序是瓶颈；空间 `O(n)`',
                 '先删 `f` 再加 `t`，题目保证 `f` 处有石块，所以 `remove` 不会报错',
                 '`f == t` 时先删后加，位置仍保留，顺序别反',
                 '同类：用集合/哈希表只维护「是否存在」'],
    ),
)
