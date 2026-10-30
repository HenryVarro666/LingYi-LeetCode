CONFIG = dict(
    num=1678, title='设计Goal解析器', difficulty='Easy', category='字符串',
    author='yiduobo', technique='一趟扫描 · 按字符分三种情况',
    code='''
class Solution(object):
    def interpret(self, command):

        res = []
        now = 0
        n = len(command)
        while now < n:
            char = command[now]
            if char == 'G':
                res.append('G')
                now += 1
            elif command[now + 1] == ')':
                res.append('o')
                now += 2
            else:
                res.append('al')
                now += 4
        
        return ''.join(res)
''',
    call="Solution().interpret('G()(al)G')",
    expect='GoalG',
    views=[
        dict(type='string', var='command', pointers={'now': 'blue'}, h=200, label='command'),
        dict(type='array', var='res', h=200, label='res（已解析的片段）'),
        dict(type='text', h=90, fn=lambda S: ('' if 'now' not in S else f"当前下标 `{S['now']}`，已解析：=={''.join(S['res']) or '（空）'}==")),
    ],
    watch=[('now', 'now', 'blue'), 'char', ('res', "''.join(res)", 'green')],
    captions={
        'res = []': '`res` 用来收集解析出的片段，最后拼成答案',
        'now = 0': '`now` 是当前扫描的位置，从头开始',
        'n = len': '`n = {n}`',
        'while now < n': lambda S, B, r: (f'`now = {S.now} < n = {S.n}`，还有字符没处理' if S.now < S.n else f'`now = {S.now} == n`：扫描完了'),
        'char = command[now]': "当前字符 `char = '{char}'`",
        "if char == 'G'": lambda S, B, r: ("`char` 是 `G` → 原样加入答案" if S.char == 'G' else f"`char = '{S.char}'` 不是 G，必然是左括号 `(`，看下一个字符"),
        "res.append('G')": '加入 `G`：`res` = {res}',
        'now += 1': '`G` 只占 1 个字符 → `now` = {now}',
        "elif command[now + 1] == ')'": lambda S, B, r: (f"下一个是 `)`，说明是 `()` → 解析成 `o`" if S.command[S.now + 1] == ')' else f"下一个是 `{S.command[S.now + 1]}` 不是 `)`，说明是 `(al)`"),
        "res.append('o')": '`()` 解析为 `o`：`res` = {res}',
        'now += 2': '`()` 占 2 个字符，跳过 → `now` = {now}',
        "res.append('al')": '`(al)` 解析为 `al`：`res` = {res}',
        'now += 4': '`(al)` 占 4 个字符，跳过 → `now` = {now}',
        'return': "拼接 `res` 得到 `'{ret}'`",
    },
    cards=dict(
        one_liner='看当前字符就知道它是哪种片段，再跳过对应长度',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['`G` 解析为 `G`，`()` 解析为 `o`，`(al)` 解析为 `al`',
                 '把命令字符串按此规则翻译，拼成一个新字符串',
                 '示例：`"G()(al)"` → `"Goal"`；本视频：`"G()(al)G"` → `"GoalG"`'],
        quote='若不满足情况1，那么此时当前字符必然为左括号。若下一个字符为右括号，那么将o加入到答案中，然后跳过下一个字符。',
        quote_src='—— yiduobo 题解原文',
        idea=['从头一趟扫描：当前是 `G`，直接加入答案，走 1 步',
              '否则一定是 `(`：看下一个字符，`)` 就是 `o`，走 2 步',
              '再否则就是 `(al)`：加入 `al`，走 4 步'],
        summary=['时间 `O(n)`，空间 `O(n)`',
                 '只有三种片段，靠 `command[now + 1]` 一个字符就能区分 `()` 和 `(al)`',
                 '跳过的步长要写对：`()` 是 2，`(al)` 是 4',
                 '原文只有 `res` 列表加最后 `join`，避免字符串反复拼接'],
    ),
)
