CONFIG = dict(
    num=649, title='Dota2 参议院', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='模拟 · 记录待 ban 人数',
    tags=['灵神核心路线', '灵神题单·常用数据结构'],
    code='''
class Solution(object):
    def predictPartyVictory(self, senate):

        q = []
        r = d = 0
        del_r = del_d = 0
        for char in senate:
            q.append(char)
            if char == 'R':
                r += 1
            else:
                d += 1
        
        while r > 0 and d > 0:
            tot = r + d
            r = d = 0
            for index in range(tot):
                if q[index] == 'R':
                    if del_r > 0:
                        del_r -= 1
                    else:
                        q[r + d] = q[index]
                        r += 1
                        del_d += 1
                else:
                    if del_d > 0:
                        del_d -= 1
                    else:
                        q[r + d] = q[index]
                        d += 1
                        del_r += 1

        if r > 0:
            return 'Radiant'
        else:
            return 'Dire'
''',
    call="Solution().predictPartyVictory('RDDRDR')",
    expect='Dire',
    views=[
        dict(type='array', var=lambda S: S['q'], pointers={'index': 'blue', 'r + d': 'pink'}, h=210, cell=70,
             label='队列 q（蓝 = 正在投票的人，粉 = 幸存者写回位置）',
             color=lambda S, i, v: ('red' if v == 'R' else 'cyan') if v in 'RD' else None),
        dict(type='text', h=70, fn=lambda S: (f"R 剩 =={S['r']}==，D 剩 =={S['d']}==；待 ban 的 R：`{S['del_r']}`，待 ban 的 D：`{S['del_d']}`" if 'del_r' in S else '')),
    ],
    watch=[('r', 'r', 'red'), ('d', 'd', 'cyan'), ('del_r', 'del_r', 'orange'), ('del_d', 'del_d', 'orange')],
    skip=['q.append(char)'],
    captions={
        5: '`r`、`d` 记两阵营人数',
        4: '`q` 存全部参议员',
        6: '`del_r`：R 阵营接下来要被 ban 的人数；`del_d` 同理',
        7: lambda S, B, ret: '先数一遍人数：`{}`'.format(S.char),
        9: lambda S, B, ret: '`{}` 是 `R` 阵营'.format(S.char) if S.char == 'R' else '`{}` 是 `D` 阵营'.format(S.char),
        14: lambda S, B, ret: ('两方都有人（`r = {}`，`d = {}`）→ 再投一轮'.format(S.r, S.d) if S.r > 0 and S.d > 0
                                                       else '有一方没人了 → 另一方获胜'),
        15: '这一轮有 `{tot}` 人要依次发言；幸存者会被压缩写回 `q` 的前面',
        16: '重新统计这轮的幸存者人数',
        17: lambda S, B, ret: ('这一轮 `{}` 人都处理完了' .format(S.tot) if B.get('index') == S.index and S.index == S.tot - 1 else '轮到 `q[{}]` = `{}` 发言'.format(S.index, S.q[S.index])),
        18: lambda S, B, ret: '轮到 ==R==' if S.q[S.index] == 'R' else '轮到 ==D==',
        19: lambda S, B, ret: ('有 `{}` 个 R 已被对方 ban → 这个 R 被 ban，无法发言'.format(S.del_r) if S.del_r > 0
                                           else '没人被 ban → 这个 R 可以发言'),
        20: '这个 R 被抵消了一次 ban：`del_r` → {del_r}',
        26: lambda S, B, ret: ('有 `{}` 个 D 已被对方 ban → 这个 D 被 ban，无法发言'.format(S.del_d) if S.del_d > 0
                                           else '没人被 ban → 这个 D 可以发言'),
        27: '这个 D 被抵消了一次 ban：`del_d` → {del_d}',
        22: '幸存者写回 `q[{r + d}]`，留到下一轮',
        29: '幸存者写回 `q[{r + d}]`，留到下一轮',
        23: 'R 幸存者 `r` → {r}',
        30: 'D 幸存者 `d` → {d}',
        24: '它发言 ban 掉后面尚未投票的 D：`del_d` → {del_d}',
        31: '它发言 ban 掉后面尚未投票的 R：`del_r` → {del_r}',
        33: lambda S, B, ret: ('D 全被 ban 光，R 胜' if S.r > 0 else 'R 全被 ban 光，D 胜'),
        "return 'Radiant'": '返回 `Radiant`',
        "return 'Dire'": '返回 `Dire`',
    },
    cards=dict(
        one_liner='优先 ban 对手马上要发言的人：用计数代替真的删除',
        complexity='时间 `O(n)`，空间 `O(n)`',
        problem=['Dota2 参议院：`R`（天辉）和 `D`（夜魇）按顺序投票，每人可以 ban 掉一名对手',
                 '被 ban 的人失去发言权；某一方人全被 ban 光，另一方获胜',
                 '示例：`"RDDRDR"` → `"Dire"`'],
        quote='在进行投票ban人时，应当优先杀伤对手马上要投票的生力军，而对于已经投过票的对手可以留在后面再ban。',
        quote_src='—— yiduobo 题解原文',
        idea=['例 `RDDRDR`：第一个 R 禁掉第一个 D，那第二个 D 就该禁掉第二个 R（尚未发言的），第三个 D 才有机会',
              '用 `del_r / del_d` 记「还要被 ban 几个」：轮到某人时若计数 > 0，他被 ban；否则他发言并让对方计数 +1',
              '幸存者压缩写回 `q` 前部，进入下一轮，直到某方人数为 0'],
        summary=['每轮至少少一半人，总处理量 `O(n)`；空间 `O(n)`',
                 '易错：发言者要 ban 的是==后面还没发言==的对手，所以用计数而不是真的删除',
                 '同一轮里写回位置 `q[r + d]` 不会超过读取位置 `index`，原地覆盖安全',
                 '对比常见双队列写法：这里没有队列，用计数 + 原地压缩；原文为 Python 2 风格，只删去了类型说明文档字符串，无需改动'],
    ),
)
