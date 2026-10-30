def _pos(S):
    """已累加到第几个字符（用 left 反推，字母得分都是正数，所以唯一）"""
    if 'left' not in S:
        return None
    acc = 0
    for k, ch in enumerate(S['s']):
        if acc == S['left']:
            return k - 1 if k else None
        acc += ord(ch) & 31
    return len(S['s']) - 1 if acc == S['left'] else None


def _scores(S):
    return [ord(c) & 31 for c in S['s']]


def _line(S):
    if 'left' in S:
        t = S['total']
        return f"`left * 2 = {S['left']*2}`，`total = {t}`" + ('  → ==相等==' if S['left']*2 == t else '')
    if 'total' in S:
        return f"总得分 `total = {S['total']}`"
    return ''


CONFIG = dict(
    num=3707, title='相等子字符串分数', difficulty='Easy', category='动态规划',
    author='灵茶山艾府', technique='前缀和 · left×2 = total',
    tags=['灵神题单', '动态规划', '难度分 1262'],
    code='''
class Solution:
    def scoreBalance(self, s: str) -> bool:
        total = sum(ord(b) & 31 for b in s)

        left = 0
        for b in s:  # 字母位置是正数，可以遍历到 s 末尾（末尾一定不满足要求）
            left += ord(b) & 31
            if left * 2 == total:
                return True
        return False
''',
    call='Solution().scoreBalance("bcabd")',
    expect=True,
    views=[
        dict(type='text', fn=_line, size=30),
        dict(type='string', var='s', label='s', h=170,
                          color=lambda S, i, v: 'green' if _pos(S) is not None and i <= _pos(S) else None),
        dict(type='array', var=lambda S: _scores(S), label='每个字母的得分 ord(c) & 31', h=170),
    ],
    watch=[('total', 'total', 'purple'), ('left', 'left', 'blue'), ('b', 'b', 'yellow')],
    captions={
        'total = sum': '先扫一遍：所有字母得分之和 `total = {total}`，各字母得分是 `ord(b) & 31`（a=1 … z=26）',
        'left += ': '加入字符 `{b}`（得分 `{ord(b) & 31}`），前缀得分 `left = {B.left} + {ord(b) & 31} = {left}`',
        'if left': '另一半得分是 `total - left = {total - left}`；要相等即 `left * 2 == total`：`{left*2}` vs `{total}` → {"==成立==" if left*2==total else "不成立"}',
        'return True': '找到分割点：左右两半得分相等 → 返回 ==True==',
        'return False': '整个字符串都试过没有相等 → 返回 False',
    },
    cards=dict(
        one_liner='算出总分，枚举前缀，看 前缀×2 是否等于总分',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['字母得分：`a=1, b=2, …, z=26`，字符串得分 = 各字符得分之和',
                 '能否切成两个非空子串，得分相等？返回 `True / False`',
                 '示例：`"adcb"` → `True`（`ad` = 5，`cb` = 5）'],
        quote='题目要求 left = total - left，即 ==left·2 = total==。如果遍历过程中符合上式，返回 true。',
        quote_src='—— 灵茶山艾府题解',
        idea=['第一遍求总分 `total`，第二遍边走边累加前缀 `left`',
              '右半得分 = `total - left`，所以不用单独算右边，只比 `left * 2 == total`',
              '字母得分是正数，可以遍历到末尾：末尾 `left = total`，`2·total ≠ total`，一定不会误判'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '字母位置用 `ord(c) & 31` 比 `ord(c) - ord("a") + 1` 更短',
                 '易错点：两半都要非空；这里靠“得分为正”自动排除了整串',
                 '同类：前后缀分解专题（前缀和 + 总和相减得后缀）'],
    ),
)
