def _s_color(S, k, v):
    if 'ids' in S:
        return 'green' if k in S['ids'] else None
    if 'mx' in S:
        return 'blue' if S['cnt'][v] == S['mx'] and k == S['last'][v] else None
    return None


def _top(S):
    if 'ids' in S:
        return f"出现 `{S['mx']}` 次的字母，取最后一次出现的下标，按下标排序：`{S['ids']}`"
    if 'mx' in S:
        return f"最大出现次数 `mx = {S['mx']}`：最后一轮剩下的就是这些字母"
    if 'cnt' in S:
        return '`last[c]`：字母最后一次出现的下标；`cnt[c]`：出现次数'
    if 'last' in S:
        return '`last[c]`：字母最后一次出现的下标（后面的覆盖前面的）'
    return '每一轮每种字母各删一个（最早的），最后一轮之前剩下什么？'


CONFIG = dict(
    num=3039, title='进行操作使字符串为空', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='最大频次 + 最后出现位置',
    tags=[],
    code='''
class Solution:
    def lastNonEmptyString(self, s: str) -> str:
        last = {c: i for i, c in enumerate(s)}
        cnt = Counter(s)
        mx = max(cnt.values())
        ids = sorted(last[ch] for ch, c in cnt.items() if c == mx)
        return ''.join(s[i] for i in ids)
''',
    call='Solution().lastNonEmptyString("aabcbbca")',
    expect='ba',
    views=[
        dict(type='text', fn=_top, size=26),
        dict(type='string', var='s', label='s（蓝 = 最大频次字母的最后一次出现，绿 = 答案）', cell=84, color=_s_color),
        dict(type='map', var='last', label='last：字母 → 最后出现的下标', h=170),
        dict(type='map', var='cnt', label='cnt：字母 → 出现次数', h=170),
    ],
    watch=[('mx', 'mx', 'green'), ('ids', 'ids', 'pink')],
    captions={
        'last = {': '遍历 s，同一个字母后出现的会覆盖前面的 → `last[c]` 就是它==最后一次==出现的下标：`{last}`',
        'cnt = Counter': '统计每个字母出现的次数：`{dict(cnt)}`',
        'mx = max': '每一轮每种字母最多删一个，所以出现次数最多的字母最晚删完：`mx = {mx}`',
        'ids = sorted': lambda S, B, ret: f"次数等于 `mx = {S.mx}` 的字母才会留到最后一轮；删除总是删最早的，留下的是==最后一次出现==的那个；按下标排序恢复原顺序：`ids = {S.ids}`",
        'return': '按下标取出字符拼起来，就是最后一次操作之前的字符串 =={ret!r}==',
    },
    cards=dict(
        one_liner='最后一轮剩下的，是出现次数最多的字母的最后一次出现',
        complexity='时间 `O(n + |Σ| log |Σ|)`，空间 `O(|Σ|)`',
        problem=['每轮依次从 `a` 到 `z`，删除 s 中该字母==最早==出现的一个',
                 '重复直到 s 为空，返回最后一次操作之前的 s',
                 '示例：`"aabcbbca"` → `"ba"`'],
        quote='最后一次操作时，剩下的字母互不相同。设字母的最大出现次数为 mx。由于删除是从左到右进行的，最后剩下的就是出现次数等于 mx 的靠右字母（相同字母取出现位置最右的）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['每轮每个字母只删一个，次数最多的字母要 `mx` 轮才删完',
              '倒数第二轮结束时每个剩下的字母只有 1 个，且次数 = `mx` 的才在里面',
              '从左往右删，剩下的必是最右的那个；用 `last` 记下标并排序'],
        result='`a`、`b` 都出现 3 次，最后位置 7 和 5 → 排序后 `"ba"` ✓',
        summary=['时间 `O(n + |Σ| log |Σ|)`，字符集只有 26，空间 `O(|Σ|)`',
                 '易错：要取每个字母==最后一次==出现的位置，不是第一次',
                 '多个字母并列最大频次时，按下标排序才能还原原来的顺序',
                 '不需要真的模拟删除，直接数学推出答案'],
    ),
)
