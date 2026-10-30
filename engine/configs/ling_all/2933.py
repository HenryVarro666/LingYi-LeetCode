def _any(S, B, r):
    ok = any(S.a[i] - S.a[i - 2] < 60 for i in range(2, len(S.a)))
    head = f'三次在一小时内 ⇔ 排序后有 `a[i] - a[i-2] < 60`：`{S.name}` 的 `{S.a}` '
    return head + ('满足 → 高访问员工' if ok else '不满足（不足 3 次，或隔一位的时间差都 >= 60）')


CONFIG = dict(
    num=2933, title='高访问员工', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='哈希表分组 + 排序看 a[i]-a[i-2]', tags=[],
    code='''
class Solution:
    def findHighAccessEmployees(self, access_times: List[List[str]]) -> List[str]:
        name2times = defaultdict(list)
        for name, s in access_times:
            t = int(s[:2]) * 60 + int(s[2:])
            name2times[name].append(t)

        ans = []
        for name, a in name2times.items():
            a.sort()
            if any(a[i] - a[i - 2] < 60 for i in range(2, len(a))):
                ans.append(name)
        return ans
''',
    call='Solution().findHighAccessEmployees([["a","0549"],["b","0457"],["a","0532"],["a","0621"],["b","0540"]])',
    expect=['a'],
    views=[
        dict(type='map', var='name2times', fmt=lambda k, v: f'{v}', label='name2times：姓名 → 访问时间（分钟）', h=240),
        dict(type='text', size=38, h=110, fn=lambda S: (
            f"`{S['name']}` 排序后 `{S['a']}`" if 'a' in S and 'name' in S and S.get('_line', 0) >= 11 else
            (f"`{S['name']}` 的 `{S['s']}` → `{S['t']}` 分钟" if 't' in S and S.get('_line', 0) <= 7 else ''))),
        dict(type='array', var='ans', label='ans（高访问员工）', h=160),
    ],
    watch=['name', ('ans', 'ans', 'green')],
    captions={
        'name2times = defaultdict': '按员工姓名分组，每人一个访问时间列表',
        't = int(s[:2])': '`"{s}"` 转成分钟：`{s[:2]}×60 + {s[2:]}` = =={t}==',
        'name2times[name].append': '`{name}` 的时间列表加入 `{t}`：{name2times[name]}',
        'a.sort()': '`{name}` 的时间排序 → `{a}`',
        'if any(': _any,
        'ans.append': '`{name}` 加入答案：`ans = {ans}`',
        'return ans': '返回 `{ret}`',
    },
    cards=dict(
        one_liner='排序后，隔一个位置的两次访问相差不到 60 分钟，就是三次同小时',
        complexity='时间 `O(Ln + n log n)`，空间 `O(Ln)`',
        problem=['`access_times[i] = [姓名, 时间]`，时间是 4 位 24 小时制',
                 '同一小时内访问 ≥ 3 次的员工是高访问员工，间隔恰好 60 分钟不算',
                 '示例：`[["a","0549"],["b","0457"],["a","0532"],["a","0621"],["b","0540"]]` → `["a"]`'],
        quote='把名字相同的员工对应的访问时间（转成分钟数）分到同一组中。对于每一组的访问时间 a，排序后，判断是否有 a[i]-a[i-2] < 60。',
        quote_src='—— 灵茶山艾府题解',
        idea=['时间转分钟，相同姓名放一组并排序',
              '连续三次访问 `a[i-2], a[i-1], a[i]` 里最早和最晚相差最大',
              '只要 `a[i] - a[i-2] < 60`，这三次就在同一小时内'],
        summary=['时间 `O(Ln + n log n)`，空间 `O(Ln)`',
                 '易错：必须 `< 60`，恰好相差 60 分钟不算同一小时',
                 '同一天内的时间，不用考虑跨零点',
                 '返回顺序任意，本题按名字首次出现顺序'],
    ),
)
