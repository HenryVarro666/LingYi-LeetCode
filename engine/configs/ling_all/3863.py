def _col(S, i, v):
    mn, mx = S.get('mn'), S.get('mx')
    if mn is None:
        return None
    if i == 0 and v == mx:
        return 'pink'
    if i == len(S['s']) - 1 and v == mn:
        return 'cyan'
    if v == mn:
        return 'green'
    if v == mx:
        return 'orange'
    return None


def _txt(S):
    if 'mn' not in S:
        return '先看 s 是否已经有序、长度是否为 2'
    s = S['s']
    return f"最小值 ==`{S['mn']}`==（下标 {s.index(S['mn'])}），最大值 ==`{S['mx']}`==（下标 {s.rindex(S['mx'])}）；首 `{s[0]}`，尾 `{s[-1]}`"


CONFIG = dict(
    num=3863, title='将一个字符串排序的最小操作次数', difficulty='Medium', category='贪心与思维',
    author='灵茶山艾府', technique='分类讨论 · 看首尾与最值',
    tags=['灵神题单', '思维题', '难度分 1860'],
    code='''
class Solution:
    def minOperations(self, s: str) -> int:
        # s 已经是升序
        if all(x <= y for x, y in pairwise(s)):
            return 0

        # 长为 2，无法排序
        if len(s) == 2:
            return -1

        mn = min(s)
        mx = max(s)

        # 如果 s[0] 是最小值，排序 [1,n-1] 即可
        # 如果 s[n-1] 是最大值，排序 [0,n-2] 即可
        if s[0] == mn or s[-1] == mx:
            return 1

        # 如果 [1,n-2] 中有最小值，那么先排序 [0,n-2]，把最小值排在最前面，然后排序 [1,n-1] 即可
        # 如果 [1,n-2] 中有最大值，那么先排序 [1,n-1]，把最大值排在最后面，然后排序 [0,n-2] 即可
        if any(ch == mn or ch == mx for ch in s[1:-1]):
            return 2

        # 现在只剩下一种情况：s[0] 是最大值，s[n-1] 是最小值，且 [1,n-2] 不含最小值和最大值
        # 先排序 [0,n-2]，把最大值排到 n-2
        # 然后排序 [1,n-1]，把最大值排在最后面，且最小值排在 1
        # 最后排序 [0,n-2]，把最小值排在最前面
        return 3
''',
    call='Solution().minOperations("dbca")',
    expect=3,
    views=[
        dict(type='text', fn=_txt, h=70),
        dict(type='string', var='s', label='s（绿 = 最小值，橙 = 最大值，粉 = 首位是最大值，青 = 末位是最小值）', cell=110, color=_col, h=260),
    ],
    watch=[('mn', 'mn', 'green'), ('mx', 'mx', 'orange')],
    captions={
        'if all(': '`s = "{s}"`：逐对检查是否已是升序 → ==有逆序对，不是升序==，继续',
        'if len(s) == 2': '`len(s) = {len(s)}`：不是 2。长为 2 时不能排整个串，只能 -1',
        'mn = min(s)': '最小值 `mn = {mn}`：想让它排到最前面',
        'mx = max(s)': '最大值 `mx = {mx}`：想让它排到最后面',
        'if s[0] == mn or s[-1] == mx': '`s[0]={s[0]}` 是最小值？`{s[0] == mn}`；`s[-1]={s[-1]}` 是最大值？`{s[-1] == mx}` → ==首尾都没归位==，一次排不好',
        'if any(': '中间 `{s[1:-1]}` 里有最小或最大值吗？==没有== → 一次操作也没法把最值挪出首尾',
        'return 3': '只剩最坏情形：首位是最大、末位是最小、中间无最值 → 要排三次，答案 ==3==',
    },
    cards=dict(
        one_liner='不能排整个串，答案只可能是 0、1、2、3 或 -1',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['每次选一个==不是整个字符串==的子串，把它按字母升序排好',
                 '求让 `s` 整体升序的最少操作次数，做不到返回 `-1`',
                 '示例：`"dog"` → `1`，`"card"` → `2`，`"gf"` → `-1`；本视频：`"dbca"` → `3`'],
        quote='子串不能同时包含 s 的第一个字母和最后一个字母。这意味着，如果第一个字母或者最后一个字母已经在正确的位置上，那么至多操作 1 次。否则，至少操作 2 次。',
        quote_src='—— 灵茶山艾府题解',
        idea=['抓住限制：子串碰不到「首尾同时」，所以先看首尾有没有归位',
              '按顺序分五种情况：有序 0 次；长 2 为 -1；首最小或尾最大 1 次',
              '中间有最值 2 次；否则首最大、尾最小、中间没有最值，要 3 次'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '判断顺序不能乱：先有序，再长为 2，再 1 次、2 次、3 次',
                 '`n = 2` 且已有序时返回 0，不是 -1',
                 '最值可能重复，所以用「等于 mn / mx」判断，而不是找下标',
                 '同类题：分类讨论 + 找必要条件的思维题'],
    ),
)
