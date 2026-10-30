def _ch(S, k):
    return chr(97 + S[k]) if k in S and isinstance(S[k], int) and 0 <= S[k] < 26 else '无'


CONFIG = dict(
    num=2182, title='构造限制重复的字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='主力字符 + 间隔字符',
    tags=['灵神题单·贪心与思维', '难度分 1680'],
    code='''
class Solution(object):
    def repeatLimitedString(self, s, repeatLimit):
        
        cnt_list = [0] * 26
        for char in s:
            cnt_list[ord(char) - 97] += 1
        
        now = 25
        while cnt_list[now] == 0:
            now -= 1
        
        next = now - 1
        while next >= 0 and cnt_list[next] == 0:
            next -= 1

        res = ''
        while now >= 0:
            if cnt_list[now] > repeatLimit:
                res += chr(now + 97) * repeatLimit
                cnt_list[now] -= repeatLimit
                if next < 0:
                    break
                res += chr(next + 97)
                cnt_list[next] -= 1
                while next >= 0 and cnt_list[next] == 0:
                    next -= 1
            else:
                res += chr(now + 97) * cnt_list[now]
                cnt_list[now] = 0
                now = next
                next -= 1
                while next >= 0 and cnt_list[next] == 0:
                    next -= 1
        
        return res
''',
    call='Solution().repeatLimitedString("zzzzzyya", 2)',
    expect='zzyzzyza',
    views=[
        dict(type='text', size=28, fn=lambda S: (
            f"主力 `now = {_ch(S, 'now')}`　间隔 `next = {_ch(S, 'next')}`" if 'next' in S else '')),
        dict(type='map', var=lambda S: {chr(97 + i): c for i, c in enumerate(S['cnt_list']) if c} if 'cnt_list' in S else {},
             label='剩余字母个数 cnt_list', h=240),
        dict(type='string', var='res', label='res（已构造的答案）', cell=70, h=190,
             color=lambda S, i, v: 'green'),
    ],
    watch=[('now', 'now', 'blue'), ('next', 'next', 'pink'), ('repeatLimit', 'repeatLimit')],
    skip=['cnt_list = [0]', 'for char in s', 'cnt_list[ord', 'now -= 1', 'next -= 1',
          'while cnt_list[now] == 0', 'while next >= 0 and cnt_list[next] == 0'],
    captions={
        'now = 25': '先从 `z` 往前找：`now` 是剩余字符里==字典序最大==的主力字符',
        'now -= 1': '`cnt_list[{now + 1}] == 0` 这个字母没有 → `now` 左移到 {now}',
        'while cnt_list[now] == 0': lambda S, B, r: (f"`{chr(97 + S.now)}` 还有 `{S.cnt_list[S.now]}` 个 → 它就是主力 `now`" if S.cnt_list[S.now]
                                                      else f"`{chr(97 + S.now)}` 个数为 0，继续往前找"),
        'next = now - 1': '间隔字符 `next` 从 `now - 1` 往前找：字典序第二大的存在字母',
        'while next >= 0 and cnt_list[next] == 0': lambda S, B, r: (
            f"`{chr(97 + S.next)}` 还有 `{S.cnt_list[S.next]}` 个 → 它是间隔 `next`" if S.next >= 0 and S.cnt_list[S.next]
            else ('没有可用的间隔字符了，`next = -1`' if S.next < 0 else f"`{chr(97 + S.next)}` 个数为 0，继续往前")),
        'next -= 1': '`next` 左移到 {next}',
        "res = ''": '找完了：主力 `now = {chr(now + 97)}`（字典序最大），间隔 `next = {chr(next + 97)}`（次大）。`res` 保存答案',
        'while now >= 0': lambda S, B, r: (
            f"主力 `{chr(97 + S.now)}`（剩 {S.cnt_list[S.now]} 个），间隔 `{chr(97 + S.next) if S.next >= 0 else '无'}`，继续构造" if S.now >= 0
            else '`now < 0`：字符用完了，结束'),
        'if cnt_list[now] > repeatLimit': lambda S, B, r: (
            f"`{chr(97 + S.now)}` 剩 `{S.cnt_list[S.now]}` 个 > 限制 `{S.repeatLimit}`：一次放不完，要靠间隔字符隔开" if S.cnt_list[S.now] > S.repeatLimit
            else f"`{chr(97 + S.now)}` 剩 `{S.cnt_list[S.now]}` 个 ≤ 限制 `{S.repeatLimit}`：可以一次放完"),
        '* repeatLimit': '先放 `repeatLimit = {repeatLimit}` 个 `{chr(now + 97)}`：`res = {res}`',
        'cnt_list[now] -= repeatLimit': '`{chr(now + 97)}` 还剩 `{cnt_list[now]}` 个',
        'if next < 0': lambda S, B, r: ('`next < 0`：没有间隔字符，剩下的主力不能再放，==直接结束==' if S.next < 0
                                        else f"间隔字符 `{chr(97 + S.next)}` 还有，可以隔开"),
        'break': '放不了了，退出循环',
        'res += chr(next + 97)': '放 1 个间隔 `{chr(next + 97)}`，打断主力连续：`res = {res}`',
        'cnt_list[next] -= 1': lambda S, B, r: (
            f"间隔 `{chr(S.next + 97)}` 还剩 `{S.cnt_list[S.next]}` 个" if S.cnt_list[S.next]
            else f"间隔 `{chr(S.next + 97)}` 用完了 → 接着往前找新的 `next`"),
        '* cnt_list[now]': '主力 `{chr(now + 97)}` 剩下的全部放上：`res = {res}`',
        'cnt_list[now] = 0': '`{chr(now + 97)}` 用完了',
        'now = next': '主力用完，间隔字符成为新的主力：`now` = `{chr(now + 97) if now >= 0 else "无"}`',
        'return res': '返回 `{res}`',
    },
    cards=dict(
        one_liner='大字母尽量连放 limit 个，用次大字母隔开，再接着放',
        complexity='时间 `O(n + 26)`，空间 `O(26)`',
        problem=['用 `s` 的字符重排成新串，任何字母==连续出现不超过 `repeatLimit` 次==',
                 '可以不用完所有字符，求字典序最大的结果',
                 '示例：`s = "cczazcc"`，`repeatLimit = 3` → `"zzcccac"`',
                 '本视频：`"zzzzzyya"`，`repeatLimit = 2` → `"zzyzzyza"`'],
        quote='只需在重复限制内尽量将字典序较大的字符排到前面就行了。……作为主力字符，使用now来表示。同时还需要找出字典序第二大的，作为间隔字符，使用next来表示。',
        quote_src='—— yiduobo 题解原文',
        idea=['统计每个字母个数；`now` = 最大的存在字母，`next` = 第二大的',
              '按「limit 个 now，1 个 next，再 limit 个 now…」的顺序构造',
              'now 用完 → next 变成新的 now；next 用完 → 只需找新的 next；找不到 next 就结束'],
        result='`zz` `y` `zz` `y` `z` `a` → `"zzyzzyza"` ✓',
        summary=['时间 `O(n + 26)`，空间 `O(26)`',
                 '`now` 剩余超过限制时，必须先确认 `next` 存在；没有就 `break`，多余的 now 直接丢掉',
                 '`now` 用完时，新的 `now = next`，`next` 要从它的前一个字母重新往前找',
                 '原文变量名 `next` 覆盖了内置函数名，但本题没用到内置 next，不影响运行'],
    ),
)
