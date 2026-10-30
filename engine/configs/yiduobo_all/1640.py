def _cmp(S):
    if 'p' not in S:
        return ''
    if 'num' in S and 'piece' in S and S['p'] < len(S['arr']):
        return f"对比 `piece` 里的 `{S['num']}` 与 `arr[{S['p']}] = {S['arr'][S['p']]}`"
    if S['p'] >= len(S['arr']):
        return '`p` 走到 arr 末尾：每一段都对上了'
    return f"`arr[{S['p']}] = {S['arr'][S['p']]}` 必然是某个 piece 的开头"


CONFIG = dict(
    num=1640, title='能否连接形成数组', difficulty='Easy', category='常用数据结构',
    author='yiduobo', technique='哈希表按首个数字找 piece',
    code='''
class Solution(object):
    def canFormArray(self, arr, pieces):

        p = 0
        piece_dict = {}
        for piece in pieces:
            piece_dict[piece[0]] = piece
        while p < len(arr):
            now = arr[p]
            if now not in piece_dict:
                return False
            
            piece = piece_dict[now]
            for num in piece:
                if num != arr[p]:
                    return False
                p += 1
            
        return True
''',
    call='Solution().canFormArray([91, 4, 64, 78], [[78], [4, 64], [91]])',
    expect=True,
    views=[
        dict(type='text', fn=_cmp),
        dict(type='array', var='arr', pointers={'p': 'blue'}, label='arr（只能整体重排 pieces，不能改段内顺序）', h=200,
             dim=lambda S, i, v: 'p' in S and i < S['p']),
        dict(type='map', var='piece_dict', fmt=lambda k, v: f'{k} → {v}', label='piece_dict：首个数字 → 整段 piece', h=240),
        dict(type='array', var='piece', label='当前匹配的 piece', h=150),
    ],
    watch=[('p', 'p', 'blue'), 'now', 'num'],
    captions={
        'p = 0': '`p` 指向 arr 里下一个要匹配的位置，从 0 开始',
        'piece_dict[piece[0]] = piece': '各数字互不相同 → 用 piece 的首个数字 `{piece[0]}` 当键，整段 `{piece}` 当值',
        'while p < len(arr)': lambda S, B, r: (f'`p = {S.p} < {len(S.arr)}`：arr 还没匹配完，继续' if S.p < len(S.arr) else f'`p = {S.p}` 已到末尾，不用再匹配'),
        'now = arr[p]': '`arr[{p}] = {now}`：它必然是某个 piece 的首个数字',
        'if now not in piece_dict': lambda S, B, r: (f'`{S.now}` 不是任何 piece 的开头 → 拼不出来' if S.now not in S.piece_dict else f'`{S.now}` 在 piece_dict 里 → 能找到对应的 piece'),
        'piece = piece_dict[now]': '按首个数字取出整段：`piece = {piece}`',
        'for num in piece': lambda S, B, r: ('这一段 piece 已经比完 → 回到 while，找下一段' if getattr(B, 'num', None) == S.num else f'取出 piece 中的下一个数字 `{S.num}`，去和 `arr[p]` 对比'),
        'if num != arr[p]': lambda S, B, r: (f'`{S.num} != arr[{S.p}] = {S.arr[S.p]}` → 不匹配，返回 False' if S.num != S.arr[S.p] else f'`{S.num} == arr[{S.p}]`，这一位对上了'),
        'p += 1': '对上了，`p` 后移到 {p}',
        'return True': 'arr 全部被 pieces 按序覆盖 → True',
    },
    cards=dict(
        one_liner='各数字互不相同：首个数字就能唯一定位 piece',
        complexity='时间 `O(n)`，空间 `O(m)`（m 为 pieces 个数）',
        problem=['`arr` 中数字互不相同，`pieces` 是若干段，段内顺序不能变',
                 '能否把 `pieces` 以任意顺序拼接，恰好得到 `arr`',
                 '示例：`arr=[91,4,64,78]`，`pieces=[[78],[4,64],[91]]` → `True`'],
        quote='由于题目中保证每个数字都不一样，那么只要知道了某个piece的首个数字，就可以通过哈希表对应地找个这个piece。',
        quote_src='—— yiduobo 题解原文',
        idea=['先建哈希表：piece 首个数字 → 整段 piece',
              '从 `p = 0` 扫 arr：`arr[p]` 必是某段的开头，查表取出这一段',
              '逐个对比这一段与 arr 往后的数字，对得上就推进 `p`，对不上返回 False'],
        summary=['时间 `O(n)`，空间 `O(m)`',
                 '易错：必须先查 `now in piece_dict`，否则取段时会 KeyError',
                 '依赖「数字互不相同」，否则首个数字不能唯一确定段',
                 '原文为 Python 2 风格，仅删去了类型说明文档字符串'],
    ),
)
