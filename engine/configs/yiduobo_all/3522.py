INS = ["jump", "add", "add", "jump", "add", "jump"]
VAL = [2, 1, 3, 1, -2, -3]
CONFIG = dict(
    num=3522, title='执行指令后的得分', difficulty='Medium', category='模拟',
    author='yiduobo', technique='模拟 · 集合记录已执行下标',
    tags=[],
    code='''
class Solution(object):
    def calculateScore(self, instructions, values):
        
        vis = set()
        res = 0
        now = 0
        while 0 <= now < len(instructions) and now not in vis:
            vis.add(now)
            if instructions[now] == 'jump':
                now += values[now]
            else:
                res += values[now]
                now += 1
        
        return res
''',
    call='Solution().calculateScore(%r, %r)' % (INS, VAL),
    expect=1,
    views=[
        dict(type='array', var='instructions', pointers={'now': 'blue'}, h=200, label='instructions', cell=110,
             color=lambda S, i, v: 'green' if 'vis' in S and i in S['vis'] else None),
        dict(type='array', var='values', pointers={'now': 'blue'}, h=200, label='values', cell=110),
        dict(type='set', var='vis', h=170, fmt=lambda x: str(x)),
        dict(type='text', size=30, fn=lambda S: f"`now = {S['now']}`，`res` = =={S['res']}==" if 'now' in S and 'res' in S else ''),
    ],
    watch=[('now', 'now', 'blue'), ('res', 'res', 'green')],
    captions={
        'vis = set()': '`vis` 集合：记录已经执行过的指令下标',
        'res = 0': '`res` 累计得分',
        'now = 0': '`now` 是当前指令下标，从 0 开始',
        'while 0 <= now': lambda S, B, r: (f'`now = {S.now}`：{"越界，停止" if not (0 <= S.now < len(S.instructions)) else ("已在 vis 中，之前执行过 → 停止" if S.now in S.vis else "没越界、没执行过 → 继续")}'),
        'vis.add(now)': '把 `{now}` 记入 `vis`：这条指令执行过了',
        "== 'jump'": '`instructions[{now}]` = `{instructions[now]}`：{"是 jump，把 values 累加到 now" if instructions[now] == "jump" else "是 add，把 values 累加到 res"}',
        'now += values[now]': 'jump：`now` 加上 `values[{B.now}]` = {values[B.now]} → =={now}==，得分不变',
        'res += values[now]': 'add：`res` 加上 `values[{now}]` = {values[now]} → =={res}==',
        'now += 1': 'add 之后 `now` 移到下一条：{now}',
        'return res': '最终得分 =={ret}==',
    },
    cards=dict(
        one_liner='直接模拟，用集合记下执行过的下标',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['从下标 0 开始，得分为 0',
                 '`add`：得分加 `values[index]`，下标加 1；`jump`：下标加 `values[index]`',
                 '越界或来到执行过的指令就停止，问最终得分',
                 '本视频：`[jump,add,add,jump,add,jump]`，`[2,1,3,1,-2,-3]` → `1`'],
        quote='题目的描述很清晰，直接按照描述执行模拟就行了。另外根据停止条件，需要使用一个集合记录已经处理过的指令下标。',
        quote_src='—— yiduobo 题解原文',
        idea=['初始化 `vis` 为空集合，`now` 和 `res` 为 0',
              '是 `jump` 就把 `values[now]` 累积到 `now`，否则累加到 `res` 且 `now += 1`',
              '直到 `now` 越界或已在 `vis` 中为止'],
        summary=['时间 `O(n)`，空间 `O(n)`（集合）',
                 '循环条件先判越界再判 `now not in vis`',
                 '`jump` 不改得分，`add` 才改；别把两个分支写反',
                 '原文为 Python 2 风格，仅有类型说明注释，代码无需修改'],
    ),
)
