def _pos(S):
    """now 对应已累加到第几个字符"""
    if 'now' not in S:
        return None
    acc = 0
    for k, ch in enumerate(S['s']):
        if acc == S['now']:
            return k - 1 if k else None
        acc += ord(ch) - 96
    return len(S['s']) - 1 if acc == S['now'] else None


def _line(S):
    if 'now' in S:
        return f"`now + now = {S['now']*2}`  vs  `total = {S['total']}`" + ('  → ==相等==' if S['now']*2 == S['total'] else '  → 不等')
    if 'total' in S:
        return f"总得分 `total = {S['total']}`"
    return ''


CONFIG = dict(
    num=3707, title='相等子字符串分数', difficulty='Easy', category='动态规划',
    author='yiduobo', technique='字符转分数 · 前缀和等于总和一半',
    tags=['灵神题单', '动态规划', '难度分 1262'],
    code='''
class Solution(object):
    def scoreBalance(self, s):
        
        total = 0
        for c in s:
            total += ord(c) - 96
        
        now = 0
        for c in s:
            now += ord(c) - 96
            if now + now == total:
                return True
        
        return False
''',
    call='Solution().scoreBalance("bace")',
    expect=False,
    views=[
        dict(type='text', fn=_line, size=30),
        dict(type='string', var='s', label='s', h=300,
             color=lambda S, i, v: 'green' if _pos(S) is not None and i <= _pos(S) else None),
    ],
    watch=[('total', 'total', 'purple'), ('now', 'now', 'blue'), ('c', 'c', 'yellow')],
    captions={
        'total += ': '字符 `{c}` 的得分是 `ord(c) - 96 = {ord(c) - 96}`，累加：`total = {B.total} + {ord(c) - 96} = {total}`',
        'now += ': '前缀和再来一遍：加上 `{c}` 的得分 `{ord(c) - 96}`，`now = {B.now} + {ord(c) - 96} = {now}`',
        'if now': '前缀和 `now = {now}`，两倍 `{now + now}`，总和 `{total}`：{"==恰好是总和的一半，可以切==" if now + now == total else "不等，继续往后看"}',
        'return True': '找到前缀和等于总和一半的位置 → 返回 True',
        'return False': '所有前缀都试过，没有恰好等于总和一半的 → 返回 ==False==',
    },
    cards=dict(
        one_liner='先把字母变成分数，再找「前缀和 = 总和一半」',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字母得分 `a=1 … z=26`，把 `s` 切成两个非空子串，使得分相等',
                 '能切返回 `True`，否则 `False`',
                 '示例：`"bace"` 总分 `2+1+3+5 = 11` → `False`'],
        quote='题目实际上就是给出一个数组，问是否存在某个前缀，其和恰好等于数组总和的一半。',
        quote_src='—— yiduobo 题解',
        idea=['每个字符的得分就是 `ord(c) - 96`，字符串变成一个正整数数组',
              '先一趟遍历求总和 `total`，再一趟遍历累加前缀和 `now`',
              '判断条件写成 `now + now == total`，避免除以 2 的小数问题'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '`ord(c) - 96` 因为 `ord("a") = 97`，所以 `a` 得 1',
                 '总和为奇数时一定不可能切开，前缀和永远凑不出一半',
                 '得分都是正数，所以最后一个前缀（整串）不会误判'],
    ),
)
