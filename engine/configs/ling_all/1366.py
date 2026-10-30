def _txt(S):
    if 'cnts' not in S:
        return '每支队伍记一个长为 m 的「名次票数」列表：第 i 位 = 排第 i 的票数'
    c = S['cnts']
    if S.get('_line') == 8:
        order = sorted(c, key=lambda ch: (c[ch], ch))
        return '排序键 `(cnts[ch], ch)`：票数取了相反数，==字典序小 = 票数多==，再按字母 → ==' + ''.join(order) + '=='
    if 'ch' in S and 'i' in S:
        return f'`{S["ch"]}` 排第 `{S["i"] + 1}` 名的票数 −1（取负）：`cnts[{S["ch"]!r}] = {c[S["ch"]]}`'
    return '遍历每张票，给每个字母在对应名次上记一票'


CONFIG = dict(
    num=1366, title='通过投票对团队排名', difficulty='Medium', category='字符串',
    author='灵茶山艾府', technique='名次计数列表 · 排序',
    tags=[],
    code='''
class Solution:
    def rankTeams(self, votes: List[str]) -> str:
        m = len(votes[0])
        cnts = defaultdict(lambda: [0] * m)
        for vote in votes:
            for i, ch in enumerate(vote):
                cnts[ch][i] -= 1  # 改成负数（相反数），方便比大小
        return ''.join(sorted(cnts, key=lambda ch: (cnts[ch], ch)))
''',
    call="Solution().rankTeams(['ABC', 'ACB', 'ABC', 'ACB', 'ACB'])",
    expect='ACB',
    views=[
        dict(type='text', fn=_txt, h=60),
        dict(type='array', var='vote', label='当前这张票（第 1 位 = 最高排名）', pointers={'i': 'blue'}, h=190),
        dict(type='map', var='cnts', label='cnts：字母 → 各名次票数的相反数',
             fmt=lambda k, v: f'{k} → {v}', h=130),
    ],
    watch=[('i', 'i', 'blue'), ('ch', 'ch', 'pink')],
    captions={
        'm = len(votes[0])': '每张票都排了 `m = {m}` 支队伍，名次列表长度就是 `m`',
        'cnts = defaultdict': '`cnts[字母]` 默认是 `m` 个 0：每个名次得到的票数',
        'for vote in votes': lambda S, B, r: (lambda p: '所有票都统计完了，`cnts` 里每个字母都有一份名次票数' if p == len(S.votes)
                                              else f'读第 {p + 1} 张票 `{S.vote}`')(-sum(sum(v) for v in S.cnts.values()) // S.m),
        'cnts[ch][i] -= 1': '`{ch}` 在这张票排第 `{i + 1}`：`cnts[{ch!r}][{i}]` → `{cnts[ch][i]}`（取相反数：票越多越小）',
        'return': '键是 `(cnts[ch], ch)`：先比名次票数列表（==越负越靠前==），平局再比字母 → 结果 =={ret}==',
    },
    cards=dict(
        one_liner='给每支队伍记一个「各名次票数」列表，按列表字典序排',
        complexity='时间 `O(nm + m² log m)`，空间 `O(m²)`',
        problem=['每张投票是一个字符串，按「从高到低」给所有队伍排名',
                 '按得「第一名」票数多的排前面；并列看「第二名」票数，以此类推；全平局按字母序',
                 '示例：`["ABC","ACB","ABC","ACB","ACB"]` → `"ACB"`'],
        quote='把每种字母及其出现次数列表，记到一个哈希表（或数组）中。……第一关键字：字母的出现次数列表，字典序大的排在前面；第二关键字：字母的大小（ASCII 值），小的排在前面。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`A` 记作 `[5,0,0]`：第 1 名 5 票；`B` 是 `[0,2,3]`；`C` 是 `[0,3,2]`',
              '列表比较本身就是「先比第一名票数，再比第二名……」',
              '票数取相反数，就能直接升序排序；字母放第二关键字处理完全平局'],
        summary=['时间 `O(nm + m² log m)`，空间 `O(m²)`',
                 '易错：次数列表要比「大的在前」，所以取负数再升序',
                 '全平局时字母小的在前，`(cnts[ch], ch)` 的第二项正好管这个'],
    ),
)
