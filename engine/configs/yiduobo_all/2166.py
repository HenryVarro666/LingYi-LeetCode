def _real(S):
    """实际的位集：arr 在翻转标记为 True 时取反"""
    arr, f = S.get('self.arr'), S.get('self.filp_flag')
    if arr is None:
        return None
    return [1 - x for x in arr] if f else list(arr)


def _txt(S):
    arr = S.get('self.arr')
    if arr is None:
        return ''
    f = S.get('self.filp_flag')
    real = ''.join(map(str, _real(S)))
    return f"实际位集 = ==\"{real}\"==（{'arr 取反' if f else 'arr 原样'}）　`cnt = {S.get('self.cnt')}`，`size = {S.get('self.size')}`"


CONFIG = dict(
    num=2166, title='设计位集', difficulty='Medium', category='设计',
    author='yiduobo', technique='翻转标记 + 计数器', tags=[],
    code='''
class Bitset(object):

    def __init__(self, size):
        self.size = size
        self.arr = [0] * size
        self.cnt = 0
        self.filp_flag = False

    def fix(self, idx):
        if self.filp_flag:
            target = 1
        else:
            target = 0

        if self.arr[idx] == target:
            self.arr[idx] = 1 - target
            self.cnt += 1

    def unfix(self, idx):
        if self.filp_flag:
            target = 0
        else:
            target = 1
        
        if self.arr[idx] == target:
            self.arr[idx] = 1 - target
            self.cnt -= 1

    def flip(self):
        self.filp_flag = not self.filp_flag
        self.cnt = self.size - self.cnt

    def all(self):
        return self.cnt == self.size

    def one(self):
        return self.cnt > 0

    def count(self):
        return self.cnt

    def toString(self):
        if self.filp_flag:
            return ''.join([str(1 - x) for x in self.arr])
        else:
            return ''.join([str(x) for x in self.arr])
''',
    call='''bs = Bitset(5)
out = [bs.fix(3), bs.fix(1), bs.flip(), bs.all(), bs.unfix(0), bs.flip(), bs.one(), bs.unfix(0), bs.count(), bs.toString()]
out''',
    expect=[None, None, None, False, None, None, True, None, 2, '01010'],
    views=[
        dict(type='text', size=28, h=110, fn=_txt),
        dict(type='array', var='self.arr', label='arr（存的是「没翻转」时的位；翻转标记为 True 时实际值取反）', cell=110, h=210,
             pointers={'idx': 'blue'},
             color=lambda S, i, v: ('green' if (v ^ (1 if S.get('self.filp_flag') else 0)) else None)),
        dict(type='array', var=lambda S: _real(S) or [], label='实际位集（arr 按标记取反之后）', cell=110, h=200,
             color=lambda S, i, v: 'green' if v else None),
    ],
    watch=[('flip标记', 'self.filp_flag', 'purple'), ('cnt', 'self.cnt', 'green'), ('size', 'self.size'), ('idx', 'idx', 'blue'), ('target', 'target', 'orange')],
    captions={
        'self.size = size': '`size = {size}`：位集的长度',
        'self.arr = [0] * size': '`arr` 存每一位，初始全 0：`{self.arr}`',
        'self.cnt = 0': '`cnt` 记录实际位集里 1 的个数，这样 `all / one / count` 都是 O(1)',
        'self.filp_flag = False': '`filp_flag` 是翻转标记：不真的翻转数组，只记「当前是否翻转过奇数次」',
        10: '`filp_flag = {self.filp_flag}`：' + '{"已翻转，arr 存的值和实际相反 → fix 要找 arr 里的 1（实际是 0）" if self.filp_flag else "没翻转 → fix 要找 arr 里的 0"}',
        11: '已翻转：实际为 0 的位在 arr 里存的是 1 → `target = 1`',
        13: '没翻转：fix 要把实际的 0 变成 1 → `target = 0`',
        20: '`filp_flag = {self.filp_flag}`：' + '{"已翻转，arr 存的值和实际相反 → unfix 要找 arr 里的 0（实际是 1）" if self.filp_flag else "没翻转 → unfix 要找 arr 里的 1"}',
        21: '已翻转：实际为 1 的位在 arr 里存的是 0 → `target = 0`',
        23: '没翻转：unfix 要把实际的 1 变成 0 → `target = 1`',
        15: '`arr[{idx}] = {self.arr[idx]}`，`target = {target}` → ' + '{"相等，这一位需要修改" if self.arr[idx] == target else "不相等：这一位已经是目标状态，什么也不做"}',
        25: '`arr[{idx}] = {self.arr[idx]}`，`target = {target}` → ' + '{"相等，这一位需要修改" if self.arr[idx] == target else "不相等：这一位已经是目标状态，什么也不做"}',
        16: '把 `arr[{idx}]` 改成 `1 - target = {1 - target}`',
        26: '把 `arr[{idx}]` 改成 `1 - target = {1 - target}`',
        43: '`filp_flag = {self.filp_flag}`：toString 要输出实际的位，' + '{"已翻转 → arr 每位取反" if self.filp_flag else "没翻转 → arr 原样输出"}',
        'self.cnt += 1': '实际多了一个 1：`cnt` → =={self.cnt}==',
        'self.cnt -= 1': '实际少了一个 1：`cnt` → =={self.cnt}==',
        'self.filp_flag = not': '翻转标记取反 → `{self.filp_flag}`：数组一位都不用动，O(1)',
        'self.cnt = self.size - self.cnt': '0 和 1 互换，1 的个数变成 `size - cnt` = =={self.cnt}==',
        'return self.cnt == self.size': '`cnt = {self.cnt}`，`size = {self.size}` → 全是 1 吗？`{ret}`',
        'return self.cnt > 0': '`cnt = {self.cnt} > 0` → 至少有一个 1：`{ret}`',
        'return self.cnt': '直接返回计数器 `cnt = {ret}`',
        "return ''.join([str(1 - x)": '翻转状态：每一位取反再拼接 → =="{ret}"==（O(size)，最多调用 5 次）',
        "return ''.join([str(x)": '没翻转：直接拼接 → =="{ret}"==',
    },
    max_steps=90,
    cards=dict(
        one_liner='flip 不真翻数组：打个标记，再维护 1 的个数',
        complexity='除 `toString` 为 `O(size)` 外，其余操作均为 `O(1)`',
        problem=['设计位集：`fix` 置 1、`unfix` 置 0、`flip` 翻转所有位',
                 '`all` 是否全 1、`one` 是否有 1、`count` 1 的个数、`toString` 输出',
                 '示例：`Bitset(5)` → `fix(3), fix(1), flip() ...` → `toString = "01010"`'],
        quote='偶数次的flip操作就相当于没有flip，因此可以设置一个标记，表示当前是否flip过。但是需要的注意的是，在两次flip操作之间的fix以及unfix的效果是相反的',
        quote_src='—— yiduobo 题解原文',
        idea=['`flip` 调用次数不限，不能每次遍历数组 → 用 `filp_flag` 打标记',
              '翻转后 `fix / unfix` 的效果相反：用 `target` 适配，要找的值取反',
              '`cnt` 在 fix、unfix、flip 里都能 O(1) 更新，翻转时变成 `size - cnt`',
              '`toString` 最多调用 5 次，每次直接遍历即可'],
        summary=['`fix / unfix / flip / all / one / count` 均为 `O(1)`，`toString` 为 `O(size)`，空间 `O(size)`',
                 '易错点：翻转标记为真时，arr 里存的值和实际值相反，`fix` 要找的是 arr 中的 1',
                 '只有「位真的变了」才改 `cnt`，重复 fix 同一位不能重复加',
                 '原文的标记变量名拼写为 `filp_flag`，代码保持原样；对比灵神：同样是懒标记 + cnt'],
    ),
)
