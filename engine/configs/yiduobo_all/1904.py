CONFIG = dict(
    num=1904, title='你完成的完整对局数', difficulty='Medium', category='数学算法',
    author='yiduobo', technique='换算成分钟 · 起点上取整终点下取整',
    tags=[],
    code='''
class Solution:
    def numberOfRounds(self, loginTime, logoutTime):

        login_hour, login_minute = loginTime.split(':')
        start = int(login_hour) * 60 + int(login_minute)
        logout_hour, logout_minute = logoutTime.split(':')
        end = int(logout_hour) * 60 + int(logout_minute)
        if start <= end:
            return self.calc(start, end)
        else:
            return self.calc(start, 1440) + self.calc(0, end)
    
    def calc(self, start, end):
        if start % 15 != 0:
            start = start // 15 * 15 + 15
        end = end // 15 * 15
        return max(0, (end - start) // 15)
''',
    call='Solution().numberOfRounds("23:20", "00:50")',
    expect=5,
    views=[
        dict(type='text', size=34, h=110, fn=lambda S: (
            f"`login = {S['loginTime']}`，`logout = {S['logoutTime']}`" + (
                f"　→　分钟：start = =={S['start']}==" if 'start' in S else '') + (
                f"，end = =={S['end']}==" if 'end' in S else ''))),
        dict(type='text', size=30, h=110, fn=lambda S: (
            f"本段 `[{S['start']}, {S['end']}]`：起点上取整，终点下取整" if S['_line'] >= 14 else
            '每个整刻钟（0、15、30、45 分）才开一局，只数完整落在区间里的')),
        dict(type='text', size=30, h=110, fn=lambda S: (
            f"本段完整对局数 = `({S['end']} − {S['start']}) // 15` = =={max(0, (S['end'] - S['start']) // 15)}==" if S['_line'] >= 17 else '')),
    ],
    watch=[('start', 'start', 'blue'), ('end', 'end', 'pink')],
    captions={
        'login_hour, login_minute': '把 `loginTime` 按冒号拆开：时 `{login_hour}`，分 `{login_minute}`',
        'start = int': '统一成分钟：`{login_hour} × 60 + {login_minute}` = ==start {start}==，终点同理',
        'logout_hour, logout_minute': '同样拆开 `logoutTime`：时 `{logout_hour}`，分 `{logout_minute}`',
        'end = int': '`{logout_hour} × 60 + {logout_minute}` = ==end {end}==',
        'if start <= end': lambda S, B, ret: (
            f'`start = {S.start} <= end = {S.end}`：同一天内' if S.start <= S.end
            else f'`start = {S.start} > end = {S.end}`：==跨午夜==，要拆成两段'),
        'return self.calc(start, end)': '同一天，直接算 `[start, end]` 内的完整对局',
        'return self.calc(start, 1440)': '跨午夜：`[start, 24:00]` 加 `[0, end]`，两段各算各的再相加',
        'if start % 15 != 0': lambda S, B, ret: (
            f'`start % 15 = {S.start % 15}` ≠ 0：起点在某局开始之后，这一局不完整' if S.start % 15 != 0
            else f'`start % 15 = 0`：起点正好踩在整刻钟，不用调整'),
        'start = start // 15': '起点==向上取整==到下一个整刻钟：`start = {start}`',
        'end = end // 15': '终点==向下取整==到上一个整刻钟：`end = {end}`',
        'return max(0': lambda S, B, ret: (
            f'`(end − start) // 15 = ({S.end} − {S.start}) // 15 = {(S.end - S.start) // 15}`'
            + ('，==为负就取 0==（起终点在同一刻钟内）' if S.end < S.start else '') + f'，本段 =={ret}== 局'),
    },
    max_steps=60,
    cards=dict(
        one_liner='起点上取整、终点下取整，再除以 15；跨午夜拆两段',
        complexity='时间 `O(1)`，空间 `O(1)`',
        problem=['每个整刻钟（`HH:00/15/30/45`）开始一个 15 分钟的对局',
                 '只数你==完整参与==的对局；`finishTime` 早于 `startTime` 表示通宵',
                 '示例：`12:01 → 12:44` 得 `1`；`20:00 → 06:00` 得 `40`'],
        quote='起始时间应该除以15向上取整，而结束时间则应该除以15向下取整。……当出现起始时和结束时间在同一个十五分钟内，且两个时间都没有踩上整15分钟的点的话，此时的答案就应该为0，但是如果直接向上向下取整来算的话，会得到-1这样奇怪的答案。',
        quote_src='—— yiduobo 题解',
        idea=['先把 `HH:MM` 统一成分钟数，方便做整除',
              '起点 `start` 要找第一个整刻钟，终点 `end` 要找最后一个整刻钟',
              '跨午夜就拆成 `[start, 1440]` 和 `[0, end]` 两段分别算'],
        summary=['时间 `O(1)`，空间 `O(1)`',
                 '易错：取整后 `end < start` 会得到 -1，要用 `max(0, ...)`',
                 '原文为 Python 2 写法，`calc` 中的整数除法 `/` 已改为 `//`',
                 '跨午夜时 `end` 取 1440（24:00），不是 1439'],
    ),
)
