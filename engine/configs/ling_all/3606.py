_CODE = ["SAVE20", "", "PHARMA5", "SAVE@20", "Z9", "A_1"]


def _grp(S):
    g = S.get('groups')
    if g is None:
        return ''
    names = ['electronics', 'grocery', 'pharmacy', 'restaurant']
    return '  '.join(f"`{names[i]}`={g[i]}" for i in range(len(g)))


def _ok(S, B, ret):
    s, bus, active, cat = S.s, S.bus, S.active, S.category
    why = []
    if not s:
        why.append('code 为空')
    elif not all(c == '_' or c.isalnum() for c in s):
        why.append('code 含非法字符')
    if cat < 0:
        why.append('类别不合法')
    if not active:
        why.append('未激活')
    if why:
        return f"`{s!r}`：{'、'.join(why)} → ==无效==，跳过"
    return f"`{s}` 三个条件都满足 → ==有效==，加入第 {cat} 组"


CONFIG = dict(
    num=3606, title='优惠券校验器', difficulty='Easy', category='模拟',
    author='灵茶山艾府', technique='哈希表分组 + 组内排序',
    tags=[],
    code='''
BUSINESS_LINE_TO_CATEGORY = {
    "electronics": 0,
    "grocery": 1,
    "pharmacy": 2,
    "restaurant": 3,
}

class Solution:
    def validateCoupons(self, code: List[str], businessLine: List[str], isActive: List[bool]) -> List[str]:
        groups = [[] for _ in range(len(BUSINESS_LINE_TO_CATEGORY))]
        for s, bus, active in zip(code, businessLine, isActive):
            category = BUSINESS_LINE_TO_CATEGORY.get(bus, -1)
            if s and category >= 0 and active and \\
               all(c == '_' or c.isalnum() for c in s):
                groups[category].append(s)  # 相同类别的优惠码分到同一组

        ans = []
        for g in groups:
            g.sort()  # 每一组内部排序
            ans += g
        return ans
''',
    call='Solution().validateCoupons(["SAVE20","","PHARMA5","SAVE@20","Z9","A_1"], ["restaurant","grocery","pharmacy","restaurant","grocery","grocery"], [True]*6)',
    expect=['A_1', 'Z9', 'PHARMA5', 'SAVE20'],
    views=[
        dict(type='array', var='code', label='code（蓝 = 当前优惠券）', cell=130, h=170,
             color=lambda S, i, v: 'blue' if S.get('s') == v else None),
        dict(type='text', fn=lambda S: '类别 → 编号：`electronics`=0  `grocery`=1  `pharmacy`=2  `restaurant`=3（查不到 = 非法）', size=22),
        dict(type='text', fn=_grp, size=24),
        dict(type='text', fn=lambda S: ('结果 `ans` = ' + str(S['ans'])) if 'ans' in S else '', size=28),
    ],
    skip=['all(c =='],
    watch=['s', 'bus', 'active', 'category', ('ans', 'ans', 'green')],
    captions={
        'groups = [': '四个类别各一个空列表：`groups = {groups}`，下标就是类别编号',
        'for s, bus, active': '取出一张优惠券：`s = {s!r}`，`bus = {bus!r}`，`active = {active}`',
        'category = ': '哈希表查类别：`{bus!r}` → 编号 =={category}==（查不到就是 `-1`，即类别非法）',
        'if s and': _ok,
        'groups[category].append': '`{s}` 放进第 {category} 组：`groups = {groups}`',
        'ans = []': '分组完成，下面逐组排序后拼起来：`groups = {groups}`',
        'for g in groups': '处理下一组 `g = {g}`',
        'g.sort()': '组内按字典序排序 → `g = {g}`（逐字符比较 ASCII：`A` < `Z`）',
        'ans += g': '把这一组接到答案后面：`ans = {ans}`',
        'return ans': '组与组之间的顺序天然由编号 0,1,2,3 保证 → 返回 `{ret}`',
    },
    cards=dict(
        one_liner='用哈希表给类别编号，分四组，每组内部排序再拼起来',
        complexity='时间 `O(L log n)`，空间 `O(n)`',
        problem=['给出 `code`、`businessLine`、`isActive` 三个数组，筛出==有效优惠券==',
                 '有效：code 非空且只含字母数字和 `_`；类别是 4 个之一；已激活',
                 '按类别顺序、类别内按字典序输出 code'],
        quote='用一个哈希表保存类别到类别编号（0,1,2,3）的映射，方便把答案分组，顺带可以判断类别是否合法（是否在哈希表中）。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`get(bus, -1)`：编号 >= 0 同时说明类别合法',
              '有效的 code 按编号放进对应的列表，==不用写复杂的多关键字排序==',
              '最后每组只需 `sort()`，依次拼接即得答案'],
        summary=['时间 `O(L log n)`，`L` 是所有 code 长度之和，瓶颈在排序',
                 '易错：code 为空串要先判 `s`，`isalnum` 对空串返回 False 但 `all([])` 为 True',
                 '`isalnum` 对中文也返回 True，本题 code 是 ASCII 所以没问题',
                 '分组思想：先按第一关键字桶分，再在桶内按第二关键字排序'],
    ),
)
