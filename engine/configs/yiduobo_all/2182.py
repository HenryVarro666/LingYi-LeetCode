def _cnt(S):
    return {chr(97 + i): c for i, c in enumerate(S['cnt_list']) if c}


CONFIG = dict(
    num=2182, title='构造限制重复的字符串', difficulty='Medium', category='贪心与思维',
    author='yiduobo', technique='主力字符 now + 间隔字符 next',
    tags=['灵神题单', '贪心与思维', '难度分 1680'],
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
    call='Solution().repeatLimitedString("zzzzyyx", 2)',
    expect="zzyzzyx",
    views=[
        dict(type='text', fn=lambda S: (f"`now = {chr(97 + S['now'])}`（主力），`next = {chr(97 + S['next']) if S['next'] >= 0 else '无'}`（间隔）；`res = {S['res']}`" if 'res' in S and 'next' in S else '找出最大的主力字符 now 和次大的间隔字符 next'), size=26),
        dict(type='map', var=_cnt, label='cnt_list（剩余个数）', h=240),
    ],
    watch=[('now', "chr(97+now) if now >= 0 else '无'", 'pink'), ('next', "chr(97+next) if next >= 0 else '无'", 'blue'), ('res', 'res', 'green')],
    captions={
        'cnt_list = [0] * 26': '`cnt_list` 统计每种字符的出现次数',
        'now = 25': '先从 `z` 开始，往小找第一个还有剩余的字符作主力 `now`',
        'while cnt_list[now] == 0': '`now` 指向最大的还有剩余的字符：`{chr(97 + now)}`',
        'next = now - 1': '间隔字符 `next` 从 `now` 前一个字母开始找',
        'while next >= 0 and cnt_list[next] == 0': lambda S, B, r: (f"`next` 对应的字母已用完，继续往小找" if (S.next >= 0 and S.cnt_list[S.next] == 0) else (f'没有可用的间隔字符了：`next = {S.next}`' if S.next < 0 else f"间隔字符 `next = {chr(97 + S.next)}`，还剩 `{S.cnt_list[S.next]}` 个")),
        'res = \'\'': '`res` 用来拼答案',
        'while now >= 0': lambda S, B, r: (f"主力 `{chr(97 + S.now)}` 还有 `{S.cnt_list[S.now]}` 个，继续构造" if S.now >= 0 else '主力字符也没有了，构造结束'),
        'if cnt_list[now] > repeatLimit': lambda S, B, r: (f"`{S.cnt_list[S.now]} > {S.repeatLimit}`：主力 `{chr(97 + S.now)}` 一次放不完 → ==放 {S.repeatLimit} 个，再插一个间隔字符==" if S.cnt_list[S.now] > S.repeatLimit else f"`{S.cnt_list[S.now]} <= {S.repeatLimit}`：主力 `{chr(97 + S.now)}` 一次能放完"),
        'res += chr(now + 97) * repeatLimit': '连放 `{repeatLimit}` 个 `{chr(now + 97)}` → `{res}`',
        'cnt_list[now] -= repeatLimit': '`{chr(now + 97)}` 还剩 `{cnt_list[now]}` 个',
        'if next < 0': lambda S, B, r: ('`next < 0`：没有间隔字符，主力剩下的放不了 → ==break==' if S.next < 0 else '`next >= 0`：还有间隔字符可用'),
        'res += chr(next + 97)': '插入间隔字符 `{chr(next + 97)}` → `{res}`',
        'cnt_list[next] -= 1': '`{chr(next + 97)}` 还剩 `{cnt_list[next]}` 个',
        'res += chr(now + 97) * cnt_list[now]': '主力一次放完：全部 `{cnt_list[now]}` 个也不超限 → `{res}`',
        'cnt_list[now] = 0': '主力 `{chr(97 + B.now)}` 用完了',
        'now = next': '==主力用完，原来的间隔字符升为新主力==：`now` → `{chr(now + 97) if now >= 0 else "无"}`',
        'next -= 1': '`next` 往小一格 → {next}',
        'return res': '构造结果 =={ret}==',
    },
    cards=dict(
        one_liner='最大的字符当主力，放满限制就插一个次大的字符隔开',
        complexity='时间 `O(n + 26)`，空间 `O(26)`',
        problem=['字符串 `s`，任何字母连续出现不能超过 `repeatLimit` 次',
                 '不必用完所有字符，求字典序最大的结果',
                 '示例：`s = "cczazcc", repeatLimit = 3` → `"zzcccac"`；本视频：`"zzzzyyx"`，限制 2'],
        quote='按照repeatLimit个now、1个next、再repeatLimit个now、再1个next的顺序来构造答案，直到now或者next用完。',
        quote_src='—— yiduobo 题解原文',
        idea=['`now` 是剩余字符中最大的，`next` 是次大的',
              '连放 `repeatLimit` 个 `now`，插 1 个 `next`，重复',
              '`now` 用完：`next` 升为新 `now`；`next` 用完：只换 `next`'],
        summary=['时间 `O(n + 26)`，空间 `O(26)`',
                 '原文为 Python 2 写法，只删去了 `:type` 文档字符串（本题无需改动其它）',
                 '易错点：没有 `next` 时必须停止，主力剩下的不能硬放',
                 '用了变量名 `next`，会遮住内置函数 `next`，但在这里没有影响'],
    ),
)
