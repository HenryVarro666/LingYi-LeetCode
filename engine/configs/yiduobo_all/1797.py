
CONFIG = dict(
    num=1797, title='设计一个验证系统', difficulty='Medium', category='设计',
    author='yiduobo', technique='哈希表 · 延迟更新',
    tags=[],
    code='''
class AuthenticationManager(object):

    def __init__(self, timeToLive):
        self.timeToLive = timeToLive
        self.tokenDict = {}

    def generate(self, tokenId, currentTime):
        self.tokenDict[tokenId] = currentTime

    def renew(self, tokenId, currentTime):
        if tokenId in self.tokenDict:
            if currentTime - self.tokenDict[tokenId] >= self.timeToLive:
                self.tokenDict.pop(tokenId)
            else:
                self.tokenDict[tokenId] = currentTime

    def countUnexpiredTokens(self, currentTime):
        res = 0
        for tokenId in list(self.tokenDict.keys()):
            if currentTime - self.tokenDict[tokenId] >= self.timeToLive:
                self.tokenDict.pop(tokenId)
            else:
                res += 1
        
        return res
''',
    call="""am = AuthenticationManager(5)
out = []
am.renew('aaa', 1)
am.generate('aaa', 2)
out.append(am.countUnexpiredTokens(6))
am.generate('bbb', 7)
am.renew('aaa', 8)
am.renew('bbb', 10)
am.generate('ccc', 11)
out.append(am.countUnexpiredTokens(15))
out""",
    expect=[1, 1],
    views=[
        dict(type='text', h=70, fn=lambda S: (
            f"过期规则：`当前时间 − 记录时间 >= {S['self.timeToLive']}` 就算过期" if 'self.timeToLive' in S else '')),
        dict(type='map', var='self.tokenDict', label='tokenDict（token → 最近一次生成/续期的时间）', fmt=lambda k, v: f'{k} → t={v}', h=230),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=[('tokenId', 'tokenId', 'blue'), ('currentTime', 'currentTime', 'pink'), ('res', 'res', 'green')],
    captions={
        'self.timeToLive = timeToLive': '`timeToLive = {timeToLive}`：token 存活 {timeToLive} 秒',
        'self.tokenDict = {}': '哈希表：token → 最新更新时间，==不主动删除过期 token==',
        8: '新增：`tokenDict[{tokenId!r}] = {currentTime}`，直接写入（已有就覆盖）',
        11: lambda S, B, ret: (
            f"`{S.tokenId!r}` 在哈希表里 → 继续判断是否过期" if S.tokenId in S['self.tokenDict']
            else f"`{S.tokenId!r}` 不在哈希表里（没生成过或已被清理）→ 什么都不做"),
        12: lambda S, B, ret: (lambda d: (
            f"`{S.currentTime} − {S['self.tokenDict'][S.tokenId]} = {d}` >= `{S['self.timeToLive']}` → ==已过期==，延迟到现在才清理"
            if d >= S['self.timeToLive'] else
            f"`{S.currentTime} − {S['self.tokenDict'][S.tokenId]} = {d}` < `{S['self.timeToLive']}` → 还没过期，可以续期"))(
            S.currentTime - S['self.tokenDict'][S.tokenId]),
        13: '过期：把 `{tokenId!r}` 从哈希表删掉，它再也不能续期',
        15: '续期：`tokenDict[{tokenId!r}]` 刷新为 `{currentTime}`',
        18: '统计未过期数量：`res` 从 0 开始',
        19: lambda S, B, ret: ('遍历结束：表里剩下的都是未过期 token' if B.get('tokenId') == S.tokenId else f"检查 token `{S.tokenId!r}`（遍历时顺便清理过期的）"),
        20: lambda S, B, ret: (lambda d: (
            f"`{S.currentTime} − {S['self.tokenDict'][S.tokenId]} = {d}` >= `{S['self.timeToLive']}` → ==已过期==，不计数，顺手清理"
            if d >= S['self.timeToLive'] else
            f"`{S.currentTime} − {S['self.tokenDict'][S.tokenId]} = {d}` < `{S['self.timeToLive']}` → 仍有效，计数"))(
            S.currentTime - S['self.tokenDict'][S.tokenId]),
        21: '过期：从哈希表删除 `{tokenId!r}`（这就是延迟清理）',
        23: '未过期，`res` = {res}',
        25: '返回未过期数量 `{res}`',
    },
    skip=[],
    cards=dict(
        one_liner='过期不立刻删，等下次访问再清理（延迟更新）',
        complexity='generate / renew `O(1)`；count `O(n)`，空间 `O(n)`',
        problem=['`AuthenticationManager(timeToLive)`：token 生成或续期后存活 `timeToLive` 秒',
                 '`generate` 生成 token；`renew` 续期（已过期或不存在则忽略）',
                 '`countUnexpiredTokens` 返回当前未过期的 token 数',
                 '本视频：`timeToLive = 5`，操作时间 1→15，依次生成、续期、统计'],
        quote='对于这类问题，一个经典的做法就是延迟更新。……某个token到期后，并不是立即处理这个token，而是等到下次访问这个token，或者统计汇总信息的时候再更新这个token的信息。',
        quote_src='—— yiduobo 题解原文',
        idea=['哈希表只存每个 token 的==最新更新时间==，不开定时器',
              '`renew` 时才判断：已过期就删，没过期才刷新时间',
              '`count` 时遍历整张表，顺便把过期的清掉，剩下的就是答案'],
        summary=['`generate` / `renew` 为 `O(1)`，`count` 为 `O(n)`',
                 '过期条件是 `当前 − 记录 >= timeToLive`，恰好等于也算过期',
                 '原文为 Python 2 写法，遍历时 `pop` 在 Python 3 会报错，已将 `.keys()` 改为 `list(...keys())`',
                 '续期必须先判过期：过期的 token 不能被 renew 复活'],
    ),
)
