def _grp(S):
    g = S.get('groups')
    if g is None or 'k' not in S:
        return ''
    best = ''.join(g[S['k']]) if S['k'] in g else ''
    return f"当前最优组：频率 `k = {S['k']}`，字母 =={best or '无'}=="


CONFIG = dict(
    num=3692, title='众数频率字符', difficulty='Easy', category='常用数据结构',
    author='灵茶山艾府', technique='哈希表套列表（反向映射）', tags=[],
    code='''
class Solution:
    def majorityFrequencyGroup(self, s: str) -> str:
        cnt = Counter(s)
        groups = defaultdict(list)
        k = 0
        for ch, cnt in cnt.items():
            groups[cnt].append(ch)
            if (len(groups[cnt]), cnt) > (len(groups[k]), k):
                k = cnt
        return ''.join(groups[k])
''',
    call="Solution().majorityFrequencyGroup('aaabbbccdddde')",
    expect='ab',
    views=[
        dict(type='string', var='s', label='s', cell=60, h=130),
        dict(type='map', var='groups', label='groups（出现次数 → 字母列表）',
             fmt=lambda k, v: f"{k} 次: {','.join(v) if v else '空'}", h=300, font=32),
        dict(type='text', h=70, size=30, fn=_grp),
    ],
    watch=[('ch', 'ch', 'blue'), ('cnt', 'cnt', 'cyan'), ('k', 'k', 'green')],
    captions={
        'cnt = Counter': '统计每个字母出现次数：`{dict(cnt)}`',
        'groups = defaultdict': '`groups`：把「出现次数」映射到「字母列表」，相当于把 cnt 的 value 反过来当 key',
        'k = 0': '`k` 记录当前最优组的出现次数，先设为 0',
        'for ch, cnt': '取一个字母 `{ch}`，它出现了 `{cnt}` 次（这里的 cnt 变量被复用为次数）',
        'groups[cnt].append': '字母 `{ch}` 归入出现 `{cnt}` 次的组：`groups[{cnt}] = {groups[cnt]}`',
        'if (len(groups': lambda S, B, r: (
            f"比较 `(组大小, 次数)`：`({len(S.groups[S.cnt])}, {S.cnt})` vs `({len(S.groups[S.k])}, {S.k})` → "
            + ('==更大==，更新最优组' if (len(S.groups[S.cnt]), S.cnt) > (len(S.groups[S.k]), S.k) else '不更大，保持')),
        'k = cnt': '最优组换成出现 `{k}` 次的组：人数更多，或人数并列但次数更大',
        'return': '答案 = 最优组的字母拼起来：`{ret!r}`',
    },
    cards=dict(
        one_liner='把「字母到次数」反过来，按次数分组，取人数最多的组',
        complexity='时间 `O(n)`，空间 `O(min(n, |Σ|))`',
        problem=['按出现次数 `k` 给字母分组，选字母数最多的组',
                 '人数并列时，取出现次数 `k` 更大的组，返回组内所有字母',
                 '示例：`"aaabbbccdddde"` → `"ab"`'],
        quote='遍历 cnt，把出现次数相同的字母，分到同一组，这可以用一个哈希表套列表实现。这一步相当于反向映射，把 cnt 的 value 映射到 key 上。',
        quote_src='—— 灵茶山艾府题解',
        idea=['先数每个字母出现几次，再按次数装进 `groups`',
              '边装边比较 `(组大小, 次数)` 这个元组，字典序比较正好满足「先比人数、再比次数」',
              '遍历结束后 `k` 就是答案组，不用再扫一遍'],
        summary=['时间 `O(n)`，空间 `O(|Σ|)`，|Σ| = 26',
                 '易错：元组比较一次搞定并列规则，不要只比组大小',
                 '`for ch, cnt in cnt.items()` 复用了 cnt 变量名：迭代器已创建，所以能正常运行',
                 '`groups[k]` 在 k = 0 时会建出一个空组，不影响结果'],
    ),
)
