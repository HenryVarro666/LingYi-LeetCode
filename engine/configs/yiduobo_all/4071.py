CONFIG = dict(
    num=4071, title='拨号的最少旋转次数II', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='一趟遍历 · 反转后缀只改一步',
    code='''
class Solution(object):
    def minRotations(self, n, s):
        
        pre = 0
        res = 0
        delta = 0
        last = int(s[-1])

        for c in s:
            c = int(c)
            diff = abs(c - pre)
            dis = min(diff, 10 - diff)
            res += dis

            diff_last = abs(last - pre)
            dis_last = min(diff_last, 10 - diff_last)
            if delta > dis_last - dis:
                delta = dis_last - dis
            
            pre = c
        
        return res + delta
''',
    call="Solution().minRotations(4, '1990')",
    expect=3,
    views=[
        dict(type='text', fn=lambda S: (f"在 `s[k]` 处反转后缀：这一步从 `{S['pre']}` 去 `{S['c']}`（{S['dis']} 步）改成去末位 `{S['last']}`（{S['dis_last']} 步），差 =={S['dis_last']-S['dis']}==" if 'dis_last' in S and 'c' in S else '')),
        dict(type='string', var='s', label='s（反转的是某个后缀 s[k:]）', h=170,
             color=lambda S, i, v: 'green' if i == len(S['s']) - 1 else None),
        dict(type='array', var=lambda S: list(range(10)), label='环形拨号盘 0–9', index=False,
             pointers={'pre': 'blue'}, h=200),
    ],
    watch=['pre', 'c', 'dis', 'dis_last', ('delta', 'delta', 'orange'), ('res', 'res', 'green')],
    captions={
        'pre = 0': '指针最初指向 `0`',
        'res = 0': '`res` 是不反转时的总旋转次数',
        'delta = 0': '`delta` 记反转最多能省多少（≤ 0），初始 0 = 不反转',
        'last = int': '反转后缀后，第一个到达的一定是末位 `last = {last}`',
        'for c in s': '把每个位置都当作后缀起点 `k` 试一遍',
        'c = int(c)': '候选起点 `s[k] = {c}`，前一个位置是 `{pre}`',
        'diff = abs(c - pre)': '不反转：`{pre} → {c}`，直走距离 `diff = {diff}`',
        'dis = min': '不反转这一步要 `{dis}` 次',
        'res += dis': '累加到总数 `res` = {res}',
        'diff_last = ': '反转：`{pre} → {last}`，直走距离 `{diff_last}`',
        'dis_last = ': '反转后这一步要 `{dis_last}` 次（后面整段的距离反转前后相同）',
        'if delta > dis_last - dis': lambda S, B, r: (f'差值 `{S.dis_last} − {S.dis} = {S.dis_last - S.dis}`，比 `delta = {S.delta}` 更小 → 更省，更新' if S.delta > S.dis_last - S.dis
                                                     else f'差值 `{S.dis_last - S.dis}` 不比 `delta = {S.delta}` 小 → 不更新'),
        'delta = dis_last - dis': '`delta` → =={delta}==：从这里反转可省 `{-delta}` 次',
        'pre = c': '指针前进到 `{pre}`',
        'return res + delta': '不反转 `{res}`，最多省 `{-delta}` → 答案 =={res + delta}==',
    },
    cards=dict(
        one_liner='反转后缀只改变一步：去 s[k] 还是去末位',
        complexity='时间 `O(n)`，空间 `O(1)`',
        problem=['规则同 4070：环形拨号盘，指针从 `0` 出发拨完 `s`',
                 '拨号前可至多一次，选 `s` 的任意后缀并反转',
                 '求最少旋转次数。本视频：`s = "1990"`'],
        quote='对于上面反转与不反转这两种情况，唯一的差别仅在于从s[k - 1]或者0到达的是s[k]还是s[n - 1]',
        quote_src='—— yiduobo 题解原文',
        idea=['后缀内部相邻数字的距离，正着走反着走一样',
              '所以只有进入后缀的那一步变了：`s[k-1]→s[k]` 变成 `s[k-1]→s[n-1]`',
              '枚举 `k` 取差值最小且小于 0 的，加到不反转的总数上'],
        summary=['时间 `O(n)`，空间 `O(1)`',
                 '易错点：`delta` 初值 0，表示可以不反转；k=0 时前一个位置是 0',
                 '参数 `n` 是 `s` 的长度，代码里没有用到',
                 '原文为 Python 2 风格（`class Solution(object)`），代码无需修改'],
    ),
)
