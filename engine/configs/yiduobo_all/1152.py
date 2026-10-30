USERS = ["joe", "joe", "joe", "james", "james", "james", "james"]
TIMES = [1, 2, 3, 4, 5, 6, 7]
SITES = ["home", "about", "career", "home", "cart", "about", "career"]
WEBS = list(dict.fromkeys(SITES))   # 按首次出现顺序编号 = 代码里的 wid


def _name(k):
    return f'{WEBS[k // 2500]}→{WEBS[k // 50 % 50]}→{WEBS[k % 50]}'


def _fn(S):
    if 'res' not in S:
        return ''
    r = S['res']
    return f"当前最优：`{'→'.join(r)}`（出现 =={S['max_f']}== 次）" if r else '当前最优：（还没有）'


CONFIG = dict(
    num=1152, title='用户网站访问行为分析', difficulty='Medium', category='常用数据结构',
    author='yiduobo', technique='哈希表计数 · 三重循环枚举访问模式',
    tags=['VIP 题'],
    code='''
class Solution(object):
    def mostVisitedPattern(self, username, timestamp, website):

        user2uid = {}
        web2wid = {}
        wid2web = {}

        user_watch = {}

        for user, t, web in zip(username, timestamp, website):
            if user not in user2uid:
                user2uid[user] = len(user2uid)
            uid = user2uid[user]
            
            if uid not in user_watch:
                user_watch[uid] = []
            
            if web not in web2wid:
                web2wid[web] = len(web2wid)
                
            wid = web2wid[web]
            wid2web[wid] = web

            user_watch[uid].append([t, wid])

        freq = {}
        for user in user_watch:
            watch_list = user_watch[user]
            watch_list.sort()
            pattern = set()
            for first in range(len(watch_list) - 2):
                for second in range(first + 1, len(watch_list) - 1):
                    for third in range(second + 1, len(watch_list)):
                        key = watch_list[first][1] * 2500 + watch_list[second][1] * 50 + watch_list[third][1]
                        pattern.add(key)
            
            for key in pattern:
                freq[key] = freq.get(key, 0) + 1
        
        res = None
        max_f = 0

        for key, f in freq.items():
            if f >= max_f:
                first_id = key // 2500
                second_id = key // 50 % 50
                third_id = key % 50
                candidate = [wid2web[first_id], wid2web[second_id], wid2web[third_id]]

                if f > max_f or candidate < res:
                    max_f = f
                    res = candidate[:]
        
        return res
''',
    call=f'Solution().mostVisitedPattern({USERS}, {TIMES}, {SITES})',
    expect=["home", "about", "career"],
    skip=['user2uid = {}', 'web2wid = {}', 'wid2web = {}', 'user_watch = {}', 'if user not in user2uid', 'user2uid[user] =',
          'uid = user2uid', 'if uid not in user_watch', 'user_watch[uid] = []', 'if web not in web2wid', 'web2wid[web] =',
          'wid = web2wid', 'wid2web[wid] = web', 'for first in range', 'for user, t, web in zip', 'pattern.add(key)', 'for second in range', 'for third in range',
          'for key in pattern:', 'first_id =', 'second_id =', 'third_id =', 'watch_list = user_watch', 'pattern = set()',
          'freq = {}', 'res = None', 'max_f = 0'],
    max_steps=90,
    views=[
        dict(type='map', var='user_watch', label='user_watch：uid → [[时间, 网站编号 wid], ...]', h=190,
             fmt=lambda k, v: str(v)),
        dict(type='map', var='web2wid', label='web2wid：网站 → 编号（按出现顺序）', h=170),
        dict(type='map', var='freq', label='freq：访问模式（3 个网站）→ 有几个用户访问过', h=270,
             fmt=lambda k, v: f'{_name(k)} ： {v}'),
        dict(type='text', fn=_fn, size=30, h=70),
    ],
    watch=['user', ('t', 't'), 'web', ('uid', 'uid', 'blue'), ('wid', 'wid', 'pink'), ('max_f', 'max_f', 'green')],
    captions={
        'user_watch[uid].append': '第一趟收集：`{user}`（uid={uid}）在时间 `{t}` 访问 `{web}`（编号 wid={wid}）→ 记成 `[{t}, {wid}]`。==网站换成 0~49 的编号==，后面才能拼成整数',
        'for user in user_watch': lambda S, B, r: ('所有用户都枚举完了，`freq` 里是每个模式的用户数' if B.get('user') == S.user else f'第二趟：逐个用户枚举访问模式。当前 uid = `{S.user}`'),
        'watch_list.sort()': '按时间戳排序：`[t, wid]` 的比较先看 `t`，访问顺序就对了 → `{watch_list}`',
        'key = watch_list[first][1]': lambda S, B, r: f'三重循环取任意三次访问（==不要求连续==），拼成整数：`{S.watch_list[S.first][1]}×2500 + {S.watch_list[S.second][1]}×50 + {S.watch_list[S.third][1]}` = `{S.key}`（`{_name(S.key)}`），放进 `set` 去重（已有 {len(S.pattern) + 1} 个模式）',
        'freq[key] = freq.get': lambda S, B, r: f'`{_name(S.key)}` 的人数 +1 → =={S.freq[S.key]}==：按==用户数==计数，不是出现次数',
        'if f >= max_f': lambda S, B, r: (f'`{_name(S.key)}` 被 `{S.f}` 个用户访问，`f = {S.f}` 对比当前最大 `max_f = {S.max_f}`：'
                                          + ('不小于它，继续比较' if S.f >= S.max_f else '更少，直接跳过')),
        'candidate = [': '解码 `key`：`{key} // 2500 = {first_id}`，`{key} // 50 % 50 = {second_id}`，`{key} % 50 = {third_id}` → 三个网站 `{candidate}`',
        'if f > max_f or candidate < res': lambda S, B, r: (
            f'`f = {S.f}` > `max_f = {B.max_f}` → 人数更多，直接更新' if S.f > B.max_f else
            f'人数相同（`{S.f}`），比字典序：`{S.candidate}` {"<" if S.candidate < S.res else ">="} `{S.res}` → ' + ('更小，更新' if S.candidate < S.res else '不更小，保留原来的')),
        'max_f = f': '`max_f` → `{max_f}`',
        'res = candidate[:]': '`res` → `{res}`',
        'return res': '人数最多、字典序最小的模式：`{ret}`',
    },
    cards=dict(
        one_liner='数据很小：枚举每个用户的所有三元组，哈希表按用户数计数',
        complexity='时间 `O(n·k^3)`（k 为单用户访问数），空间 `O(n)`',
        problem=['给出 `username`、`timestamp`、`website`：第 `i` 次访问是 `username[i]` 在 `timestamp[i]` 访问了 `website[i]`',
                 '==访问模式==：同一用户按时间顺序访问的 3 个网站（可以不连续、可以重复）',
                 '一个模式的得分 = 访问过它的==用户数==。返回得分最高的模式，并列时取字典序最小的',
                 '本视频：joe 访问 `home→about→career`，james 访问 `home→cart→about→career` → `home→about→career`'],
        quote='由于题目的数据规模很小，因此可以先一趟遍历，将每个用户的访问序列收集起来，接下来三重循环枚举a、b、c，并使用哈希表将所有枚举的访问模式记录下来。',
        quote_src='—— yiduobo 题解原文',
        idea=['先把每个用户的访问按时间排好，再三重循环取任意三次访问',
              '网站最多 50 个，用 ==3 位 50 进制整数==（`a×2500 + b×50 + c`）当模式的哈希键',
              '每个用户先把自己的模式放进 `set` 去重，再给全局 `freq` 各加 1 → 得分是用户数'],
        summary=['时间 `O(n·k^3)`，空间 `O(n)`：k 是同一用户的访问次数，数据小所以够用',
                 '易错：同一用户重复出现的模式只算一次，所以每人先用 `set` 去重',
                 '易错：并列时比较字典序（`candidate < res`），先判断 `f > max_f` 才不会拿 `None` 比较',
                 '原文为 Python 2 写法，整数除法 `key / 2500`、`key / 50 % 50` 已改为 `//`；其余原样',
                 '三重循环的位置是 `watch_list` 排序后的下标，所以顺序一定符合时间'],
    ),
)
