CONFIG = dict(
    num=2227, title='加密解密字符串', difficulty='Hard', category='贪心算法',
    author='灵茶山艾府', technique='逆向思维 · 加密字典再哈希计数',
    tags=['灵神题单·贪心与思维', '难度分 1945'],
    code='''
class Encrypter:
    def __init__(self, keys: List[str], values: List[str], dictionary: List[str]):
        self.map = dict(zip(keys, values))
        self.cnt = Counter(self.encrypt(s) for s in dictionary)

    def encrypt(self, word1: str) -> str:
        res = ""
        for ch in word1:
            if ch not in self.map:
                return ""
            res += self.map[ch]
        return res

    def decrypt(self, word2: str) -> int:
        return self.cnt[word2]
''',
    call='''e = Encrypter(['a','b','c','d'], ["ei","zf","ei","am"], ["abd","cbd","dd"])
r1 = e.encrypt("abd")
r2 = e.decrypt("eizfam")
[r1, r2]''',
    expect=['eizfam', 2],
    views=[
        dict(type='map', var='self.map', label='map（字母 → 两位密文）', fmt=lambda k, v: f"'{k}' → {v}", h=120, font=30),
        dict(type='map', var='self.cnt', label='cnt（密文 → 有几个字典词能加密成它）', fmt=lambda k, v: f"{k}: {v}", h=120, font=30),
        dict(type='text', h=70, size=28,
             fn=lambda S: (f"正在加密 `{S['word1']}`，已拼出 `{S['res']}`" if 'word1' in S and 'res' in S else
                           (f"解密 `{S['word2']}`：直接查 cnt" if 'word2' in S else ''))),
        dict(type='calls', label='正在执行', h=130),
    ],
    watch=[('ch', 'ch', 'blue'), ('res', 'res', 'pink'), ('word2', 'word2', 'orange')],
    captions={
        'self.map = dict': '`keys` 和 `values` 配对，建加密表：{self.map}',
        'self.cnt = Counter': '==逆向==：把字典里每个词都先加密，再用哈希表数各密文出现几次 → {self.cnt}',
        'res = ""': '从空串开始拼接密文',
        'for ch in word1': lambda S, B, r: (f"取下一个字符 `{S.ch}`" if len(S.res) // 2 < len(S.word1) else f"`{S.word1}` 的字符都处理完了"),
        'if ch not in': lambda S, B, r: (f"`{S.ch}` 不在 keys 里 → 无法加密" if S.ch not in S['self'].map
                                         else f"`{S.ch}` 在 keys 里，可以加密"),
        'return ""': '有字符无法加密，返回空串',
        'res += self.map': '`{ch}` 换成 `{self.map[ch]}`，`res` = =={res}==',
        'return res': '加密完成：`{res}`',
        'return self.cnt': '解密不用枚举：加密后等于 `{word2}` 的字典词有 =={ret}== 个，直接读 `cnt`',
    },
    cards=dict(
        one_liner='解密有多解，那就反过来：先把字典全加密',
        complexity='构造 `O(字典总长)`，加密 `O(n)`，解密 `O(1)`（不计哈希）',
        problem=['`Encrypter`：`encrypt` 用 `keys[i]` 换成 `values[i]`（两位）',
                 '`decrypt` 返回有多少个解密结果落在 `dictionary` 里',
                 '`values` 可重复，一个密文可能解出多个原文'],
        quote='直接解密较为复杂，不妨逆向思考，即加密 dictionary 中的每个字符串，并用哈希表记录每个加密后的字符串的出现次数。',
        quote_src='—— 灵茶山艾府题解',
        idea=['`values` 有重复，所以密文 → 原文不唯一，正向解密会组合爆炸',
              '加密是确定的：构造时把每个字典词加密，`Counter` 数出现次数',
              '`decrypt(word2)` 只剩一次查表'],
        summary=['复杂度：构造 `O(Σ len(dictionary[i]))`，`encrypt` `O(n)`，`decrypt` `O(1)`',
                 '易错：字典词里有 `keys` 外的字符时加密返回 `""`，不能计入',
                 '本题字典词都能加密；正向解密枚举会指数爆炸',
                 '思想：正向复杂就逆向，同类题 3307、880'],
    ),
)
