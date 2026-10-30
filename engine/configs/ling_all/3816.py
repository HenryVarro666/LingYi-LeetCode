CODE = '''
class Solution:
    def lexSmallestAfterDeletion(self, s: str) -> str:
        left = Counter(s)

        st = []
        for ch in s:
            # 如果 ch 比栈顶小，移除栈顶，可以让字典序更小
            while st and ch < st[-1] and left[st[-1]] > 1:
                left[st.pop()] -= 1
            st.append(ch)

        # 最后，移除末尾的重复字母，可以让字典序更小
        while left[st[-1]] > 1:
            left[st.pop()] -= 1

        return ''.join(st)
'''
_L = CODE.strip('\n').split('\n')
LN_APP = [i for i, l in enumerate(_L, 1) if 'st.append(ch)' in l][0]
LN_TAIL = [i for i, l in enumerate(_L, 1) if l.strip().startswith('while left[st[-1]]')][0]


def _idx(S):
    """当前处理的下标：已入栈的 + 已删掉的 = 已处理的个数"""
    if 'st' not in S or 'ch' not in S or S['_line'] >= LN_TAIL:
        return None
    done = len(S['st']) + len(S['s']) - sum(S['left'].values())
    i = done if S['_line'] < LN_APP else done - 1
    return i if 0 <= i < len(S['s']) else None


def _show(S):
    if 'st' not in S:
        return '`left[x]` = 字母 x 现在还剩几个（栈里 + 右边），==大于 1 才能删=='
    t = ''.join(S['st'])
    if S['_line'] >= LN_TAIL:
        if S['st']:
            x = S['st'][-1]
            return f'收尾　栈 `"{t}"`　栈顶 `{x}` 还剩 ==`{S["left"][x]}`== 个'
        return '栈空了'
    i = _idx(S)
    if i is None:
        return f'栈 `"{t}"`'
    if S['st'] and S['_line'] < LN_APP:
        x = S['st'][-1]
        return f'`{S["ch"]}` vs 栈顶 `{x}`　`left[{x}] = {S["left"][x]}`'
    return f'栈 `"{t}"`'


def _while(S, B, ret):
    ch, st, left = S.ch, S.st, S.left
    if not st:
        return '栈空了 → 没有可删的，直接入栈'
    x = st[-1]
    if ch < x and left[x] > 1:
        return f'`{ch} < {x}`，且 `left[{x}] = {left[x]} > 1`（还有别的 {x}）→ ==删掉栈顶，字典序变小=='
    if ch < x:
        return f'`{ch} < {x}` 但 `left[{x}] = 1`，它是==最后一个==，不能删'
    return f'`{ch} ≥ {x}`：删掉栈顶不会让字典序更小 → 停止'


def _tail(S, B, ret):
    if not S.st:
        return '栈空了，结束'
    x = S.st[-1]
    if S.left[x] > 1:
        return f'末尾 `{x}` 还有重复（`left = {S.left[x]}`）→ ==删掉它，前缀不变但更短，字典序更小=='
    return f'末尾 `{x}` 只剩一个，必须保留 → 停止'


CONFIG = dict(
    num=3816, title='删除重复字符后的字典序最小字符串', difficulty='Hard', category='单调栈',
    author='灵茶山艾府', technique='单调栈 · 类似 316 题',
    tags=['最小字典序', '难度分 2377'],
    code=CODE,
    call='Solution().lexSmallestAfterDeletion("dbcaddb")',
    expect='bcad',
    views=[
        dict(type='string', var='s', label='s（蓝 = 当前字母 ch，灰 = 已处理）', cell=96, h=215,
             pointers={_idx: 'blue'}, pointer_labels={_idx: 'ch'},
             dim=lambda S, i, v: _idx(S) is not None and i < _idx(S),
             color=lambda S, i, v: 'blue' if i == _idx(S) else None),
        dict(type='stack', var='st', label='st（栈，栈顶在右）', h=150, font=34),
        dict(type='map', var='left', label='left（还剩几个，栈里 + 右边）', fmt=lambda k, v: f"'{k}': {v}", h=160, font=30),
        dict(type='text', fn=_show, size=28, h=90),
    ],
    watch=[('ch', 'ch', 'blue'), ('st', "''.join(st)", 'green')],
    captions={
        'left = Counter': '先统计每个字母的个数：`left[x] > 1` 才说明 x 能删掉一个',
        'st = []': '`st` 当栈，里面是目前字典序最小的结果',
        'for ch in s': lambda S, B, ret: (f'读入第 `{_idx(S)}` 个字母 `{S.ch}`' if _idx(S) is not None else '遍历结束，进入收尾'),
        'while st and': _while,
        'left[st.pop()] -= 1': lambda S, B, ret: (f'删掉栈顶 `{B.st[-1]}`，它还剩 `{S.left[B.st[-1]]}` 个' if B.st else '删掉栈顶'),
        'st.append(ch)': lambda S, B, ret: f'`{S.ch}` 入栈 → `st = "{"".join(S.st)}"`',
        'while left[st[-1]]': _tail,
        'return': '得到字典序最小的结果 `"{ret}"`',
    },
    cards=dict(
        one_liner='和 316 类似，但「能删」的条件是还有重复',
        complexity='时间 `O(n + |Σ|)`，空间 `O(n)`',
        problem=['每次可删掉当前字符串里==至少出现两次==的某个字母的一次出现',
                 '求能得到的字典序最小的字符串',
                 '示例：`"aaccb"` → `"aacb"`；本视频：`"dbcaddb"` → `"bcad"`'],
        quote='如果 ch 比栈顶小，移除栈顶，可以让字典序更小',
        quote_src='—— 灵茶山艾府题解代码注释',
        idea=['做法类似 316：新字母比栈顶小，就想删掉栈顶',
              '区别：能删的条件是 `left[栈顶] > 1`，即还剩别的同字母',
              '遍历后还要把末尾的重复字母删掉：更短的前缀字典序更小'],
        summary=['时间 `O(n)`，空间 `O(n)`（栈长度可能接近 n）',
                 '`left` 记录的是栈里 + 右边的个数，弹栈要同步减一',
                 '易错：收尾 `while` 不能漏，否则 `"dbcaddb"` 末尾会留着重复的 `d`',
                 '对比 316：那里删了的字母必须能在右边补回来；这里删了就真的没了'],
    ),
)
