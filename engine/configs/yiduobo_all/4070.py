CONFIG = dict(
    num=4070, title='拨号的最少旋转次数I', difficulty='Easy', category='模拟',
    author='yiduobo', technique='一趟遍历 · 环形取近',
    code='''
class Solution(object):
    def minRotations(self, s):
        
        pre = 0
        res = 0
        for c in s:
            c = int(c)
            diff = abs(pre - c)
            res += min(diff, 10 - diff)
            pre = c
        
        return res
''',
    call="Solution().minRotations('2908')",
    expect=8,
    views=[
        dict(type='text', fn=lambda S: (f"指针 `{S['pre']}` → `{S['c']}`：直走 {abs(S['pre']-S['c'])} 步，绕回 {10-abs(S['pre']-S['c'])} 步" if 'c' in S and isinstance(S['c'], int) else '')),
        dict(type='array', var=lambda S: list(range(10)), label='环形拨号盘 0–9（9 与 0 相邻）', index=False,
             pointers={'pre': 'blue', 'c': 'pink'},
             color=lambda S, i, v: 'blue' if i == S.get('pre') else None, h=220),
        dict(type='string', var='s', label='要拨的号码 s', h=170),
    ],
    watch=['pre', 'c', 'diff', ('res', 'res', 'green')],
    captions={
        'pre = 0': '指针最初指向 `0`',
        'res = 0': '`res` 累计旋转次数',
        'for c in s': '依次拨号码里的每个数字',
        'c = int(c)': '目标数字 `c = {c}`',
        'diff = ': '`diff = |{pre} − {c}|` = {diff}：不绕圈要转的步数',
        'res += min': '顺逆两个方向取较小：`min({diff}, 10 − {diff}) = {min(diff, 10-diff)}` → `res` = =={res}==',
        'pre = c': '指针停在 `{pre}`，下一个数字从这里出发',
        'return res': '一共最少旋转 `{res}` 次',
    },
    cards=dict(
        one_liner='每次移动取顺时针和逆时针中较短的那条',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['拨号盘是 0–9 的环，`9` 和 `0` 相邻，指针从 `0` 出发',
                 '每次转一格，可顺可逆；依次拨出 `s` 的每个数字',
                 '求最少旋转次数。本视频：`s = "2908"`'],
        quote='对于从pre移动到c的一次移动，记diff = abs(c - pre)，那么这次移动的最少移动次数就是min(10 - diff, diff)',
        quote_src='—— yiduobo 题解原文',
        idea=['`diff` 是不跨 9→0 缝隙直接走的距离',
              '反方向绕一圈是 `10 - diff`',
              '逐个数字累加较小者即可'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：起点是 `0` 不是 `s[0]`；别忘了取 `10 - diff`',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需修改',
                 '进阶见 4071：可反转一个后缀'],
    ),
)
