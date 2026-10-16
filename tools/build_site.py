import re, html, urllib.parse, datetime, pathlib
CSS = open(pathlib.Path(__file__).with_name('base.css'), encoding='utf-8').read()
CSS += """
[hidden]{display:none!important}
.crumbs{font-size:12px;color:var(--muted)}
.crumbs a{color:var(--muted)}
.mast a.brand{color:inherit;text-decoration:none}
.navlinks{display:flex;gap:4px;margin-left:auto;flex-wrap:wrap}
.navlinks a{padding:8px 12px 9px;font-weight:700;color:var(--muted);text-decoration:none;border-bottom:3px solid transparent}
.navlinks a[aria-current="page"]{color:var(--ink);border-bottom-color:var(--accent)}
.blist{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.blist a{display:block;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:12px 16px;text-decoration:none;color:var(--ink);font-weight:700}
.blist small{display:block;font-weight:400;color:var(--muted);font-size:12px}
.prose{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:22px 20px;display:flex;flex-direction:column;gap:14px}
.prose p,.prose ul{margin:0;max-width:40em}

/* catalogue: photo-first cards */
.cards{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:14px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;min-width:0}
.ph{display:block;aspect-ratio:1;background:#fff;border-bottom:1px solid var(--line);position:relative}
.ph img{width:100%;height:100%;object-fit:contain;display:block}
.ph.none{background:var(--chip);color:var(--link);display:grid;place-items:center;text-decoration:none;text-align:center;font-size:12px;line-height:1.6}
.ph.none svg{width:38%;height:auto;display:block;margin:0 auto 6px}
.kind{position:absolute;left:8px;top:8px;background:var(--strong);color:var(--strong-ink);font-size:11px;font-weight:700;border-radius:999px;padding:1px 10px;line-height:1.7}
.card-b{padding:12px 12px 14px;display:flex;flex-direction:column;gap:6px;flex:1;min-width:0}
.ep{font-size:11px;color:var(--muted);line-height:1.5}
.card .name{font-size:14px;line-height:1.5}
.card .name a{color:inherit;text-decoration:none}
.catch{font-size:13px;line-height:1.6;color:var(--ink);margin:0}
.card .price{font-size:19px;margin-top:auto;padding-top:4px;white-space:normal}
.cond{font-size:11px;color:var(--muted);line-height:1.5}
.card .btn{text-align:center;padding:9px 10px}
.more{font-size:12px;text-align:center}

/* article */
.epbox{background:var(--chip);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.epbox h2{font-size:15px}
dl.kv{margin:0;display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 14px;font-size:14px}
dl.kv dt{color:var(--muted);font-weight:700;font-size:12px;letter-spacing:.04em;padding-top:2px;white-space:nowrap}
dl.kv dd{margin:0;min-width:0;overflow-wrap:anywhere}
.block{display:grid;grid-template-columns:300px minmax(0,1fr);gap:18px;align-items:start;padding-top:20px}
.block .ph{border:1px solid var(--line);border-radius:14px;overflow:hidden}
.block-b{display:flex;flex-direction:column;gap:10px;min-width:0}
.block h3{font-family:var(--display);font-size:18px;line-height:1.5}
.block .catch{font-weight:700;font-size:15px;color:var(--strong)}
.block p{max-width:38em}
.eat{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.eat b{font-size:12px;color:var(--muted);letter-spacing:.04em;margin-right:2px}
.eat span{background:var(--ok-bg);color:var(--ok);border-radius:999px;padding:1px 10px;font-size:12px;line-height:1.7}
.said{border-left:4px solid var(--accent);background:var(--bg);border-radius:0 8px 8px 0;padding:8px 12px;font-size:13px}
.buyrow{display:flex;flex-wrap:wrap;align-items:center;gap:10px 16px}
.btn.big{font-size:15px;padding:11px 22px;background:var(--strong);color:var(--strong-ink)}
.sub{font-weight:700;font-size:13px;color:var(--muted);letter-spacing:.04em;margin-top:4px}
.article table{min-width:0}
.block td:first-child{min-width:4.6em}
.block.nophoto{grid-template-columns:1fr}
.block{scroll-margin-top:84px}
.ph.cover img{object-fit:cover}
.kakaku{border:1px solid var(--line);border-radius:12px;padding:12px 14px;display:flex;flex-direction:column;gap:8px;background:var(--bg)}
.kakaku h4{margin:0;font-size:13px;font-weight:700;letter-spacing:.04em;color:var(--muted)}
.kakaku ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:6px}
.kakaku li{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:2px 10px;align-items:center;background:var(--surface);border:1px solid var(--line);border-radius:10px;padding:8px 10px}
.kakaku li .p{grid-column:1;grid-row:1}
.kakaku li .shopnm{grid-column:1;grid-row:2}
.kakaku li a{grid-column:2;grid-row:1/3}
.kakaku .p{font-family:var(--display);font-weight:900;font-size:17px;white-space:nowrap}
.kakaku .p small{font-family:var(--body);font-weight:400;font-size:11px;color:var(--muted);margin-left:4px}
.kakaku .shopnm{font-size:12px;line-height:1.5;min-width:0;overflow-wrap:anywhere}
.kakaku .tag{display:inline-block;white-space:nowrap;font-size:11px;font-weight:700;border-radius:999px;padding:0 8px;line-height:1.7;background:var(--ok-bg);color:var(--ok);margin-right:4px}
.kakaku .tag.off{background:var(--warn-bg);color:var(--warn)}
.kakaku .tag.tv{background:var(--chip);color:var(--ink)}
.kakaku li.gone{opacity:.6}
.kakaku p{font-size:13px}
.mark{font-size:11px;font-weight:700;border-radius:6px;padding:2px 8px;line-height:1.6;align-self:flex-start}
.mark.gone{background:var(--warn-bg);color:var(--warn)}
.mark.alt{background:var(--ok-bg);color:var(--ok);text-decoration:none}
.kotsu{margin:0;padding-left:1.2em;font-size:14px;display:flex;flex-direction:column;gap:4px}
.credit{position:absolute;left:0;bottom:0;background:rgba(0,0,0,.6);color:#fff;font-size:10px;line-height:1.6;padding:1px 7px;border-radius:0 6px 0 0}
.phs{display:flex;flex-direction:column;gap:10px;min-width:0}
.block .ph.land{aspect-ratio:16/9}
.prnote{margin:0 0 8px;font-size:13px;color:var(--ink)}
/* まとめ買いリスト */
.add{border:1px solid var(--strong);background:var(--surface);color:var(--strong);font-weight:700;font-size:12px;border-radius:8px;padding:7px 8px;cursor:pointer;line-height:1.5}
.add[aria-pressed="true"]{background:var(--ok-bg);border-color:var(--ok);color:var(--ok)}
.bulk{background:var(--warn-bg);border-radius:12px;padding:14px 16px;display:flex;flex-direction:column;gap:8px}
.bulk h2{font-size:15px}
.bulk p{margin:0;font-size:14px}
.cartbar{position:fixed;left:0;right:0;bottom:0;z-index:8;background:var(--ink);color:#fff;padding:10px 16px calc(10px + env(safe-area-inset-bottom,0px));display:flex;align-items:center;justify-content:center;gap:10px 16px;flex-wrap:wrap}
.cartbar b{font-family:var(--display);font-size:16px}
.cartbar .btn{background:var(--accent);color:var(--accent-ink)}
body.hascart{padding-bottom:76px}
.cartpanel{position:fixed;inset:0;z-index:9;background:rgba(58,46,44,.45);display:flex;align-items:flex-end;justify-content:center}
.cartsheet{background:var(--surface);width:100%;max-width:560px;max-height:86vh;overflow:auto;border-radius:16px 16px 0 0;padding:18px 16px calc(18px + env(safe-area-inset-bottom,0px));display:flex;flex-direction:column;gap:12px}
.carthead{display:flex;align-items:center;justify-content:space-between;gap:12px}
.cartsheet p{margin:0;font-size:13px}
.cartlist{list-style:none;margin:0;padding:0;display:flex;flex-direction:column}
.cartlist li{display:grid;grid-template-columns:64px minmax(0,1fr) auto;gap:10px;align-items:center;padding:10px 0;border-top:1px solid var(--line)}
.cartlist img{width:64px;height:64px;object-fit:contain;border:1px solid var(--line);border-radius:8px;background:#fff}
.cartlist .nm{font-size:13px;font-weight:700;line-height:1.5}
.cartlist .pr2{font-size:13px;color:var(--muted)}
.cartlist .ops{display:flex;flex-direction:column;gap:6px;align-items:stretch;text-align:center}
.cartlist .seen{font-size:11px;color:var(--ok)}
.x{background:none;border:0;color:var(--muted);font-size:12px;text-decoration:underline;cursor:pointer;padding:2px}
.carttotal{display:flex;justify-content:space-between;align-items:baseline;border-top:2px solid var(--ink);padding-top:10px;font-weight:700}
@media (max-width:720px){.block{grid-template-columns:1fr}.block .ph{max-width:340px;width:100%;margin:0 auto}}
@media (max-width:600px){
  .navlinks{margin-left:0;width:100%}.navlinks a{flex:1;text-align:center;white-space:nowrap;font-size:14px;padding-inline:4px}
  .cards{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  .card-b{padding:10px 10px 12px}
  .card .price{font-size:17px}
}
"""
BASE = 'https://hirumemo.com/'
TODAY = (datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(hours=9)).date().isoformat()
GA_ID = 'G-KXTP512PVZ'  # Googleアナリティクスの測定ID（G-XXXX）。空なら計測タグは出さない
FAV = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Ccircle cx='32' cy='32' r='28' fill='%23f6a700'/%3E%3Ctext x='32' y='43' font-size='30' text-anchor='middle' fill='%23fff' font-family='sans-serif' font-weight='900'%3E%E3%81%B2%3C/text%3E%3C/svg%3E"
def cutdesc(t, n=120):
    if len(t)<=n: return t
    c=t[:n]; i=c.rfind('。')
    return c[:i+1] if i>=40 else c.rstrip('、')+'…'
AFF = '584a3b37.2a4108aa.584a3b38.a1b9d8be'
ME = '1390601'
NOTE = '[商品価格に関しましては、リンクが作成された時点と現時点で情報が変更されている場合がございます。]'
WD = '月火水木金土日'
DISH = '<svg viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><path d="M6 30h36"/><path d="M10 30a14 14 0 0 1 28 0"/><path d="M24 12v4"/><path d="M14 38h20"/></svg>'
ONSEN = '<svg viewBox="0 0 48 48" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><path d="M8 30c0 7 7 11 16 11s16-4 16-11"/><path d="M8 30c4-3 28-3 32 0"/><path d="M17 8c-3 4 3 6 0 11M24 6c-3 4 3 7 0 13M31 8c-3 4 3 6 0 11"/></svg>'
def q(s): return urllib.parse.quote(s, safe='')
def e(s): return html.escape(str(s), quote=True)
def rk(code): return f'https://hb.afl.rakuten.co.jp/ichiba/{AFF}/?pc=' + q(f'https://item.rakuten.co.jp/akomeyatokyo/{code}/')
def rimg(item_id, path, s=400): return f'https://hbb.afl.rakuten.co.jp/hgb/{AFF}/?me_id={ME}&item_id={item_id}&pc=' + q(f'https://thumbnail.image.rakuten.co.jp/@0_mall/akomeyatokyo/cabinet/{path}?_ex={s}x{s}') + f'&s={s}x{s}&t=picttext'
def yen(n, fr=False): return '確認中' if n is None else f'{n:,}円' + ('〜' if fr else '')
def dlong(d): return f'{d.year}年{d.month}月{d.day}日（{WD[d.weekday()]}）'
def dshort(d): return f'{d.month}月{d.day}日'

POINTDAY = 'https://hb.afl.rakuten.co.jp/hgc/584a3b39.dd9c39ba.584a3b3a.f5e65f8f/?pc=https%3A%2F%2Fevent.rakuten.co.jp%2Fcard%2Fpointday%2F&link_type=text&ut=eyJwYWdlIjoidXJsIiwidHlwZSI6InRleHQiLCJjb2wiOjF9'
SHOPS = {'AKOMEYA TOKYO': dict(label='AKOMEYA TOKYO 楽天市場店',
  url='https://hb.afl.rakuten.co.jp/hgc/584a3b37.2a4108aa.584a3b38.a1b9d8be/?pc=https%3A%2F%2Fwww.rakuten.co.jp%2Fakomeyatokyo%2Fcontents%2Fmedia%2F20250919%2F&link_type=text&ut=eyJwYWdlIjoidXJsIiwidHlwZSI6InRleHQiLCJjb2wiOjF9',
  ship='送料の目安：宅配便 710円（北海道 1,420円・沖縄 2,130円）、メール便対応の商品は 250円。2026年10月8日確認。')}
def cmpbox(it):
    if not it.get('id'): return ''
    code=it['id']; offs=OFFERS.get(code) or [(it['price'],1,None,None)]; out = code in SOLDOUT
    ins=[o for o in offs if not (o[2] is None and out)]
    lowest=min((o for o in ins), key=lambda o:o[0]) if ins else None
    incl=[o for o in ins if o[1]==0]; lowin=min(incl,key=lambda o:o[0]) if incl else None
    rows=[]
    for o in offs:
        pr,pf,shop,url=o; mine = shop is None
        tags=''
        if mine: tags+='<span class="tag tv">番組で紹介されたお店</span>'
        if mine and out: tags+='<span class="tag off">在庫切れ</span>'
        if o is lowest and len(ins)>1: tags+='<span class="tag">本体価格がいちばん安い</span>'
        if o is lowin: tags+='<span class="tag">送料込みでいちばん安い</span>'
        rows.append(f'<li{" class=\"gone\"" if (mine and out) else ""}><span class="p">{yen(pr)}<small>{"送料込" if pf==0 else "送料別"}</small></span><span class="shopnm">{tags}{e(OFFICIAL[1] if mine else shop)}</span><a class="btn ghost" href="{e(it["url"] if mine else url)}" {A}>見る</a></li>')
    only = len(offs)==1
    lead = f'<p>楽天市場では、番組で紹介されたお店（{e(OFFICIAL[1])}）だけが販売しています。{"いまは在庫切れです。" if out else ""}</p>' if only else (f'<p>番組で紹介されたお店は在庫切れですが、ほかのお店で買えます。</p>' if out else '')
    return f'''<div class="kakaku" data-jan="{e(code)}" data-kw="{e(KW.get(code,""))}" data-base="{it['price']}" data-shop="{OFFICIAL[0]}" data-shopname="{e(OFFICIAL[1])}" data-url="{e(it['url'])}"><h4>楽天市場の価格くらべ</h4>{lead}<ul>{''.join(rows)}</ul><p class="note"><span class="when">{SNAP}に確認</span>。1個売りを本体価格の安い順に並べています。内容量と送料は各お店のページでご確認ください。</p></div>'''
def addbtn(it, shop):
    if not it.get('id'): return ''
    return f'<button class="add" type="button" aria-pressed="false" data-id="{e(it["id"])}" data-shop="{e(shop)}" data-name="{e(it["name"])}" data-price="{it["price"]}" data-url="{e(it["url"])}" data-img="{e(it["img"])}">＋ まとめ買いリストへ</button>'
def bulkbox(b):
    if not b['items'] and not b.get('deal'): return ''
    d = b.get('deal')
    if d: return f'<div class="bulk"><h2>{e(d["title"])}</h2><p>{e(d["text"])}</p><p class="note">{e(d["note"])}</p><div><a class="btn" href="{e(d["url"])}" {A}>{e(d["btn"])}</a></div></div>'
    sh = SHOPS.get(b['shop'])
    if not sh: return ''
    return f'''<div class="bulk"><h2>まとめ買いできます</h2>
<p>ここで紹介している{len(b['items'])}品は、すべて同じお店（{e(sh['label'])}）の商品です。1品が数百円なので、気になるものを「まとめ買いリスト」に入れて、1回の注文にまとめるのがおすすめです。送料は注文1回ごとにかかります。</p>
<p class="note">{e(sh['ship'])}</p>
<div><a class="btn" href="{e(sh['url'])}" {A}>お店の紹介商品ページでまとめて選ぶ</a></div>
<h2>お得に買うコツ</h2>
<ul class="kotsu">
<li><b>5と0のつく日に買う</b>：毎月5・10・15・20・25・30日は、エントリーして楽天カードで払うとポイントが4倍になります。<span class="d50"></span> <a href="{e(POINTDAY)}" {A}>エントリーはこちら</a></li>
<li><b>1回の注文にまとめる</b>：送料は注文ごとにかかるので、同じお店の商品はまとめたほうが送料1回分で済みます。</li>
<li><b>1品だけなら価格くらべを見る</b>：ほかのお店のほうが安かったり、送料込みで買えたりする商品があります。各商品の「楽天市場の価格くらべ」に、確認した日時つきで載せています。</li>
</ul></div>'''
OFFICIAL = ('akomeyatokyo', 'AKOMEYA TOKYO 楽天市場店')
SNAP = '2026年10月8日 10時ごろ'
def au(code, path): return f'https://hb.afl.rakuten.co.jp/hgc/{code}/?pc=' + q(f'https://item.rakuten.co.jp/{path}/') + '&rafcid=wsc_i_is_931d9945-ec85-47b8-bb97-c6e651fbb4fd'
# snapshot of the Rakuten Ichiba price search (single-unit offers, cheapest first): (price, postageFlag 0=込 1=別, shop name, url or None for the featured shop)
OFFERS = {
 '4900325025268': [(410,1,'季折 楽天市場店',au('g00sb5jo.hwjef1bb.g00sb5jo.hwjeg942','e-kiori/403143')),(490,1,None,None),(540,0,'せとうちユカリーギフト',au('g00twf9o.hwjeffa7.g00twf9o.hwjegac2','onegoroya/mazekake-furi-n1'))],
 '4970905233413': [(418,1,'プロフーズ',au('g00pw95o.hwjef5c4.g00pw95o.hwjeg7ef','profoods/10010427')),(454,1,'楽天24',au('g00r136o.hwjefb4e.g00r136o.hwjeg380','rakuten24/4970905233413')),(470,1,None,None),(700,0,'海鮮KARATO 河上商店 楽天市場店',au('g00tsq6o.hwjefb4a.g00tsq6o.hwjegeba','kawakami-fish/10000037'))],
 '4580330652811': [(648,1,None,None),(741,1,'生活雑貨のお店!Vie-UP',au('g00r57uo.hwjef941.g00r57uo.hwjeg4b1','vie-up/et-2570059100009')),(832,1,'ポッチ',au('g00tbzko.hwjefd3c.g00tbzko.hwjega56','pocchi-shop/m-4580330652811'))],
}
SOLDOUT = {'4970905233413','4580330653160'}   # featured shop out of stock at SNAP
KW = {'4900325025268':'のどぐろ','4970905233413':'しそわかめ','4580330652811':'マッシュルームイチバン'}
AN = 'target="_blank" rel="noopener"'
def ra(it): return A if it.get('aff', True) else AN
def S(name, kind, price, url, btn, catch, desc, eat, specs, place, fr=0, said=None, eatlabel='おすすめの食べ方', pricenote='税込'):
    return dict(id=None, kind=kind, aff=False, name=name, price=price, fr=fr, url=url, img=None, catch=catch, desc=desc, eat=eat, specs=specs, said=said,
                btn=btn, cond='税込', place=place, eatlabel=eatlabel, pricenote=pricenote)
def P(name, price, code, iid, path, catch, desc, eat, specs, fr=0, said=None):
    return dict(id=code, name=name, price=price, fr=fr, url=rk(code), img=rimg(iid, path), catch=catch, desc=desc, eat=eat, specs=specs, said=said,
                btn='楽天市場で見る', cond='税込', place='楽天市場（AKOMEYA TOKYO 公式ショップ）')

AK = [
 P('AKOMEYA TOKYO 味付き鶏節削り 極薄削り',648,'4977930004063','10001371','10273314/4977930004063_1.jpg',
   'かつお節よりあっさり、うま味はしっかり',
   '鹿児島県で作られた「鶏節」に薄く塩味をつけて、ごく薄く削った削り節です。かつお節に比べて淡泊なのに、うま味はしっかり。口当たりが軽いので、いつもの料理にふわっとのせるだけで一品らしくなります。',
   ['卵かけごはん','サラダ','冷奴','厚揚げ'], [('主な原料','鶏節（鹿児島県製造）'),('味つけ','薄い塩味')]),
 P('AKOMEYA TOKYO サクサク ふりかけ（とり）30g',680,'4977930004414','10004392','09516418/imgrc0091562033.jpg',
   '甘辛しょう油味の、サクサク食感',
   '薄く削った鶏節をしょう油・みりん・砂糖で甘辛く味つけし、すりごまをまぶしたふりかけです。名前のとおりサクサクした食感で、海苔の風味が鶏節の味を引き立てます。',
   ['炊きたてごはん','おにぎり'], [('内容量','30g'),('原材料','鶏節（国内製造）、しょう油、みりん、砂糖、のり、ごま、食塩')]),
 P('AKOMEYA TOKYO 極薄削りふりかけ（とり）',756,'4977930004391','10004390','09516418/imgrc0091555678.jpg',
   '0.01mmの極薄削りで、ふわふわ',
   '0.01mmの薄さに削ったとり節に、海苔とちりめんを合わせたふりかけです。ごはんにのせるとふわふわの口どけ。味つけは控えめで、素材の風味を楽しむタイプです。同じシリーズに「かつお」「いわし」もあります。',
   ['熱いごはんにのせて','お好みでしょう油をひとたらし'], [('主な原料','とり節、海苔、ちりめん'),('シリーズ','とり／かつお／いわし')]),
 P('AKOMEYA TOKYO ごま和え胡麻 スタンドパック(60g)／ボトル(180g)',620,'4546722900038','10000007','biiino/item/main-image/20251125175000_1.jpg',
   'ゆで野菜に和えるだけで、ごま和えが完成',
   'しょう油味のごまに、アーモンドとかつお節を合わせた香ばしい「かけるごま」です。ゆでた野菜に和えるだけでごま和えになり、ごはんや麺、冷奴にそのままかけても使えます。まず試すなら60gのスタンドパック、気に入ったら180gのボトルを。',
   ['野菜のごま和え','ごはん・おにぎり','うどん・そうめん','冷奴','サラダ'], [('内容量','スタンドパック60g／ボトル180g'),('主な原料','ごま、アーモンド、かつお節'),('賞味期限','製造日から365日')], fr=1),
 P('まぜ×かけ のどぐろ 100g',490,'4900325025268','10003705','08950751/imgrc0089651857.jpg',
   '高級魚のどぐろ入り。混ぜても、かけても',
   '甘じょっぱく味つけしたひじきに、あおさ、とろろ昆布、国産のどぐろを合わせたソフトタイプのふりかけです。ごはんに混ぜれば混ぜごはんに、そのままかければふりかけに。姉妹品に「あご」「梅」「わさび」もあります。',
   ['混ぜごはん','卵かけごはん','和風パスタの具'], [('内容量','100g'),('主な原料','ひじき、あおさ、とろろ昆布、のどぐろ（国産）')],
   said='この商品は2023年10月26日放送の「ヒルナンデス！」でも登場。出演者から「もう毎日これでいい！」という声が出たと、暮らし情報サイトのヨムーノが伝えています。'),
 P('井上商店 ソフトふりかけ しそわかめ',470,'4970905233413','10004337','09516418/imgrc0093249136.jpg',
   '萩の「わかめ飯」がもとの、しそ風味',
   '山口県・萩地方で昔から食べられてきた「わかめ飯」をもとにした、しそ風味のやわらかいふりかけです。ごはんに混ぜるだけで、わかめごはんになります。',
   ['温かいごはん','ピラフ','お好み焼き','うどん','野菜サラダ'], [('製造','井上商店（山口県）'),('味','しそ風味')]),
 P('AKOMEYA TOKYO おおぶり焼きほぐし 天然真鯛',750,'4905171007277','10007388','10494522/11293831/imgrc0104764265.jpg',
   '愛媛の天然真鯛を、大きめのほぐし身で',
   '愛媛県産の天然真鯛を焼いて大きめにほぐし、鯛のあら・昆布・貝のだしと藻塩で味つけした瓶詰めです。身がしっとりしていて、鯛のうま味にだしの香りが重なります。',
   ['おにぎりの具','だしをかけてお茶漬け'], [('主な原料','天然真鯛（愛媛県産）、だし（鯛あら・昆布・貝）、藻塩'),('容器','瓶詰め')]),
 P('マッシュルームイチバン',648,'4580330652811','10005480','10273314/45803306528111.jpg',
   '粗みじんとペースト、2つの食感',
   '千葉県産のマッシュルームを「粗みじん切り」と「ペースト」の2通りに加工して合わせた瓶詰めです。ごはんにもパンにも合い、マヨネーズやクリームチーズに混ぜればディップにもなります。',
   ['卵かけごはん','パン','パスタ','ディップソース'], [('主な原料','マッシュルーム（千葉県産）'),('容器','瓶詰め')]),
 P('AKOMEYA TOKYO 卵かけ専用 かける牛肉ビビンバ',750,'4580330653160','10007168','10494522/11293831/imgrc0104933366.jpg',
   '卵かけごはんが、甘辛ビビンバ風に',
   '国産牛肉、人参、ニラをコチュジャンベースで甘辛く仕上げた、卵かけごはん専用のお供です。卵と混ぜてちょうどよい濃いめの味つけ。うどんや鍋の味つけにも使えます。シリーズはほかに「ニララー油」「魯肉飯」。',
   ['卵かけごはん','うどん','焼肉','鍋'], [('主な原料','国産牛肉、人参、ニラ、コチュジャン'),('シリーズ','牛肉ビビンバ／ニララー油／魯肉飯')]),
 P('AKOMEYA TOKYO 卵かけ専用 かけるニララー油',750,'4580330653177','10007169','10494522/11293831/imgrc0104933454.jpg',
   '大きめニラの、旨辛スタミナ系',
   '食感が残るよう大きめに切った国産ニラに、千葉県産の生姜、玉ねぎ、にんにく、唐辛子を合わせた、卵かけごはん専用のラー油です。濃いめの旨辛味で、麺や炒め物にも使えます。',
   ['卵かけごはん','麺類','炒め物','和え物'], [('主な原料','ニラ（国産）、生姜（千葉県産）、玉ねぎ、にんにく、唐辛子'),('シリーズ','牛肉ビビンバ／ニララー油／魯肉飯')]),
 P('AKOMEYA TOKYO ピリ辛山菜きのこ',519,'4990998106029','10003884','09935422/compass1685349857.jpg',
   '6種のきのこと山菜を、ピリ辛で',
   'えのき、たけのこ、ぶなしめじ、山くらげ、きくらげ、しいたけの6種を使ったピリ辛の瓶詰めです。長野県のメーカー「高見澤」との共同開発。ごはんにのせるほか、冷奴やラーメンの具にもなります。',
   ['ごはん','炒め物','冷奴','ラーメンの具'], [('具材','えのき、たけのこ、ぶなしめじ、山くらげ、きくらげ、しいたけ'),('共同開発','高見澤（長野県）')]),
 P('AKOMEYA TOKYO たっぷり具材 豚そぼろ大葉味噌',780,'4580330652903','10006282','10494522/10610737/4580330652903_1.jpg',
   '国産豚と大葉の、甘辛みそ',
   '国産の豚肉と刻み大葉を、白味噌と赤味噌で甘辛く仕上げた肉みそです。肉を炒めた油で香味野菜の香りを引き出していて、味噌のコクのあとに大葉の香りが残ります。',
   ['炊きたてごはん','おにぎりの具','冷奴','野菜のディップ'], [('主な原料','豚肉（国産）、大葉（国産）、白味噌、赤味噌'),('容器','瓶詰め')]),
 P('AKOMEYA TOKYO たっぷり具材 鮪とねぎの生姜煮',780,'4580330653061','10006670','10494522/0329-2134.jpg',
   'まぐろと長ねぎを、生姜でピリッと',
   'ビンチョウマグロと千葉県産の長ねぎ、針生姜をじっくり甘辛く煮込み、唐辛子で後味をピリッと引き締めた瓶詰めです。ごはんのお供にも、そのまま小鉢の一品にもなります。',
   ['ごはん','おにぎりの具','小鉢の一品','お酒のおつまみ'], [('主な原料','ビンチョウマグロ、長ねぎ（千葉県産）、生姜、唐辛子'),('容器','瓶詰め')]),
 P('AKOMEYA TOKYO 炊き込みごはんの素 宮城県産鮭バターめし 2合炊き用',1500,'4905171008144','10008580','biiino/item/main-image/20250820181532_1.jpg',
   'お米2合と炊くだけ。宮城の銀鮭とバター',
   '宮城県産の銀鮭に、松山あげ、だし昆布、人参を合わせた炊き込みごはんの素です。バターはフリーズドライで別添え。お米2合と一緒に炊飯器に入れて炊くだけで、鮭とバターのコクのあるごはんになります。',
   ['お米2合と炊飯器で炊く'], [('内容量','2合炊き用'),('主な原料','銀鮭（宮城県産）、バター（フリーズドライ）、松山あげ、だし昆布、人参')]),
 P('AKOMEYA TOKYO アコメヤの出汁 きのこ 35g（7g×5袋）',600,'4974560000694','10008576','biiino/item/main-image/20250820180612_1.jpg',
   '舞茸と椎茸の、香りのだしパック',
   '国産の舞茸と椎茸を使っただしパックです。きのこの香りとうま味が出るので、炊き込みごはんや鍋のベースに。袋を破って中身をそのまま和風パスタにからめる使い方もできます。',
   ['炊き込みごはん','鍋','うどん・そばのつゆ','和風パスタ'], [('内容量','35g（7g×5袋）'),('主な原料','舞茸・椎茸（国産）')]),
 P('AKOMEYA TOKYO アコメヤのゆずぽん酢',880,'4984252900232','10007402','10494522/10967989/0920ak224.jpg',
   '徳島県産ゆず果汁をたっぷり',
   '徳島県産のゆず果汁をたっぷり使い、国産丸大豆しょう油、純米酢、釜で煮出しただしを合わせたぽん酢です。島根・奥出雲の醤油蔵「森田醤油」との共同開発。鍋の季節の前に1本あると重宝します。',
   ['焼き魚','焼肉','豆腐','生野菜'], [('主な原料','ゆず果汁（徳島県産）、国産丸大豆しょう油、純米酢、だし'),('共同開発','森田醤油（島根県）')]),
]

OMORI = dict(id=None, name='伊香保温泉 和心の宿 大森', price=30800, fr=1, img='https://img.travel.rakuten.co.jp/share/HOTEL/10737/10737.jpg', img2='https://img.travel.rakuten.co.jp/share/HOTEL/10737/10737_room.jpg', credit='楽天トラベル',
  url='https://hb.afl.rakuten.co.jp/hgc/584eca7f.b482ba06.584eca80.649f3027/?pc=https%3A%2F%2Ftravel.rakuten.co.jp%2FHOTEL%2F10737%2F10737.html&link_type=text&ut=eyJwYWdlIjoidXJsIiwidHlwZSI6InRleHQiLCJjb2wiOjF9',
  btn='楽天トラベルで空室を見る', cond='赤城牛つき会席・和室10〜14畳／1泊2食・2名1室の1名あたり・税込', place='楽天トラベル',
  catch='標高800mの屋上露天風呂と、赤城牛の会席',
  desc='大正8年（1919年）創業、伊香保温泉の全35室の宿です。屋上の露天風呂は標高およそ800mにあり、赤城山などの山並みを見ながら伊香保の「白銀の湯」に入れます。部屋は10畳の和室から33畳のグループ向けまであり、夕食は群馬の食材を使った会席です。',
  eat=[], said=None,
  specs=[('住所','群馬県渋川市伊香保町伊香保58'),('アクセス','伊香保温泉バス停から徒歩約1分／関越道 渋川伊香保ICから約12km'),('チェックイン','15:00（最終19:00）／チェックアウト10:00'),('部屋数','全35室'),('お風呂','屋上露天風呂（標高約800m）、大浴場、貸切露天風呂。泉質は単純泉（白銀の湯）'),('クチコミ','楽天トラベルの総合評価 4.58（1,541件）。朝食 4.63／夕食 4.55／風呂 4.50。2026年10月8日時点')],
  tables=[('部屋の広さ',['部屋タイプ','広さ','定員'],[
      ('和室','10〜14畳','1〜6人'),('和洋室（10畳＋ベッド）','10畳','2〜5人'),('展望温泉付き和室','10畳','1〜3人'),
      ('展望温泉付き和洋室','20畳','1〜4人'),('温泉付きゆったり和洋室','20畳','1〜4人'),('ファミリー＆グループルーム','33畳','大人4名以上')]),
    ('ごはん',['','内容','食べる場所'],[
      ('夕食','旬の食材を使った会席。上州ブランドの赤城牛がつくプラン、上位プランは赤城和牛の「逸会席」','標準プランは会場食、上位プランは個室食'),
      ('朝食','群馬の野菜とお米を使った「健康朝食」','広間')]),
    ('料金の目安（2名1室・1名あたり・1泊2食・税込）',['プラン','部屋','料金'],[
      ('赤城牛つき会席（会場食）','和室10〜14畳','30,800円〜35,200円'),('赤城牛つき会席（会場食）','和洋室10畳＋ベッド','34,100円〜39,600円'),
      ('赤城和牛つき逸会席（個室食）','和モダンツイン','41,800円〜47,300円'),('赤城和牛つき逸会席（個室食）','半露天風呂付き和洋室','52,800円〜58,300円')])])

B = [
 dict(slug='20261016-kinugawa-mikazuki', date=datetime.date(2026,10,16), kind='店', shop='鬼怒川・世田谷', theme='宿・ステーキ・バウムクーヘン・焼肉',
   title='【ヒルナンデス】10月16日放送｜鬼怒川紅葉旅（ステーキよし乃・はちやカフェ・日光きぬ川スパホテル三日月）と有名人ファミリー探偵（米沢屋）まとめ',
   label='陣内智則さん・野々村友紀子さんの鬼怒川紅葉旅と、福田雄一さん行きつけの米沢牛焼肉', checked='2026年10月16日',
   tochead='紹介されたお店・商品・宿一覧',
   ep=[('放送日','2026年10月16日（金）'),('番組','日本テレビ系「ヒルナンデス！」'),
       ('企画','「夫婦円満の秘訣大調査！鬼怒川紅葉旅」／「有名人ファミリー探偵！」（番組表の表記による）'),
       ('ロケ','鬼怒川紅葉旅：陣内智則さん、野々村友紀子さん（VTRゲスト）／有名人ファミリー探偵：タイムマシーン3号'),
       ('スタジオ','南原清隆さん、伊藤遼さん（日本テレビアナウンサー）、久本雅美さん、陣内智則さん、西尾由佳理さん、タイムマシーン3号、王林さん、ゲスト 新川優愛さん')],
   intro='2026年10月16日（金）放送の「ヒルナンデス！」は、陣内智則さんと野々村友紀子さんが紅葉前の栃木・鬼怒川を旅する企画と、タイムマシーン3号が有名人の家族を調べる「有名人ファミリー探偵！」でした。足利マール牛のステーキ店、焼きたてバウムクーヘンのカフェ、1泊で最大5食が付くホテル、福田雄一さん行きつけの米沢牛の焼肉店など、紹介が確かめられた6件を値段と買える場所つきでまとめました。',
   notes=[('まだ確認できていないこと',[
       'ステーキよし乃・はちやカフェ・米沢屋のメニューの正式な値段（下の値段は放送まとめサイトの記載で、税込かどうかも確認中です）',
       'はちやバウム・ろっくバウムの税込価格と、お店での値段',
       '日光きぬ川スパホテル三日月の料金、部屋数、番組で使った部屋とプラン',
       '鬼怒川近くのロープウェイ（視聴者の投稿1件で触れられたのみで、名前と紹介の裏づけは確認中）',
       '出演者の味や感想（どれも確認が取れていません）',
       '見逃し配信の有無'])],
   foot='※紹介されたことは番組表、放送まとめサイト、視聴者の投稿で確かめています。出演者の発言は確認が取れていないため載せていません。値段はお店・販売サイトの表示で確かめられたものを参考として載せ、税込と確かめられないものは「確認中」としています（2026年10月16日確認）。',
   items=[
    S('渓谷のレストラン ステーキよし乃（鬼怒川温泉）','店',None,'https://gj3h100.gorp.jp/','お店のページを見る',
      '栃木のブランド牛を焼く、渓谷沿いのステーキ店',
      '栃木県のブランド牛「足利マール牛」を中心に、地元の食材を使うレストランです。番組では、リブロースとフィレのステーキ、和牛の握り、生パスタのペペロンチーノなどが登場したと、放送まとめサイト2件が伝えています。鬼怒川温泉駅から歩いて約15分です。',
      ['足利マール牛のリブロース','足利マール牛のフィレ','和牛握り（2貫）','生パスタのペペロンチーノ'],
      [('場所','栃木県日光市鬼怒川温泉大原680-1（鬼怒川温泉駅から徒歩約15分）'),('営業','ランチ11:30〜14:30（L.O.14:00）、ディナー17:00〜20:30（L.O.19:30）、月・火定休（お店の公式ページ、2026年10月16日確認。とちぎ旅ネットでは時間の記載が異なり、祝日・シーズン中は営業とあります）'),('電話','0288-25-7762'),('値段','確認中（放送まとめサイト2件の記載：足利マール牛リブロース100g 7,500円、フィレ100g 8,250円、和牛握り2貫 2,200円、生パスタのペペロンチーノ 1,500円。税込かどうかは確認中）'),('通販','なし（店内飲食のみ）')],
      '店頭のみ', eatlabel='番組で登場したメニュー',
      said='陣内智則さんと野々村友紀子さんが訪れました（放送まとめサイト2件より）。発言の中身は確認中です。'),
    S('はちやカフェ（バウムクーヘン工房はちや・鬼怒川温泉）','店',None,'https://hachiya-nikko.jp/hachiya_cafe/','お店のページを見る',
      '焼きたてを温かいまま出す、バウムクーヘンのカフェ',
      '「バウムクーヘン工房はちや」の隣にあるカフェです。店内で焼いたバウムクーヘンを温かいうちに出す「HOTバウムクーヘン」が名物で、番組では「賞味期限10分」のバウムクーヘンとして紹介されたと、放送まとめサイト2件と視聴者の投稿が伝えています。下のホテル三日月のすぐ近くです。',
      ['HOTバウムクーヘン 4種盛り（プレーン・ろっく・いちご・日光しょうゆ）','バウムソフト 日光しょうゆ','バウムソフト 和栗'],
      [('場所','栃木県日光市鬼怒川温泉大原1396-43'),('営業','9:00〜16:45（お店の公式ページ、2026年10月16日確認）。定休日は確認中'),('電話','0288-77-1453'),('値段','確認中（放送まとめサイト2件の記載：HOTバウムクーヘン4種盛り 700円、バウムソフト日光しょうゆ 700円、バウムソフト和栗 800円。税込かどうかは確認中）')],
      '店頭のみ', eatlabel='番組で登場したメニュー',
      said='陣内智則さんと野々村友紀子さんが訪れました（放送まとめサイト2件より）。発言の中身は確認中です。'),
    S('バウムクーヘン工房はちや「はちやバウム（S）」','商品',None,'https://www.baumkuchen-hachiya.com/view/item/000000000001','公式通販で見る',
      '日光の卵で焼いた、定番の丸いバウムクーヘン',
      '日光産の卵「日光御養卵」、カルピスバター、北関東産の小麦を使い、生地を一層ずつ重ねて焼いたバウムクーヘンです。直径約14cm・高さ約4cmの丸い形で、常温で日持ちするので、鬼怒川みやげにも向いています。',
      ['そのまま常温で','コーヒーや紅茶と','薄く切り分けて家族で','鬼怒川みやげ・手みやげに'],
      [('内容量','1個250g（直径約14cm・高さ約4cm）'),('主な原材料','卵（日光産）、砂糖、ショートニング、バター、クリーム、小麦粉など（小麦・卵・乳成分を含む）'),('賞味期限','未開封・常温で14日'),('値段','確認中（公式通販の表示は1,728円。税込かどうかの記載はなく、放送まとめサイトでは1,620円。2026年10月16日確認）'),('在庫','公式通販で在庫あり（2026年10月16日確認）')],
      '公式通販、はちやカフェ店頭'),
    S('バウムクーヘン工房はちや「ろっくバウム（S）」','商品',None,'https://www.baumkuchen-hachiya.com/view/item/000000000004','公式通販で見る',
      '外はカリッ、中はもっちりの、岩のようなバウムクーヘン',
      '鬼怒川渓谷の岩をイメージした、縦長の形のハードタイプのバウムクーヘンです。日光御養卵とカルピス発酵バターを使い、外側はカリッと、中はもっちりした食感とされています。',
      ['そのまま外側の歯ざわりを楽しむ','軽く温めてバターの香りを立たせる','厚めに切ってコーヒーと','手みやげに'],
      [('内容量','1個300g（直径約8cm・高さ約12cm）'),('主な原材料','卵（日光産）、砂糖、小麦粉、バター、ショートニング、アーモンドパウダー、脱脂粉乳など（小麦・卵・乳成分・アーモンドを含む）'),('賞味期限','未開封・常温で21日'),('値段','確認中（公式通販の表示は2,958円。税込かどうかの記載はなく、放送まとめサイトでは2,850円。2026年10月16日確認）'),('在庫','公式通販で在庫あり（2026年10月16日確認）')],
      '公式通販、はちやカフェ店頭'),
    dict(S('日光きぬ川スパホテル三日月','宿',None,'https://www.mikazuki.co.jp/kinugawa/','公式サイトで見る',
      '1泊で最大5食が付く、鬼怒川の温泉ホテル',
      '鬼怒川温泉駅から歩いてすぐの、鬼怒川沿いのホテルです。宿泊料金に、到着日のウェルカムランチから夕食・夜食・朝食・チェックアウト後のランチまで最大5食と、約20種類の飲み物が含まれます。水着で入る屋外の温泉「おぷ～ろ」（約40℃、鬼怒川渓谷を望む）や温水プールも使えます（公式サイト、2026年10月16日確認）。',
      [],
      [('住所','栃木県日光市鬼怒川温泉大原1400'),('アクセス','東武 鬼怒川温泉駅から徒歩約3分（送迎なし）'),('チェックイン','フロント受付12:00から、入室15:00から／チェックアウト10:00（公式サイトのよくある質問）'),('部屋数','確認中'),('お風呂','水着で入る屋外の温泉「おぷ～ろ」、温水プール、スパ、鬼怒川を望む温泉'),('食べる場所','館内レストラン「ALL DAY DINING」（部屋食なし）'),('料金の目安','確認中（日程・人数・部屋で変わります）')],
      '公式サイト、楽天トラベル（「日光きぬ川ホテル三日月」の名前で掲載、住所は同じ）。じゃらんは確認中',
      said='陣内智則さんと野々村友紀子さんの鬼怒川の旅で登場しました（番組表の予告「おぷーろ」「1泊5食付き」と、視聴者の投稿より）。発言の中身は確認中です。'),
      placelabel='予約できる場所',
      tables=[('部屋の広さ（公式サイト、2026年10月16日確認）',['部屋タイプ','広さ','定員'],[
          ('スタンダード 和洋室','45㎡（和室6畳＋セミダブル2台）','確認中'),('スタンダード 広々和洋室','56㎡','最大8名'),('スタンダード コンパクトツイン','約15㎡','確認中'),
          ('スーペリア 和モダンルーム','45㎡（テラス付き。プライベートおぷ～ろ付きの部屋もあり）','確認中'),('スーペリア ファミリールーム','72㎡','確認中'),
          ('スーペリア デラックスツイン','約38㎡または45㎡（公式に2つの記載あり）','確認中'),('プレミアム（露天風呂付きなど）','全室90㎡以上','確認中'),('キッズルーム','確認中','確認中')]),
        ('ごはん（最大5食）',['','内容','時間'],[
          ('ウェルカムランチ','確認中','11:00〜14:30'),
          ('夕食','ビュッフェ。ライブキッチン、寿司・ステーキ、デザート、キッズビュッフェあり。アルコールを含む20種以上の飲み放題付き（公式のレストランページ）','18:00〜21:00'),
          ('夜','確認中','21:00〜22:30'),
          ('朝食','ビュッフェ','7:00〜9:00'),
          ('チェックアウト後のランチ','確認中','11:00〜14:30')])],),
    S('米沢屋（世田谷・深沢）','店',None,'https://tabilist.net/262269/','お店の紹介記事を見る',
      '米沢牛だけを扱う、世田谷の焼肉店',
      '山形の米沢牛A5ランクを専門に、内臓まで米沢牛でそろえる焼肉店です。水を張った七輪で焼くスタイルで、番組では塊で出る内モモ、厚切りの特上牛タン、ねぎ塩ハラミ、女将の手作りキムチが登場したと、放送まとめサイト2件が伝えています。',
      ['内モモ（約300gの塊）','特上牛タン','米沢牛ねぎ塩ハラミ','女将の手作りキムチ'],
      [('場所','東京都世田谷区深沢3-3-13（尾山台駅・九品仏駅・自由が丘駅から徒歩約15分）'),('営業','18:00〜23:00、火曜定休（放送まとめサイトの記載。お店の公式では確認中）'),('電話','03-5707-5575'),('値段','確認中（放送まとめサイト2件の記載：米沢牛ねぎ塩ハラミ 3,850円。税込かどうかと、ほかのメニューの値段は確認中）'),('通販','なし（店内飲食のみ）')],
      '店頭のみ（夜のみ）', eatlabel='番組で登場したメニュー',
      said='福田雄一さんの行きつけのお店として紹介されました（放送まとめサイト2件より）。発言の中身は確認中です。'),
   ]),
 dict(slug='20261015-oarai-hands', date=datetime.date(2026,10,15), kind='宿', shop='茨城大洗・ハンズ', theme='宿・海鮮・キッチン用品・健康家電',
   title='【ヒルナンデス】10月15日放送｜茨城大洗の1泊2食付き2万5千円旅（大洗パークホテル・かあちゃんの店ほか）とハンズ売上1位（キャベピィMAX・ゴリラのひとつかみ）まとめ',
   label='茨城大洗の1泊2食付き2万5千円旅と、ハンズの売上1位', checked='2026年10月15日',
   tochead='紹介された宿・お店・商品一覧',
   ep=[('放送日','2026年10月15日（木）'),('番組','日本テレビ系「ヒルナンデス！」'),
       ('企画','「海鮮グルメの宝庫・茨城大洗で1泊2食付き予算2万5千円満喫プラン」（番組表の予告による）／カルディ・ハンズ・IKEAの売れ筋紹介（コーナー名は確認中）'),
       ('ロケ','大洗の旅：なすなかにし、高城れにさん（ももいろクローバーZ）。番組表では柳原可奈子さん、羽野晶紀さん、井戸田潤さん（スピードワゴン）もVTR出演（担当した企画は確認中）'),
       ('スタジオ','南原清隆さん、浦野モモさん（日本テレビアナウンサー）、横山裕さん（SUPER EIGHT）、生見愛瑠さん、木村昴さん、大沢あかねさん、榊原郁恵さん、ゲスト 仁村紗和さん、ヤーレンズ')],
   intro='2026年10月15日（木）放送の「ヒルナンデス！」は、なすなかにしと高城れにさんが茨城県大洗町を1泊2食付き・予算2万5千円で旅する企画と、カルディ・ハンズ・IKEAの売上1位を紹介する企画でした。紹介が確かめられた宿・お店・商品の5件を、値段と買える場所つきでまとめました。',
   notes=[('まだ確認できていないこと',[
       'カルディの売上1位の調味料と、IKEAの売上1位（フリーザーバッグ・収納ワゴン）の商品名',
       '大洗パークホテルで番組が使ったプラン・部屋・料理と、その料金',
       'かあちゃんの店で食べたメニューと、お店での値段',
       'ハンズでのキャベピィMAX・ゴリラのひとつかみの値段',
       '出演者の味や使い心地の感想（どれも確認が取れていません）'])],
   foot='※紹介されたことは番組表、視聴者の投稿で確かめています。出演者の発言は確認が取れていないため載せていません。値段は宿・お店・販売サイトの表示で確かめられたものだけを載せ、それ以外は「確認中」としています（2026年10月15日確認）。',
   items=[
    S('かあちゃんの店（大洗町磯浜町）','店',None,'https://www.nap-camp.com/mag/48399','お店の紹介記事を見る',
      '大洗の漁師町にある、魚料理の食堂',
      '刺身・煮付け・かき揚げ・フライなどの定食がそろう地元の食堂で、ブリカマ定食が看板とされています。料金は先払いで、お茶や水はセルフです。番組の予告では、400円のあんこう汁、生しらす丼、天然ぶり漬け丼が挙がっていました（放送でどれを食べたかは確認中）。',
      ['ブリカマ定食','あんこう汁','生しらす丼'],
      [('場所','茨城県東茨城郡大洗町磯浜町8253-20'),('営業','火〜日 10:00〜14:00、月曜定休（なっぷマガジンの記載、2026年10月15日確認）'),('値段','確認中（番組の予告では、あんこう汁400円）'),('通販','なし（店内飲食のみ）')],
      '店頭のみ', eatlabel='予告に出たメニュー',
      said='高城れにさんが二色丼を注文したという視聴者の投稿が1件あります。発言の中身は確認中です。'),
    S('アクアワールド茨城県大洗水族館','店',None,'https://www.aquaworld-oarai.com/guide/admission/','公式サイトの入場料金を見る',
      'サメの展示で知られる、大洗の大型水族館',
      '番組の予告では、年間100万人が訪れる人気の水族館として、ペンギンの餌やりとサメとのふれあいが紹介されていました。下の大洗パークホテルの目の前にあります。体験プログラムの名前と料金は確認中です。',
      ['サメの展示を中心に','大洗パークホテルとあわせて1泊で'],
      [('場所','茨城県東茨城郡大洗町磯浜町8252-3'),('営業','9:00〜17:00（最終入館16:00）'),('入館料','大人2,300円、小・中学生1,100円、幼児（3歳以上）400円、3歳未満無料（公式の入場料金ページの表示。税込かどうかは記載なし。2026年10月15日確認）'),('体験プログラム','確認中')],
      '現地', eatlabel='行くときのコツ'),
    dict(id=None, kind='宿', aff=False, name='大洗パークホテル', price=21780, fr=1, img=None,
      url='https://hotel.travel.rakuten.co.jp/hotelinfo/plan/6274',
      btn='楽天トラベルで空室を見る', cond='クラブクラシック（26㎡）／1泊2食・2名1室の1名あたり・税込', place='楽天トラベル・じゃらん（https://www.jalan.net/yad338393/）',
      catch='2026年3月にリニューアルした、水族館前の温泉宿',
      desc='アクアワールド茨城県大洗水族館の目の前にある宿で、2026年3月1日にリニューアルしました。客室50室（うちサウナ・ジャグジー付きのスイート7室）とヴィラ10棟があり、大洗温泉の大浴場（露天風呂あり）と男女入れ替え制のサウナがあります。番組で泊まった部屋と食べた料理は確認中です。',
      eat=[], said='なすなかにしと高城れにさんの大洗の旅で登場しました（視聴者の投稿より）。発言の中身は確認中です。',
      specs=[('住所','茨城県東茨城郡大洗町磯浜町8249-10'),('アクセス','水戸大洗ICから車で約15分／大洗鹿島線 大洗駅からタクシー約10分。駐車場無料'),('チェックイン','15:00〜／チェックアウト10:00（プランにより異なる）'),('部屋数','客室50室（うちサウナ・ジャグジー付きスイート7室）、ヴィラ10棟（トラベル Watchの記事による）'),('お風呂','大洗温泉の大浴場（男女各1、露天風呂あり）、サウナ（男女入れ替え制）')],
      tables=[('部屋の広さ',['部屋タイプ','広さ','定員'],[
          ('ツイン','26〜32㎡','確認中'),('クラブクラシック','26㎡','3名'),('オーシャンビュークラブサウナ','33㎡','2名'),('サウナスイート','77㎡','6名')]),
        ('ごはん',['','内容','食べる場所'],[
          ('夕食','地元の食材を使った「和洋特選会席」など（リニューアル記念プランの内容、トラベル Watchの記事による）。番組で食べた料理は確認中','メインダイニング（個室かどうかは確認中）'),
          ('朝食','確認中','確認中')]),
        ('料金の目安（2名1室・1名あたり・1泊2食）',['プラン','部屋','料金'],[
          ('楽天トラベルの最安表示','クラブクラシック','21,780円〜（税込。2026年10月15日確認）'),
          ('リニューアル記念プラン＜和洋特選会席＞','確認中','18,700円〜（トラベル Watchの記事による。税込かどうかと今の料金は確認中）'),
          ('番組で使ったプラン','確認中','確認中')])]),
    S('ののじ「キャベピィMAX」','商品',None,'https://hands.net/goods/4988760012036/','ハンズネットストアで見る',
      'キャベツの千切りが手早くできる、2枚刃のピーラー',
      '三角刃が2mm間隔で2列に並んだステンレス刃のピーラーで、包丁とまな板を使わずにキャベツを千切りにできます。玉ねぎ・大根・にんじんの薄切りにも使えます。切り口が波状になるので、ドレッシングがからみやすいとされています。刃がとても鋭いため、中厚手以上のゴム手袋を使うよう案内されています。冷凍食品・硬い食材・皮むきには使えません。',
      ['揚げ物に添えるキャベツの千切り','コールスロー','玉ねぎスライスのサラダ','大根とにんじんのなます'],
      [('値段','確認中（ハンズでの値段。参考：ミスターマックスオンラインストアでは税込1,428円、2026年10月15日確認）'),('サイズ・重さ','約18×10.6×3cm・約37g'),('材質','刃：ステンレス（420J2）、本体：ポリプロピレン'),('型番','CBP-04G（グリーン）'),('紹介のされ方','ハンズの「キッチン便利グッズ」売上1位（視聴者の投稿より）')],
      'ハンズ店舗・ハンズネットストア、ミスターマックスオンラインストア（https://mrmax.jp/products/detail/83884）ほか', eatlabel='おすすめの使い方',
      said='ハンズのキッチン便利グッズの売上1位として登場しました（視聴者の投稿より）。紹介した出演者と発言の中身は確認中です。'),
    S('ドウシシャ「ゴリラのひとつかみ」GRF-2401','商品',5500,'https://www.ksdenki.com/shop/g/g4550557799958/','ケーズデンキ通販で見る',
      'ふくらはぎに巻いて使う、エアー式の健康家電',
      'ポンプとエアバッグを備えた本体を、面ファスナーでふくらはぎに巻いて使います。電源ボタンで動かし、＋／－ボタンで強さを変えられます。軽くて折りたためるので、しまう場所をとりません。番組で使われたのが上位機種の「スーパーゴリラのひとつかみ」でないかどうかは確認中です。',
      ['テレビを見ながら座って','在宅ワークの休憩中に','使わないときは折りたたんで引き出しに'],
      [('値段','5,500円（税込。ケーズデンキ通販の表示、在庫あり。2026年10月15日確認）'),('サイズ・重さ','約W60×D20×H3cm・約330g（ACアダプター含む）'),('対応するふくらはぎ周囲','約28〜52cm'),('電源','AC100V（専用ACアダプター）'),('型番','GRF-2401GY（グレー）ほか'),('紹介のされ方','ハンズの「ハイパワー健康家電」売上1位（視聴者の投稿より）'),('ハンズでの値段・扱い','確認中')],
      'ケーズデンキ通販ほか（ハンズでの扱いは確認中）', eatlabel='おすすめの使い方', pricenote='税込・ケーズデンキ通販',
      said='ハンズのハイパワー健康家電の売上1位として登場しました（視聴者の投稿より）。体験した出演者と発言の中身は確認中です。'),
   ]),
 dict(slug='20261014-yokohama-hatobus', date=datetime.date(2026,10,14), kind='商品', shop='横浜はとバス・笹塚', theme='ツアー・スイーツ・イタリアン',
   title='【ヒルナンデス】10月14日放送｜日帰り1万円台のはとバスツアーin横浜（クルミッ子・dacō）とはなわさん行きつけの笹塚イタリアンまとめ',
   label='日帰り1万円台のはとバスツアーin横浜と、はなわさん行きつけの笹塚イタリアン', checked='2026年10月14日',
   tochead='紹介された商品・お店一覧',
   ep=[('放送日','2026年10月14日（水）'),('番組','日本テレビ系「ヒルナンデス！」'),
       ('企画','「日帰り1万円台 最新はとバスツアーin横浜」（番組表の予告による）／はなわさんの行きつけの店を当てる企画（企画名は確認中）'),
       ('ロケ','はとバスツアー：ユーキさん・シューヤさん（超特急）、安田美沙子さん、鬼越トマホーク。番組表ではヤーレンズもVTRゲスト（担当した企画は確認中）'),
       ('スタジオ','南原清隆さん、伊藤遼さん（日本テレビアナウンサー）、吉村崇さん、マヂカルラブリー、秋元真夏さん、小倉優子さん、北斗晶さん、ゲスト 髙橋海人さん（King & Prince）、ニシダさん（ラランド）')],
   intro='2026年10月14日（水）放送の「ヒルナンデス！」は、超特急のユーキさん・シューヤさん、安田美沙子さん、鬼越トマホークが日帰り1万円台の最新はとバスツアーで横浜をめぐる企画と、はなわさんの行きつけとして笹塚の予約制イタリアンが登場する企画でした。紹介が確かめられたツアー・お菓子・お店の5件を、値段と買える場所つきでまとめました。',
   notes=[('まだ確認できていないこと',[
       '中華街で食べたフカヒレスープ付き四川料理ランチの店名（はとバスのコースには「横浜中華街 福満園」が入っていますが、放送の店かは未確認）',
       'クルミッ子を買った店と、開店前の行列の場面の場所',
       'ヤーレンズが担当した企画の内容',
       'フィナンシェ クルミッ子、dacō、東京 ITALIAN AKATSUKA の値段',
       '出演者の味の感想（どれも確認が取れていません）'])],
   foot='※紹介されたことは番組表、紹介記事、視聴者の投稿で確かめています。出演者の発言は確認が取れていないため載せていません。値段はお店・販売元の公式の表示で確かめられたものだけを載せ、それ以外は「確認中」としています（2026年10月14日確認）。',
   items=[
    S('はとバス「必見！横浜中華街「変面ショー」と横浜ベイエリア満喫ナンデス！」（R7729・日帰り）','商品',11800,'https://www.hatobus.co.jp/course?searchWords=R7729','はとバス公式サイトで見る',
      '東京駅から出発する、昼食つきの横浜めぐり日帰りバスツアー',
      '東京駅丸の内南口を9:20に出て、横浜ハンマーヘッド、横浜中華街（福満園・関帝廟）、横浜マリンタワー、山下公園、横浜港のミニクルーズ、横浜赤レンガ倉庫を回る日帰りコースです。昼食が1回つき、20名から催行します。放送で回った行程とまったく同じかどうかは確認中です。',
      ['車を出さずに家族や友人と横浜観光','初めての横浜で名所をまとめて回る','中華街の変面ショーを見たいときに'],
      [('値段','大人1名 11,800円（はとバス公式サイトの表示。税込かどうかは確認中。2026年10月14日確認）'),('運行日','2026年10月31日〜12月27日の土・日・祝（11月8・14・15・28日は運休）'),('出発','東京駅丸の内南口 9:20'),('食事','昼食1回つき（朝食・夕食なし）')],
      'はとバス公式サイトで予約', eatlabel='おすすめの使い方', pricenote='大人1名',
      said='超特急のユーキさん・シューヤさん、安田美沙子さん、鬼越トマホークがはとバスツアーで横浜をめぐりました（番組表より）。発言の中身は確認中です。'),
    S('鎌倉紅谷「クルミッ子」5個入','商品',891,'https://www.kamakurabeniya.com/products/kurumicco5','公式通販で見る',
      'くるみとキャラメルを、バター生地ではさんだ焼き菓子',
      '自家製のキャラメルにくるみをたっぷり混ぜ、バターの香る生地で上下からはさんだ、鎌倉紅谷の代表的なお菓子です。はちみつが入っているので、1歳未満の子どもには食べさせないでください。暑いとキャラメルがやわらかくなります。',
      ['手みやげ・おみやげに','コーヒーや紅茶と','横浜散策のおみやげに'],
      [('値段','5個入 891円（税込。公式通販の表示、2026年10月14日確認）'),('在庫','公式通販は「入荷待ち（毎朝9:00入荷）」の表示（2026年10月14日確認）'),('内容量','5個入（箱 120×57×32mm）'),('アレルギー','くるみ・小麦・卵・乳。はちみつ使用'),('賞味期限','約30日（季節で変わります）'),('放送で出た入り数・お店','確認中')],
      '公式通販・鎌倉紅谷の直営店', pricenote='5個入・税込',
      said='スタジオで秋元真夏さんが試食したという視聴者の投稿が複数あります。味の感想は確認中です。'),
    S('鎌倉紅谷「フィナンシェ クルミッ子」','商品',None,'https://news.allabout.co.jp/articles/o/130078/','紹介記事を見る',
      'クルミッ子のキャラメルを合わせた、新しいフィナンシェ',
      'フィナンシェの生地にクルミッ子のキャラメルを合わせて、しっとり焼き上げたお菓子です。発酵バターを焦がして、香りとコクを出しているそうです（報道による）。2026年10月14日に発売されました。',
      ['クルミッ子と食べくらべ','お茶の時間に','ちょっとした手みやげに'],
      [('値段','確認中（報道では1個386円、2種2個入り833円）'),('売っている場所','鎌倉紅谷の直営店舗・イベント（報道による。販売ページは見つかっていません）'),('発売日','2026年10月14日'),('原材料','確認中')],
      '直営店舗・イベント（報道による）',
      said='放送で見たという視聴者の投稿が複数あります。誰が紹介したか、発言の中身は確認中です。'),
    S('dacō（ダコー）横浜ハンマーヘッド「生ナポリドーナツ」','店',None,'https://www.hammerhead.co.jp/shoprestaurant/detail/?cd=000061','お店のページを見る',
      'ピザ窯で生地を焼く、ドーナツのベーカリーカフェ',
      '福岡のベーカリー「AMAM DACOTAN」の別ブランドで、2026年5月16日に横浜ハンマーヘッドの1階に開きました。ピザ窯で焼く「ナポリ」シリーズがあり、生ナポリドーナツは高い温度で焼いた生地にきび糖をまぶしたものです（報道による）。放送で訪れたのがハンマーヘッドの店かどうかは確認中です。',
      ['ハンマーヘッド散策の休憩に','港を見ながらテイクアウトで','カスタード入りなどと食べくらべ'],
      [('場所','横浜市中区新港2-14-1 横浜ハンマーヘッド1F'),('営業','10:00〜21:00（ラストオーダー20:30）、予約不可'),('値段','確認中'),('通販','なし（店頭販売のみ）')],
      '店頭のみ', eatlabel='行くときのコツ',
      said='番組表では、安田美沙子さんが大喜びしたと紹介されています。発言の中身は確認中です。'),
    S('東京 ITALIAN AKATSUKA（アカツカ）笹塚','店',None,'https://restaurant.ikyu.com/121237','予約ページ（一休.com）を見る',
      '和の食材を合わせる、笹塚の予約制イタリアン',
      '京王線笹塚駅から歩いて6分ほどの、和の要素を合わせたイタリアンのお店です。付き合いのある生産者の食材や季節の食材を使っています（一休.comの店舗ページによる）。番組では、紅白歌合戦とレコード大賞に出た「スター」が誰かを当てる形で、はなわさんの行きつけとして紹介されたようです（紹介記事・視聴者の投稿による）。',
      ['記念日のディナーに','少人数での食事会に','ボロネーゼやイカ墨のパスタなど名物の皿を中心に'],
      [('場所','東京都渋谷区笹塚2-22-5 セイワパラシオン104（京王線笹塚駅北口から徒歩6分）'),('営業','12:00〜23:00（最終入店21:00）、月曜と火曜のランチは休み（一休.comの表記。ぐるなびとは時間の表記に差があるため、予約のときに確認を）'),('予約','一休.comでは紹介制で、紹介者がいない初回は直近の空席日だけ予約できると案内。ディナーはコペルト料1,000円（一休.comによる）'),('紹介されたメニュー','ボロネーゼ、野生蝦夷鹿ウチモモ肉のロースト、イカ墨ソースのパスタ、カルパッチョ盛り合わせなど（紹介記事による）'),('値段','確認中')],
      '店内飲食のみ', eatlabel='行くときのコツ',
      said='はなわさんの行きつけとして紹介されました（紹介記事・視聴者の投稿より）。発言の中身は確認中です。'),
   ]),
 dict(slug='20261013-yamanote-harajuku', date=datetime.date(2026,10,13), kind='商品', shop='山手線沿線・料理のプロ', theme='スイーツ・調味料',
   title='【ヒルナンデス】10月13日放送｜「良純と行く山手線沿線散歩」（コロンバン・rico pua）と料理のプロが愛用する麺つゆ・ドレッシング・納豆まとめ',
   label='「良純と行く山手線沿線散歩」と料理のプロが愛用する麺つゆ・ドレッシング・納豆', checked='2026年10月13日',
   tochead='紹介された商品・お店一覧',
   ep=[('放送日','2026年10月13日（火）'),('番組','日本テレビ系「ヒルナンデス！」'),
       ('企画','「良純と行く山手線沿線散歩」（渋谷駅〜代々木駅）／「料理のプロが愛用する麺つゆ・ドレッシング・納豆」'),
       ('ロケ','沿線散歩：石原良純さん、有岡大貴さん（Hey! Say! JUMP）、チョコレートプラネット（長田庄平さん・松尾駿さん）／スーパー「ロピア」での買い物：八乙女光さん、松尾駿さん、杉山愛さん、杉山走さん、和食料理人の野永喜三夫さん'),
       ('スタジオ','南原清隆さん、浦野モモさん（日本テレビアナウンサー）、いとうあさこさん、佐藤栞里さん、八乙女光さん・有岡大貴さん（Hey! Say! JUMP）、チョコレートプラネット、ゲスト 河北麻友子さん')],
   intro='2026年10月13日（火）放送の「ヒルナンデス！」は、石原良純さんたちが山手線沿線を渋谷駅から代々木駅まで歩く「良純と行く山手線沿線散歩」と、和食料理人の野永喜三夫さんら料理のプロが自腹で買う麺つゆ・ドレッシング・納豆を紹介するコーナーでした。紹介が確かめられた商品6品とお店2軒を、値段と買える場所つきでまとめました。',
   notes=[('まだ確認できていないこと',[
       '原宿で一行が訪れたサモエドカフェ、「日本一長い」とされるトルネードポテトの店、カプセルトイの店の名前',
       '予告に出た「プロ棋士も好むキーマカレーの店」が下のrico puaと同じ店かどうか',
       '買い物ロケをしたロピアの店舗名',
       'プレミアムアップルパイ、メロジョイ、rico pua、リケンのノンオイル 青じそ、すごい納豆 S-903 の値段',
       '出演者の味の感想（ほとんど確認が取れていません）'])],
   foot='※紹介されたことは番組表、番組公式の告知（X）、視聴者の投稿、放送内容のまとめサイトで確かめています。出演者の発言は確認が取れたものだけを載せています。値段はお店・メーカー・販売サイトの表示で確かめられたものだけを載せ、それ以外は「確認中」としています（2026年10月13日確認）。',
   items=[
    S('コロンバン「原宿ロール」','商品',1404,'https://www.colombin.co.jp/product/cake/post-40.php','公式商品ページを見る',
      'ざらめ糖を隠し味にした、原宿の老舗洋菓子店のロールケーキ',
      '時間をかけてふんわり焼き上げた生地で、新鮮な牛乳から作る軽くなめらかな生クリームを巻いたロールケーキです。隠し味のざらめ糖が、どこか懐かしい甘さと食感を加えます。売上の一部は認定NPO法人「世界の子どもにワクチンを日本委員会」を通じて寄付される、と公式サイトにあります。',
      ['冷蔵庫でよく冷やしてそのまま','厚めに切ってコーヒーや紅茶と','バニラアイスを添えて'],
      [('値段','1,404円（税込。公式商品ページの表示、2026年10月13日確認）'),('売っている場所','東京駅グランスタ店、原宿スイーツ、原宿サロン、池袋東武、イオン成田、イオン幕張新都心（公式サイトの記載）'),('通販','公式通販での取り扱いは確認できず'),('アレルギー','小麦・卵・乳・大豆（公式サイト）。サイズ・内容量は確認中')],
      '店頭のみ',
      said='一行が原宿のコロンバン（原宿サロン）を訪れ、原宿ロールを試食しました（視聴者の投稿より）。味の感想は確認中です。'),
    S('コロンバン「プレミアムアップルパイ」','商品',None,'https://www.colombin.co.jp/premium-applepie/','公式特設ページを見る',
      '青森県産の紅玉を使った、三層仕立てのアップルパイ',
      '青森県産の紅玉を1台に2個使い、砂糖・バター・レモン果汁・シナモンで煮てから焼き込んだアップルパイです。バターを約80％使ったパイ生地とりんごの間にスポンジ生地をはさみ、カスタードクリームを使わないのが特徴です（公式特設ページ）。',
      ['バニラアイスを添えて（番組でもアイス添えで登場）','軽く温めて','コーヒーや紅茶と'],
      [('値段','確認中'),('お店','コロンバン原宿サロン（東京都渋谷区神宮前6-34-14 原宿表参道ビル1F、月〜土 10:00〜21:00／日祝 10:00〜20:00。公式サイト、2026年10月13日確認）'),('主な材料','紅玉（青森県産）、バター、砂糖、レモン果汁、シナモン、パイ生地、スポンジ生地（公式特設ページ）。サイズ・内容量は確認中'),('ほかの販売店舗・通販','確認中')],
      '原宿サロン（ほかは確認中）',
      said='原宿サロンで、コロンバンの会長とシェフの説明を受けながら、一行がアイス添えのアップルパイを試食しました（視聴者の投稿より）。味の感想は確認中です。'),
    S('MELLOJOY（メロジョイ）原宿ポップアップショップ','店',None,'https://mellojoyjapan.com/','公式通販を見る',
      '食品用シリコーンで手作りした、スクイーズの店',
      '食品グレードのシリコーンで手作りしたスクイーズと、キャラクター「メロイヤ（Melloya）」のトイを扱う期間限定のお店です。2階に飾り付けの展示やフォトブースがあり、購入金額に応じて限定の特典が付きます（FASHIONSNAPの記事より）。',
      ['握って感触を楽しむ','デスクに飾る','ブラインドボックスで集める'],
      [('場所','東京都渋谷区神宮前6-32-1（明治通り沿い）'),('期間','2026年9月9日オープン。終了日・営業時間は確認中'),('値段','確認中（公式通販の例：ブラインドボックス 2,499円、税込かは未記載。2026年10月13日確認）'),('素材','100％フードグレードシリコーン（記事の記載）'),('通販','公式通販あり（一部売り切れの表示あり）')],
      '原宿の店頭・公式通販', eatlabel='おすすめの楽しみ方',
      said='石原良純さんが、スクイーズを握る感触を味噌を揉むことにたとえていました（視聴者の投稿より）。'),
    S('rico pua（リコプア）本店（千駄ヶ谷のスパイスカレー）','店',None,'https://tabelog.com/tokyo/A1309/A130901/13154624/','お店の情報を見る',
      '山椒が効いた、千駄ヶ谷のスパイスカレー店',
      '北参道・千駄ヶ谷エリアにあるスパイスカレーのお店で、日替わりカレーと合わせた2種盛りもあります。放送では山椒ポークカレーが出たとされ、山椒のしびれる刺激が話題になっています。メニューと値段はお店の公式の表示で確認中です。',
      ['山椒ポークカレーを単品で','日替わりとの2種盛りで食べ比べる'],
      [('場所','東京都渋谷区千駄ヶ谷3-8-14 東久パレス神宮 1F'),('営業','月〜土 11:30〜15:00、日祝休み（食べログの記載、2026年10月13日確認）'),('値段','確認中（放送内容のまとめサイトでは山椒ポークカレー 1,050円）')],
      '店内飲食', eatlabel='行くときのコツ',
      said='石原良純さん、有岡大貴さん、チョコレートプラネットの沿線散歩で登場したとされます（放送内容のまとめサイト・視聴者の投稿より）。味の感想は確認中です。'),
    S('理研ビタミン「リケンのノンオイル 青じそ」','商品',None,'https://www.rikenvitamin.jp/products/','メーカーのサイトを見る',
      '国産大葉を使った、ノンオイルの青じそドレッシング',
      'しょうゆと醸造酢をベースに、国産の大葉を100％使った、油を使わないドレッシングです。ほたてエキスやかつお節エキス、梅肉、りんごも入り、さっぱりした中にうまみがあります。大さじ1杯（15g）あたり8kcal（ネットスーパーの商品ページの記載）。',
      ['生野菜のサラダに','冷ややっこやわかめに','肉・魚料理のソースに'],
      [('内容量','190ml（ほかのサイズは確認中）'),('主な原材料','しょうゆ、醸造酢、糖類、発酵調味料、ほたてエキス、梅肉、りんご、かつお節エキス、青じそなど。小麦を含む'),('値段','確認中（参考：ネットスーパー「グリーンビーンズ」で190ml 税込214円、2026年10月13日確認）')],
      'スーパー・ネットスーパー', eatlabel='おすすめの使い方',
      said='和食料理人の野永喜三夫さんが愛用品として挙げたとされ、八乙女光さんも自宅の常備品として挙げていました（視聴者の投稿より）。発言の中身は確認中です。'),
    dict(S('にんべん「つゆの素 ゴールド」（3倍濃厚）500ml','商品',783,'https://hb.afl.rakuten.co.jp/ichiba/584a3b37.2a4108aa.584a3b38.a1b9d8be/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fninben%2Fot475n%2F','楽天市場で見る',
      '鰹節専門店にんべんの、だし素材を増やした3倍濃厚つゆ',
      '本醸造の有機しょうゆに、国内製造のかつお節と北海道産の昆布を合わせた3倍濃厚のめんつゆです。だし素材は同じ会社の「つゆの素」の1.5倍で、上位のシリーズに当たります（楽天市場のにんべん公式ショップの記載）。',
      ['めんのつけ汁（本品1：水2）','かけ汁（1：5〜7）','天つゆ・丼もの（1：2〜3）','肉じゃが（1：4〜5）','おでん（1：12〜14）'],
      [('内容量','500ml（1L、12本ケースもあり）'),('主な原材料','有機しょうゆ（国内製造）、砂糖、かつおぶし、食塩、みりん、酵母エキス、醸造酢、こんぶ。小麦・大豆を含む'),('値段','783円（楽天市場の検索一覧の表示、送料660円別。2026年10月13日確認）'),('セット','白だしゴールドとの各500mlのお試しセットもあり')],
      '楽天市場（にんべん公式ショップ）', eatlabel='おすすめの使い方', pricenote='500ml・送料別',
      said='和食料理人の野永喜三夫さんが愛用品として挙げていました（視聴者の投稿より）。発言の中身は確認中です。'), aff=True),
    S('ミツカン「金のつぶ たれたっぷり！たまご醤油たれ」3パック','商品',128,'https://greenbeans.com/products/14902106012068/details','販売ページを見る',
      'たまご醤油たれが10g付いた、極小粒の納豆',
      '極小粒の納豆に、卵黄を使った「たまご醤油たれ」を10gとたっぷり付けた3パック入りです。卵かけごはんのような味わいが楽しめる、と販売ページにあります。',
      ['ごはんにのせて','うどんやそばにのせて','刻みねぎや海苔を足して'],
      [('内容量','40g×3パック'),('主な原材料','納豆（大豆〈アメリカまたはカナダ〉、納豆菌）、たれ（砂糖混合ぶどう糖果糖液糖、しょうゆ、食塩、卵黄、醸造酢など）。卵・小麦を含む'),('値段','128円（税込。ネットスーパー「グリーンビーンズ」の表示、2026年10月13日確認）')],
      'スーパー・ネットスーパー', pricenote='3パック・税込',
      said='料理のプロが自腹で買った納豆として紹介されました（視聴者の投稿より）。どのプロが選んだか、発言の中身は確認中です。'),
    S('タカノフーズ「すごい納豆 S-903」','商品',None,'https://www.takanofoods.co.jp/products/natto.html','メーカーのサイトを見る',
      'おかめ納豆のタカノフーズの「S-903」納豆',
      'タカノフーズの納豆で、商品名の「S-903」は使っている納豆菌の名前です。内容量や原材料はメーカーの販売ページで確認中です。',
      [],
      [('値段','確認中'),('内容量・原材料','確認中')],
      '確認中',
      said='杉山家と八乙女光さんが買っている納豆として登場しました（視聴者の投稿より）。発言の中身は確認中です。'),
   ]),
 dict(slug='20261012-disney-hakone', date=datetime.date(2026,10,12), kind='店', shop='ディズニー・箱根', theme='パークフード・カフェ',
   title='【ヒルナンデス】10月12日放送｜東京ディズニーランドのハロウィーンと箱根の路線バス旅（RoheN 箱根湯本）で紹介されたグルメまとめ',
   label='東京ディズニーランドのハロウィーンと箱根の路線バス旅', checked='2026年10月12日',
   tochead='紹介されたメニュー・お店一覧',
   ep=[('放送日','2026年10月12日（月）'),('番組','日本テレビ系「ヒルナンデス！」'),
       ('企画','「人気爆発！M!LK塩﨑がディズニーランドで大暴れ！ハロウィン＆秋限定スポットを完全ガイド」／「小峠TAKAHIROが箱根の路線バス旅！ピンポン鳴ったら途中下車の旅」'),
       ('ロケ','ディズニー：塩﨑太智さん（M!LK）、こがけんさん／箱根：小峠英二さん、TAKAHIROさん'),
       ('スタジオ','南原清隆さん、浦野モモさん（日本テレビアナウンサー）、小峠英二さん、コットン、小島奈津子さん、夏菜さん、やす子さん、ゲスト 中村蒼さん、武田創世さん・高岡ミロさん（Lienel）')],
   intro='2026年10月12日（月）放送の「ヒルナンデス！」は、M!LKの塩﨑太智さんとこがけんさんが東京ディズニーランドのハロウィーンと秋限定スポットを案内し、小峠英二さんとTAKAHIROさんが箱根を路線バスでめぐって途中下車する旅でした。紹介が確かめられたパークのデザートと箱根湯本のカフェを、場所と値段つきでまとめました。',
   notes=[('まだ確認できていないこと',[
       '箱根の路線バス旅でほかに立ち寄ったお店',
       'ハロウィーンサンデーのソフトクリームの味（公式メニューはパンプキン、報道記事は紫イモと記載）',
       'RoheN HAKONEYUMOTO のカフェの今の値段と営業時間、箱根での出演者の味の感想'])],
   foot='※紹介されたことは番組表、報道記事、放送内容のまとめサイトで確かめています。値段はお店・パークの公式で確かめられたものだけを確定として載せ、それ以外は「確認中」としています。',
   items=[
    S('東京ディズニーランド「ハロウィーンサンデー（パンプキンソフトクリーム＆チュロス）」','商品',900,'https://www.tokyodisneyresort.jp/tdl/food/detail/17811619281/','公式メニューを見る',
      'ハロウィーン期間だけの、ソフトクリームとチュロスのサンデー',
      '東京ディズニーランドの「ディズニー・ハロウィーン」期間（2026年9月15日〜10月31日予定）だけ売られるデザートです。公式メニューでは、パンプキン味のソフトクリームにチュロスを合わせた一品と案内されています。番組を伝えた報道記事ではソフトクリームを「紫イモ」と書いていて、味の表記は確認中です。',
      ['チュロスをソフトクリームにつけて','溶けやすいので買ってすぐに'],
      [('値段','900円（税込。公式メニューの表示、2026年10月12日確認）'),('売っている場所','アイスクリームコーン、ラケッティのラクーンサルーン（入園が必要）'),('販売期間','2026年9月15日〜10月31日予定（予告なく終了・休止の場合あり、と公式に記載）')],
      'パーク内のみ（入園が必要）',
      said='塩﨑太智さん（M!LK）が試食し、「紫芋そのものを食べてるみたい」と芋の味をほめていました（モデルプレス、THE FIRST TIMESの記事より）。'),
    S('RoheN HAKONEYUMOTO cafe＆bar（箱根湯本）','店',None,'https://www.hakonenavi.jp/feature/6877','お店の紹介ページを見る',
      '小田原のコーヒー豆で淹れるエスプレッソと、枡のティラミス',
      '箱根湯本の宿「RoheN HAKONEYUMOTO」（全22室）の1階にあるカフェです。エスプレッソは小田原の「ひな珈琲」のスペシャルティコーヒーをラ・マルゾッコのマシンで淹れていて、エスプレッソをたっぷり使った「箱根“枡”ティラミス」や、佐賀県嬉野産の茶葉の抹茶ラテと抹茶のテリーヌを合わせた「プレミアム抹茶ラテセット」があります。朝は泊まらない人も使えるハーフビュッフェの朝食、夜はダイニングバーになります。',
      ['箱根湯本の散策の休憩に','抹茶ラテとテリーヌのセットで'],
      [('場所','神奈川県足柄下郡箱根町湯本647（箱根湯本駅から徒歩約7分）'),('営業','モーニング7:30〜10:00、カフェ11:00〜15:00、バー18:00〜22:00、年中無休（箱根ナビの2025年4月30日時点の記載。今の営業時間は確認中）'),('値段','確認中（箱根ナビの2025年4月30日時点の税込表示は、箱根“枡”ティラミス1,000円、プレミアム抹茶ラテセット1,350円）'),('宿の予約','じゃらんの宿ページ（https://www.jalan.net/yad362066/）')],
      '店内飲食', said='小峠英二さんとTAKAHIROさんが箱根の路線バス旅で立ち寄りました（放送内容のまとめサイトより）。味の感想は確認中です。', eatlabel='行くときのコツ'),
   ]),
 dict(slug='20261009-yokohama-shingo', date=datetime.date(2026,10,9), kind='店', shop='横浜', theme='横浜グルメ',
   title='【ヒルナンデス】10月9日放送｜「台本なしんご旅！」横浜（重慶飯店・西遊記・酒槽ほか）のお店・グルメまとめ',
   label='「台本なしんご旅！」横浜の中華街・馬車道・横浜駅西口グルメ', checked='2026年10月9日',
   tochead='紹介されたお店・メニュー一覧',
   ep=[('放送日','2026年10月9日（金）'),('番組','日本テレビ系「ヒルナンデス！」'),('企画','「台本なしんご旅！」（神奈川・横浜）'),
       ('ロケ','村上信五さん、久本雅美さん、羽鳥慎一さん'),
       ('スタジオ','南原清隆さん、伊藤遼さん（日本テレビアナウンサー）、久本雅美さん、陣内智則さん、西尾由佳理さん、タイムマシーン3号、王林さん、ゲスト 伊藤沙莉さん、菅生新樹さん、杢代和人さん')],
   intro='2026年10月9日（金）放送の「ヒルナンデス！」は、村上信五さん・久本雅美さん・羽鳥慎一さんが台本なしで横浜をめぐる「台本なしんご旅！」でした。馬車道のカフェ、中華街の重慶飯店と西遊記、横浜駅西口の魚と日本酒の店など、紹介が確かめられたお店を場所と値段つきでまとめました。',
   notes=[('まだ確認できていないこと',['BASEGATE横浜関内で紹介されたお店とメニュー','各メニューの正式な値段（下の値段は確認できた範囲の参考です）'])],
   foot='※紹介されたことは番組表、番組・お店の公式の告知、視聴者の投稿で確かめています。出演者の発言は確認が取れていないため載せていません。値段はお店の公式で確かめられたものだけを確定として載せ、それ以外は「確認中」としています。',
   items=[
    S('重慶飯店 本館「正宗麻婆豆腐」','店',None,'https://www.jukeihanten.com/menu/5103/','公式サイトで見る',
      '牛ひき肉と熟成豆板醤の、しびれる麻婆豆腐',
      '叩いて挽いた牛肉と、長く熟成させた豆板醤・唐辛子を油でじっくり煮て香りを出した麻婆豆腐です。しびれと辛さのあとに濃いうま味が続く味で、もとは本館の裏メニューだったものが常連に広まり、今は本館と新館で食べられます。',
      ['白いごはんと一緒に','炒飯にかけて（常連の食べ方）'],
      [('場所','横浜市中区山下町164（元町・中華街駅2番出口から徒歩約3分）'),('金曜の営業','ランチ11:30〜15:30（L.O.14:30）、ディナー17:00〜22:00'),('値段','確認中（公式メニューの「マーボー豆腐」は2,600円・税サ込）')],
      '店内飲食', said='村上信五さん、久本雅美さん、羽鳥慎一さんが訪れました（横浜中華街の公式の告知・番組表より）。', eatlabel='おすすめの食べ方'),
    dict(S('重慶飯店「麻婆豆腐醤」5個セット（家で作れる麻婆豆腐の素）','商品',2430,'https://hb.afl.rakuten.co.jp/ichiba/584a3b37.2a4108aa.584a3b38.a1b9d8be/?pc=https%3A%2F%2Fitem.rakuten.co.jp%2Fjukeihanten%2F3211019%2F','楽天市場で見る','重慶飯店の味を家で。豆腐を足してレンジで作る素','放送で出た麻婆豆腐そのものではありませんが、重慶飯店が出している麻婆豆腐の素です。豆腐一丁を足して電子レンジで作れて、山椒のしびれと唐辛子の辛さがあります。お店の正宗麻婆豆腐は牛肉を使いますが、この素は豚肉入りなので、まったく同じ味ではありません。',['豆腐一丁を足してレンジで','茄子の炒め物に','炒飯に'],[('内容量','130g（3〜4人前）×5個'),('賞味期限','常温で2年'),('価格','期間限定のセール価格（定価2,970円）。10月9日確認')],'楽天市場（重慶飯店の公式ショップ）'), aff=True),
    S('香港飲茶専門店 西遊記「チャーシューメロンパン」','商品',600,'https://saiyuki.co.jp/','お店のサイトを見る',
      '甘いさくさく生地で、叉焼あんを包んだ香港式パン',
      'メロンパンのような甘くさくさくした生地で、とろりと煮込んだ叉焼のあんを包んで焼いた点心です。店内で生地から手作りし、1階の入口で焼きたてを売っています。中華街の食べ歩きにぴったりです。',
      ['焼きたてを食べ歩きで','持ち帰って家で'],
      [('値段','2個 600円（グルメサイトの表示。店頭の今の値段は確認中）'),('お店','横浜市中区山下町149-1-4（10:00〜22:00、定休日なし）'),('通販','なし（店頭販売のみ）')],
      '中華街の店頭のみ', said='3人の中華街ロケで登場しました（横浜中華街の公式の告知・視聴者の投稿より）。', pricenote='2個・税込'),
    S('CRAFT.（馬車道・BankPark YOKOHAMA）','店',None,'https://co-trip.jp/article/713553','お店の紹介記事を見る',
      '昭和初期の銀行建築を使った、天井の高いカフェ',
      '旧第一銀行横浜支店（横浜市認定歴史的建造物）を使ったカフェで、2層吹き抜けの高い天井と8本の円柱、アーチ型の大きな窓が特徴です。工芸品のセレクトショップやギャラリーも同じ建物に入っています。',
      ['馬車道散歩の休憩に','スコーンとお茶のセットで'],
      [('場所','横浜市中区本町6-50-1 BankPark YOKOHAMA 1F'),('営業','11:00〜19:00（金・土は22:00まで）'),('メニュー','あんバタースコーンティーセット ほか（値段は確認中）')],
      '店内飲食', said='村上信五さん、久本雅美さん、羽鳥慎一さんが訪れました。', eatlabel='行くときのコツ'),
    S('日本酒・魚料理 横浜 酒槽（GEMS横浜）','店',None,'https://www.gems-portal.com/yokohama/shop/sakafune.html','お店のページを見る',
      '生簀の魚と日本酒の、横浜駅西口の店',
      '生簀の活魚、炉端焼き、土鍋の炊き込みごはんに、全国の蔵元の日本酒を合わせるお店です。放送では、かわはぎの活け造りや、いくらの土鍋御飯が登場しました。個室は最大12名まで使えます。',
      ['魚に日本酒を合わせる夜の食事に','個室での集まりに（最大12名）'],
      [('場所','横浜市西区北幸2-6-5 GEMS横浜 5F（横浜駅から徒歩3分）'),('営業','夜のみ（時間は店舗ページで確認）'),('値段','確認中（平均予算6,000円〜）'),('注意','活かわはぎは仕入れにより品切れのことがあります')],
      '店内飲食（夜のみ）', said='3人の横浜ロケで登場しました（番組表に店名）。', eatlabel='行くときのコツ'),
   ]),
 dict(slug='20261008-ginza-gusto-jollypasta', date=datetime.date(2026,10,8), kind='店', shop='銀座・ファミレス', theme='和菓子・グルメ',
   title='【ヒルナンデス】10月8日放送｜銀座「ゆのちゃんのはじめて旅」とガスト×ジョリーパスタ「2000円以内最強フルコース」のお店・和菓子まとめ',
   label='銀座「ゆのちゃんのはじめて旅」とガスト×ジョリーパスタのフルコース対決', checked='2026年10月8日',
   tochead='紹介されたお店・メニュー一覧',
   ep=[('放送日','2026年10月8日（木）'),('番組','日本テレビ系「ヒルナンデス！」'),
       ('企画','「ゆのちゃんのはじめて旅」（銀座）／「店員VS有名シェフ2000円以内最強フルコース」（ガスト、ジョリーパスタ）'),
       ('ロケ','銀座：横山裕さん、榊原郁恵さん、永尾柚乃さん／フルコース対決：木村昴さん、ニッチェ、桝谷周一郎シェフ'),
       ('スタジオ','南原清隆さん、浦野モモさん、横山裕さん（SUPER EIGHT）、生見愛瑠さん、木村昴さん、大沢あかねさん、榊原郁恵さん、ゲスト ROIROM（本多大夢さん、浜川路己さん）')],
   intro='2026年10月8日（木）放送の「ヒルナンデス！」は、横山裕さん・榊原郁恵さん・永尾柚乃さんが銀座をめぐる「ゆのちゃんのはじめて旅」と、ガストとジョリーパスタのメニューを2000円以内で組む「店員VS有名シェフ2000円以内最強フルコース」でした。紹介が確かめられたお店・和菓子・メニューを、場所や値段と一緒にまとめました。',
   notes=[('まだ確認できていないこと',[
       '寿司の握り体験をした学校の名前（番組や学校の公式の発表が見つかっていません）',
       'フルコース対決で選ばれた全メニュー、合計金額、勝敗',
       '萬年堂本店で出たわらび餅の名前と値段'])],
   foot='※紹介されたことは番組公式の告知（X）、番組表、各お店の公式サイトで確かめています。出演者の発言は確認が取れていないため載せていません。確認できたものから順に追記します。',
   items=[
    S('銀座 萬年堂本店「御目出糖（おめでとう）」 普通箱 6個入り','商品',1858,'https://ginmannendou.shop24.makeshop.jp/shopdetail/000000000001/ct7/page1/price/','公式通販で見る',
      '赤飯に見立てた、銀座のお祝い菓子',
      'こしあんに餅粉などの米粉を混ぜてそぼろ状にし、蜜漬けの大納言小豆を散らして蒸し上げた和菓子です。元禄のころから伝わる菓子を赤飯に見立てたもので、もちもちした食感が特徴。日持ちは発送日から5日なので、お祝いの手土産向きです。',
      ['蒸し器で約1分温め直す','電子レンジで約15秒温め直す','お祝いの手土産に'],
      [('内容量','6個入り（店頭では1個から買えます）'),('日持ち','発送日から5日'),('お店','銀座 萬年堂本店（東京都中央区銀座7-13-21）'),('送料','公式通販は935円〜')],
      '公式通販・銀座の店頭',
      said='横山裕さん、榊原郁恵さん、永尾柚乃さんがお店を訪れました。番組公式は放送後、萬年堂の「金平糖入り巾着袋」を5名にプレゼントすると告知しています（応募は番組公式Xから）。'),
    S('馬菜 BASAI 銀座本店「馬肉大トロ重」','店',2530,'https://basai-ginza.com/lunch/','公式ランチメニューを見る',
      '平日ランチ限定の、馬肉のお重',
      '銀座3丁目の馬肉料理店の平日ランチ限定メニューで、サラダ・香物・お椀が付きます。数に限りがあり、品薄のときは出せない日もあるそうです。お店で食べるだけで、通販はありません。',
      ['平日の11:00〜14:30に行く','ネット予約で席を取る'],
      [('場所','東京都中央区銀座3-9-4 草野ビルディング B1F（東銀座駅A2出口から徒歩2分）'),('ランチ','11:00〜15:00（ラストオーダー14:30）、無休'),('内容','馬肉大トロ重、サラダ、香物、お椀'),('予約','ネット予約あり（お店の公式サイトから）')],
      '店内飲食のみ（平日ランチ限定）', said='横山裕さん、榊原郁恵さん、永尾柚乃さんが試食しました。', eatlabel='行くときのコツ'),
    S('ガスト「焼き野菜と月見チーズINハンバーグ～きのこデミソース～」','店',1044,'https://www.skylark.co.jp/gusto/menu/fair3/index.html','公式メニューを見る',
      '温泉卵をのせた、チーズ入りハンバーグ',
      '12種類のチーズを包んだハンバーグに温泉卵をのせ、しめじ入りのデミグラスソースを合わせた一皿です。かぼちゃ、れんこん、パプリカの焼き野菜付き。秋のフェアのメニューで、10月21日までの期間限定です。',
      ['温泉卵をくずしてデミソースとからめる','焼き野菜をソースにつけて'],
      [('価格','税込1,044円〜1,154円（お店によって違います。22時〜5時は深夜料金）'),('販売期間','10月21日まで（10:30から）'),('主な食材','12種のチーズ、温泉卵、しめじ、かぼちゃ、れんこん、パプリカ')],
      '全国のガスト', fr=1,
      said='「店員VS有名シェフ2000円以内最強フルコース」に登場。有名シェフはイタリアンの桝谷周一郎さんです（番組公式の告知より）。'),
    S('ジョリーパスタ（秋冬の新メニュー）','店',None,'https://www.jolly-pasta.co.jp/menu/','公式メニューを見る',
      '10月から秋冬メニューのパスタ専門店',
      '同じフルコース対決に登場したパスタ専門店です。10月6日から秋冬のグランドメニューに変わり、牛肉100％の粗挽き肉を使うボロネーゼや、スモークサーモン・舞茸・ルッコラのペペロンチーノが加わりました。番組で選ばれたメニューは確認中です。',
      [],
      [('参考価格','感動ボロネーゼ ～ゴロゴロ牛肉～ 1,309円／感動ペペロンチーノ ～スモークサーモンとルッコラ～ 1,199円／イカスミのアランチーニ 495円（すべて税込）')],
      '全国のジョリーパスタ'),
   ]),
 dict(slug='20261005-ikaho-omori', date=datetime.date(2026,10,5), kind='宿', shop='伊香保温泉', theme='宿',
   title='【ヒルナンデス】10月5日放送｜伊香保温泉で登場した宿「和心の宿 大森」部屋の広さ・ごはん・料金まとめ',
   label='伊香保温泉の宿「和心の宿 大森」', checked='2026年10月8日',
   ep=[('放送日','2026年10月5日（月）'),('番組','日本テレビ系「ヒルナンデス！」'),('企画','伊香保温泉の女将に「メディア初出しグルメ」を聞く旅'),('出演','髙地優吾さん（SixTONES）、柳沢慎吾さん'),('ロケ地','群馬県・伊香保温泉')],
   intro='2026年10月5日（月）放送の「ヒルナンデス！」は、髙地優吾さんと柳沢慎吾さんが伊香保温泉へ。温泉宿の女将に、まだテレビに出ていないグルメを聞いて回る企画でした。この回に登場した宿「和心の宿 大森」について、泊まるときに気になる部屋の広さ、ごはん、料金をまとめました。',
   foot='※女将が紹介したグルメのお店は、確認が取れしだい追記します。料金は2026年7月1日〜2027年3月31日宿泊分のプランを2026年10月8日に確認したものです。日によって変わるため、予約ページで最新の料金をご確認ください。',
   deal=dict(title='お得に予約するには', url='https://hb.afl.rakuten.co.jp/hgc/584eca7f.b482ba06.584eca80.649f3027/?pc=https%3A%2F%2Ftravel.rakuten.co.jp%2Fcamp%2F50luxday%2Ftop%2F&link_type=text&ut=eyJwYWdlIjoidXJsIiwidHlwZSI6InRleHQiLCJjb2wiOjF9', btn='5と0のつく日のクーポンを見る',
     text='楽天トラベルでは、毎月5と0のつく日（5日・10日・15日・20日・25日・30日）に、国内の宿が最大20％OFFになるクーポンが配られます。予約の前にクーポンを獲得しておくと、同じ宿・同じプランでもその分安く泊まれます。',
     note='この宿が対象かどうかと、割引の条件はキャンペーンページでご確認ください（2026年10月8日確認）。'),
   items=[OMORI]),
 dict(slug='20250919-akomeya-tokyo', date=datetime.date(2025,9,19), kind='商品', shop='AKOMEYA TOKYO', theme='ごはんのお供・調味料',
   title='【ヒルナンデス】9月19日放送｜AKOMEYA TOKYOのふりかけ・ごはんのお供 16品まとめ',
   label='AKOMEYA TOKYOのふりかけ・ごはんのお供 16品', checked='2026年10月8日',
   ep=[('放送日','2025年9月19日（金）'),('番組','日本テレビ系「ヒルナンデス！」'),('企画','「AKOMEYAで進化するふりかけ＆ご飯のお供を調査」'),('紹介されたお店','AKOMEYA TOKYO（お米を中心に、ごはんのお供や調味料をそろえるお店）')],
   intro='2025年9月19日（金）放送の「ヒルナンデス！」は、AKOMEYA TOKYOで「進化するふりかけ＆ご飯のお供」を調べる企画でした。番組で紹介された商品のうち、お店の公式ショップで今も買える16品を、どんな味か・どう食べるとおいしいかまで1品ずつまとめました。新米の季節に、気になるものから試してみてください。',
   foot='※この回は放送から時間がたっているため、出演者の試食コメントは確認が取れたものだけを載せています。',
   items=AK),
]

import json as _json
LISTJS = '''<script>
(function(){
  var SHOPS=__SHOPS__, KEY='hirumemo-list', L=[], seen={};
  try{ L=JSON.parse(localStorage.getItem(KEY)||'[]')||[]; }catch(e){ L=[]; }
  function save(){ try{ localStorage.setItem(KEY,JSON.stringify(L)); }catch(e){} }
  function yen(n){ return Number(n).toLocaleString('ja-JP')+'円'; }
  function has(id){ return L.some(function(x){return x.id===id}); }
  function esc(s){ var d=document.createElement('div'); d.textContent=s; return d.innerHTML; }
  var bar=document.createElement('div'); bar.className='cartbar'; bar.hidden=true;
  var panel=document.createElement('div'); panel.className='cartpanel'; panel.hidden=true;
  document.body.appendChild(bar); document.body.appendChild(panel);
  function draw(){
    Array.prototype.forEach.call(document.querySelectorAll('.add'),function(b){
      var on=has(b.dataset.id); b.setAttribute('aria-pressed',String(on)); b.textContent=on?'✓ リストに入れました':'＋ まとめ買いリストへ';
    });
    var total=L.reduce(function(a,x){return a+Number(x.price)},0);
    bar.hidden=L.length===0; document.body.classList.toggle('hascart',L.length>0);
    bar.innerHTML='<span>まとめ買いリスト <b>'+L.length+'品</b>　合計 <b>'+yen(total)+'</b><small>（税込・送料別）</small></span><button class="btn" type="button" data-act="open">リストを見て買う</button>';
    if(L.length===0){ panel.hidden=true; return; }
    var shops={}; L.forEach(function(x){ (shops[x.shop]=shops[x.shop]||[]).push(x); });
    var h='<div class="cartsheet" role="dialog" aria-label="まとめ買いリスト"><div class="carthead"><h2>まとめ買いリスト</h2><button class="btn ghost" type="button" data-act="close">とじる</button></div>';
    Object.keys(shops).forEach(function(k){
      var s=SHOPS[k]||{label:k};
      h+='<p><b>'+esc(s.label)+'</b>の商品です。上から順に「楽天市場で見る」を押して買い物かごに入れていくと、1回の注文にまとめられます。</p>'+(s.ship?'<p class="note">'+esc(s.ship)+'</p>':'')+'<ul class="cartlist">';
      shops[k].forEach(function(x){
        h+='<li><img src="'+esc(x.img)+'" alt="" width="64" height="64" loading="lazy"><div><div class="nm">'+esc(x.name)+'</div><div class="pr2">'+yen(x.price)+'（税込）</div></div><div class="ops"><a class="btn" href="'+esc(x.url)+'" target="_blank" rel="nofollow sponsored noopener" data-seen="'+esc(x.id)+'">楽天市場で見る</a>'+(seen[x.id]?'<span class="seen">✓ 開きました</span>':'')+'<button class="x" type="button" data-rm="'+esc(x.id)+'">リストから外す</button></div></li>';
      });
      h+='</ul>'+(s.url?'<div><a class="btn ghost" href="'+esc(s.url)+'" target="_blank" rel="nofollow sponsored noopener">お店の紹介商品ページでまとめて選ぶ</a></div>':'');
    });
    h+='<div class="carttotal"><span>合計（'+L.length+'品）</span><span>'+yen(total)+'<small>（税込・送料別）</small></span></div><p class="note">価格は確認時点のものです。最新の価格と送料は楽天市場の注文画面でご確認ください。</p></div>';
    panel.innerHTML=h;
  }
  document.addEventListener('click',function(ev){
    var t=ev.target, b=t.closest('.add');
    if(b){ var id=b.dataset.id; if(has(id)) L=L.filter(function(x){return x.id!==id}); else L.push({id:id,shop:b.dataset.shop,name:b.dataset.name,price:Number(b.dataset.price),url:b.dataset.url,img:b.dataset.img}); save(); draw(); return; }
    if(t.closest('[data-act="open"]')){ panel.hidden=false; return; }
    if(t.closest('[data-act="close"]')||t===panel){ panel.hidden=true; return; }
    var r=t.closest('[data-rm]'); if(r){ L=L.filter(function(x){return x.id!==r.dataset.rm}); save(); draw(); return; }
    var s=t.closest('[data-seen]'); if(s){ seen[s.dataset.seen]=1; setTimeout(draw,300); }
  });
  document.addEventListener('keydown',function(ev){ if(ev.key==='Escape') panel.hidden=true; });
  draw();
})();
</script>'''.replace('__SHOPS__', _json.dumps(SHOPS, ensure_ascii=False))
DEALJS = """<script>
(function(){
  var els=document.querySelectorAll('.d50'); if(!els.length) return;
  var w='日月火水木金土', d=new Date(), t='';
  for(var i=0;i<32;i++){ var x=new Date(d.getFullYear(),d.getMonth(),d.getDate()+i); if(x.getDate()%5===0){ t=i===0?'今日がその日です。':'次は'+(x.getMonth()+1)+'月'+x.getDate()+'日（'+w[x.getDay()]+'）です。'; break; } }
  Array.prototype.forEach.call(els,function(e){ e.textContent=t; });
})();
</script>"""
def page(path, title, desc, body, current='', script='', image='', kind='website', pub=''):
    script = script + LISTJS + (DEALJS if 'class="d50"' in body else '')
    desc = cutdesc(desc)
    url = BASE + ('' if path=='index.html' else path)
    ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA_ID}");document.addEventListener("click",function(ev){{var a=ev.target.closest&&ev.target.closest("a[href*=\\"rakuten.co.jp\\"]");if(a)gtag("event","affiliate_click",{{link_url:a.href,link_text:(a.textContent||"").trim().slice(0,80)}});}});</script>') if GA_ID else ''
    extra = (f'<meta property="og:image" content="{e(image)}">\n<meta name="twitter:image" content="{e(image)}">\n' if image else '') + (f'<meta property="article:published_time" content="{pub}">\n<meta property="article:modified_time" content="{TODAY}">\n' if pub else '')
    nav = ''.join(f'<a href="{h}"{" aria-current=\"page\"" if current==k else ""}>{t}</a>' for k,h,t in [('home','./','さがす'),('list','./#kai','放送回まとめ'),('about','about.html','サイトについて')])
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{BASE}{'' if path=='index.html' else path}">
<meta property="og:type" content="{kind}">
<meta property="og:site_name" content="ひるメモ">
<meta property="og:locale" content="ja_JP">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="{'summary_large_image' if image else 'summary'}">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
{extra}<meta name="msvalidate.01" content="BED3DDA80BBB9FC04817B4096368D5E1">
<meta name="theme-color" content="#f6a700">
<link rel="icon" href="{FAV}">
<link rel="alternate" type="application/rss+xml" title="ひるメモ 新着" href="{BASE}feed.xml">
{ga}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zen+Maru+Gothic:wght@700;900&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap">
<style>html{{color-scheme:light}}body{{margin:0}}img{{max-width:100%}}{CSS}</style>
</head>
<body>
<header class="mast"><div class="mast-in">
<a class="brand" href="./"><div class="sun" aria-hidden="true"></div><div><b>ひるメモ</b><br><span>お昼のテレビで紹介されたもの、ぜんぶメモ。</span></div></a>
<nav class="navlinks" aria-label="メニュー">{nav}</nav>
</div></header>
<div class="wrap">
{body}
<footer><p class="prnote">※本サイトにはアフィリエイト広告（PR）が含まれます。</p>当サイトは番組・放送局とは関係のない非公式サイトです。価格・在庫・空室は確認時点の情報です。最新の情報は各販売ページ・予約ページでご確認ください。<br><a href="about.html">このサイトについて</a>　<a href="https://developers.rakuten.com/" target="_blank" rel="noopener">Supported by Rakuten Developers</a></footer>
</div>
{script}
</body>
</html>
'''
A = 'target="_blank" rel="nofollow sponsored noopener"'
def photo(it, kind=None, lazy=True, src=None, land=False, what='の写真'):
    k = f'<span class="kind">{e(kind)}</span>' if kind else ''
    lz = ' loading="lazy"' if lazy else ''
    if it.get('credit') and it['img']:
        return f'<a class="ph cover{" land" if land else ""}" href="{e(it["url"])}" {A}><img src="{e(src or it["img"])}"{lz} alt="{e(it["name"])}{what}"><span class="credit">写真：{e(it["credit"])}</span>{k}</a>'
    if it['img']:
        return f'<a class="ph" href="{e(it["url"])}" {A}><img src="{e(it["img"])}" width="400" height="400"{lz} alt="{e(it["name"])}の商品写真" title="{e(NOTE)}">{k}</a>'
    if not it.get('aff', True):
        return f'<a class="ph none" href="{e(it["url"])}" {AN}><span>{DISH}写真はお店の<br>ページで見られます</span>{k}</a>'
    return f'<a class="ph none" href="{e(it["url"])}" {A}><span>{ONSEN}写真は予約ページで<br>見られます</span>{k}</a>'
def photos(it):
    if it.get('img2'):
        return '<div class="phs">'+photo(it, land=True, what='の外観')+photo(it, src=it['img2'], what='の客室')+'</div>'
    return photo(it) if it['img'] else ''

def cardflag(it, slug, k):
    code=it.get('id'); out=''
    if not code: return ''
    offs=OFFERS.get(code,[]); others=[o for o in offs if o[2] is not None]
    if code in SOLDOUT: out+='<span class="mark gone">紹介されたお店は在庫切れ（10/8）</span>'
    if others:
        lo=min(o[0] for o in others)
        if lo<it['price'] or code in SOLDOUT: out+=f'<a class="mark alt" href="{slug}.html#i{k+1}">ほかのお店なら{yen(lo)}〜</a>'
    return out
# ---- index
cards=[]; total=0
for b in sorted(B, key=lambda x:x['date'], reverse=True):
    for k,it in enumerate(b['items']):
        total+=1
        text=' '.join([it['name'],b['shop'],b['theme'],it['catch'],it['desc'],' '.join(it['eat'])]).lower()
        kd=it.get('kind',b['kind'])
        cards.append(f'''<li class="card" data-kind="{e(kd)}" data-shop="{e(b['shop'])}" data-date="{b['date'].isoformat()}" data-price="{it['price'] or 0}" data-text="{e(text)}">
{photo(it, kd, lazy=total>4)}
<div class="card-b"><div class="ep">{dlong(b['date'])}放送｜{e(b['shop'])}</div>
<div class="name"><a href="{b['slug']}.html#i{k+1}">{e(it['name'])}</a></div>
<p class="catch">{e(it['catch'])}</p>
{cardflag(it, b['slug'], k)}
<div class="price">{yen(it['price'],it['fr'])}<small>{('' if it['price'] is None else it.get('pricenote','税込')) if it['cond']=='税込' else '1名・1泊2食・税込'}</small></div>
<a class="btn" href="{e(it['url'])}" {ra(it)}>{e(it['btn'])}</a>
{addbtn(it, b['shop'])}
<a class="more" href="{b['slug']}.html#i{k+1}">くわしく見る</a></div>
</li>''')
kinds = sorted({it.get('kind',b['kind']) for b in B for it in b['items']}); shops=[b['shop'] for b in sorted(B,key=lambda x:x['date'],reverse=True) if b['items']]
chips = lambda key, vals: '<button class="chip" data-f="%s" data-v="" aria-pressed="true">すべて</button>'%key + ''.join(f'<button class="chip" data-f="{key}" data-v="{e(v)}" aria-pressed="false">{e(v)}</button>' for v in vals)
blist = ''.join(f'<li><a href="{b["slug"]}.html">{dlong(b["date"])}放送｜{e(b["label"])}{'' if b['items'] else '（随時更新）'}<small>{e(dict(b["ep"]).get("企画",""))}　確認日：{e(b["checked"])}</small></a></li>' for b in sorted(B,key=lambda x:x['date'],reverse=True))
index_body = f'''<main style="display:flex;flex-direction:column;gap:16px">
<h1>ヒルナンデスで紹介された商品・宿をさがす</h1>
<p class="lead">どの放送回で紹介されたか、どんな味か、宿なら部屋の広さやごはんまで。価格は販売ページで確かめたものだけを載せています。気になる商品は「まとめ買いリスト」に入れると、合計を見ながらまとめて買えます。</p>
<div class="tools">
<input class="search" id="q" type="search" placeholder="商品名・お店・食べ方でさがす（例：ふりかけ、卵かけ）" aria-label="キーワードでさがす">
<div class="frow"><span class="flabel">種類</span>{chips('kind',kinds)}</div>
<div class="frow"><span class="flabel">お店・場所</span>{chips('shop',shops)}</div>
<div class="bar"><div class="count" id="count" aria-live="polite">{total}件 <small>全{total}件・{len([b for b in B if b['items']])}放送回</small></div>
<select class="sort" id="sort" aria-label="並び順"><option value="new">放送日が新しい順</option><option value="low">価格が安い順</option><option value="high">価格が高い順</option></select></div>
</div>
<ul class="cards" id="list">
{chr(10).join(cards)}
</ul>
<div class="empty" id="empty" hidden><div>条件に合うものがありません。しぼり込みを減らしてください。</div><button class="btn ghost" id="reset">条件をすべて外す</button></div>
<h2 id="kai">放送回まとめ</h2>
<ul class="blist">{blist}</ul>
</main>'''
index_js = '''<script>
(function(){
  var list=document.getElementById('list'), items=Array.prototype.slice.call(list.children);
  items.forEach(function(li,i){ li.dataset.i=i; });
  var st={q:'',kind:'',shop:'',sort:'new'};
  function render(){
    var q=st.q.trim().toLowerCase(), n=0;
    items.forEach(function(li){
      var ok=(!st.kind||li.dataset.kind===st.kind)&&(!st.shop||li.dataset.shop===st.shop)&&(!q||li.dataset.text.indexOf(q)>=0);
      li.hidden=!ok; if(ok) n++;
    });
    var s=items.slice().sort(function(a,b){
      if(st.sort==='new') return a.dataset.i-b.dataset.i;
      return st.sort==='low' ? a.dataset.price-b.dataset.price : b.dataset.price-a.dataset.price;
    });
    s.forEach(function(li){ list.appendChild(li); });
    document.getElementById('count').firstChild.nodeValue=n+'件 ';
    list.hidden=n===0; document.getElementById('empty').hidden=n!==0;
    Array.prototype.forEach.call(document.querySelectorAll('.chip'),function(c){ c.setAttribute('aria-pressed',String(st[c.dataset.f]===c.dataset.v)); });
  }
  document.addEventListener('click',function(ev){ var c=ev.target.closest('.chip'); if(!c) return; st[c.dataset.f]=c.dataset.v; render(); });
  document.getElementById('q').addEventListener('input',function(){ st.q=this.value; render(); });
  document.getElementById('sort').addEventListener('change',function(){ st.sort=this.value; render(); });
  document.getElementById('reset').addEventListener('click',function(){ st.q='';st.kind='';st.shop=''; document.getElementById('q').value=''; render(); });
})();
</script>'''
out = pathlib.Path('site'); out.mkdir(exist_ok=True)
(out/'index.html').write_text(page('index.html','ひるメモ｜ヒルナンデスで紹介された商品・宿まとめ','「ヒルナンデス！」で紹介された商品や宿を、放送回・お店・種類でさがせる非公式のまとめサイトです。どんな味か、宿の部屋の広さやごはんまで、販売ページで確認して掲載しています。',index_body+'<script type="application/ld+json">'+_json.dumps({'@context':'https://schema.org','@graph':[{'@type':'WebSite','name':'ひるメモ','url':BASE,'inLanguage':'ja'},{'@type':'Organization','name':'ひるメモ','url':BASE},{'@type':'ItemList','name':'放送回まとめ','itemListElement':[{'@type':'ListItem','position':k+1,'url':BASE+b['slug']+'.html','name':b['title']} for k,b in enumerate(sorted(B,key=lambda x:x['date'],reverse=True))]}]},ensure_ascii=False)+'</script>','home',index_js,image=next((it['img'] for b in sorted(B,key=lambda x:x['date'],reverse=True) for it in b['items'] if it.get('img')),'')),encoding='utf-8')

# ---- broadcast pages
def kv(pairs): return '<dl class="kv">'+''.join(f'<dt>{e(k)}</dt><dd>{e(v)}</dd>' for k,v in pairs)+'</dl>'
def tbl(head, rows): return '<div class="tbl"><table><thead><tr>'+''.join(f'<th>{e(h)}</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{e(c)}</td>' for c in r)+'</tr>' for r in rows)+'</tbody></table></div>'
for b in B:
    n=len(b['items']); t=b['title']
    blocks=[]
    for k,it in enumerate(b['items']):
        eat = f'<div class="eat"><b>{e(it.get("eatlabel","おすすめの食べ方"))}</b>'+''.join(f'<span>{e(x)}</span>' for x in it['eat'])+'</div>' if it['eat'] else ''
        said = f'<div class="said">{e(it["said"])}</div>' if it.get('said') else ''
        tables = ''.join(f'<div class="sub">{e(h)}</div>{tbl(hd,rows)}' for h,hd,rows in it.get('tables',[]))
        price_k = '価格' if it['cond']=='税込' else '料金の目安'
        price_v = ('確認中' if it['price'] is None else f'税込{yen(it["price"],it["fr"])}') if it['cond']=='税込' else f'{yen(it["price"],it["fr"])}（{it["cond"]}）'
        blocks.append(f'''<section class="block{'' if it['img'] else ' nophoto'}" id="i{k+1}">{photos(it)}
<div class="block-b"><h3>{e(it['name'])}</h3>
<p class="catch">{e(it['catch'])}</p>
<p>{e(it['desc'])}</p>
{eat}{said}
{kv(it['specs']+[(price_k,price_v),(it.get('placelabel') or ('買える場所' if it['cond']=='税込' else '予約できる場所'),it['place'])])}
{tables}
{cmpbox(it)}
<div class="buyrow"><a class="btn big" href="{e(it['url'])}" {ra(it)}>{e(it['btn'])}</a>{addbtn(it, b['shop'])}<span class="price">{yen(it['price'],it['fr'])}<small>{('' if it['price'] is None else it.get('pricenote','税込')) if it['cond']=='税込' else '1名・1泊2食・税込'}</small></span></div></div></section>''')
    toc = ''
    if n>1:
        trs=''.join(f'<tr><td><a href="#i{k+1}">{e(it["name"])}</a></td><td>{e(it["catch"])}</td><td class="num">{yen(it["price"],it["fr"])}</td></tr>' for k,it in enumerate(b['items']))
        tochead = b.get('tochead','紹介された商品一覧')
        toc = f'<h2>{e(tochead)}</h2><div class="tbl"><table><thead><tr><th>名前</th><th>ひとことで言うと</th><th>価格（税込）</th></tr></thead><tbody>{trs}</tbody></table></div>'
    body=f'''<main style="display:flex;flex-direction:column;gap:16px">
<div class="crumbs"><a href="./">ひるメモ</a> ＞ 放送回まとめ</div>
<article class="article">
<h1>{e(t)}</h1>
<div class="epbox"><h2>この放送回について</h2>{kv(b['ep'])}</div>
<p>{e(b['intro'])}</p>
<p class="note">最終更新：{e(b['checked'])}。価格は同日に販売ページ・予約ページで確認したものです。</p>
{''.join('<h2>'+e(h)+'</h2><ul class="kotsu">'+''.join('<li>'+e(x)+'</li>' for x in xs)+'</ul>' for h,xs in b.get('notes',[]))}
{bulkbox(b)}
{toc}
{''.join(blocks)}
<p class="note">{e(b['foot'])}</p>
<p class="note">※価格・在庫・空室は{e(b['checked'])}時点の情報です。最新の情報は各ページでご確認ください。</p>
</article></main>'''
    ld = {'@context':'https://schema.org','@graph':[
        {'@type':'Article','headline':t[:110],'datePublished':b['date'].isoformat(),'dateModified':TODAY,'inLanguage':'ja','mainEntityOfPage':BASE+b['slug']+'.html','author':{'@type':'Organization','name':'ひるメモ','url':BASE},'publisher':{'@type':'Organization','name':'ひるメモ','url':BASE}},
        {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'ひるメモ','item':BASE},{'@type':'ListItem','position':2,'name':t[:60],'item':BASE+b['slug']+'.html'}]},
        {'@type':'ItemList','name':b.get('tochead','紹介された商品一覧'),'itemListElement':[{'@type':'ListItem','position':k+1,'name':it['name'],'url':BASE+b['slug']+'.html#i'+str(k+1)} for k,it in enumerate(b['items'])]}]}
    ogimg = next((it['img'] for it in b['items'] if it.get('img')), '')
    if ogimg: ld['@graph'][0]['image']=[ogimg]
    body += '<script type="application/ld+json">'+_json.dumps(ld,ensure_ascii=False)+'</script>'
    (out/f'{b["slug"]}.html').write_text(page(f'{b["slug"]}.html',t+'｜ひるメモ',b['intro'],body,'list',image=ogimg,kind='article',pub=b['date'].isoformat()),encoding='utf-8')

# ---- about
about=f'''<main style="display:flex;flex-direction:column;gap:16px">
<h1>このサイトについて</h1>
<div class="prose">
<p>「ひるメモ」は、お昼の情報番組で紹介された商品や宿を、あとから探しやすいようにまとめているサイトです。</p>
<h2>番組・放送局との関係</h2>
<p>当サイトは非公式のサイトで、番組・放送局・出演者・販売店・宿泊施設とは関係がありません。</p>
<h2>広告について</h2>
<p>当サイトはアフィリエイトプログラム（楽天アフィリエイト）を利用しています。サイト内のリンクから商品の購入や宿の予約があると、当サイトが紹介料を受け取ることがあります。</p>
<h2>掲載している情報について</h2>
<p>商品名・価格・買える場所、宿の部屋の広さ・食事・料金は、販売ページや予約ページで確認した時点のものです。商品の説明は、販売ページに書かれている事実をもとに当サイトの言葉でまとめています。価格や在庫、空室は変わることがあるため、購入・予約の前に各ページで最新の情報をご確認ください。</p>
<h2>アクセス情報の取り扱い</h2>
<p>リンク先の楽天市場・楽天トラベルでは、紹介料の計算のためにCookieが使われます。当サイトには入力フォームがなく、お名前やメールアドレスなどの個人情報は集めていません。</p>
<p>当サイトでは、どのページがよく読まれているかを知るために、Googleアナリティクスを使うことがあります。Googleアナリティクスは Cookie を使って、個人を特定しない形でアクセスの情報を集めます。集め方や止め方は<a href="https://policies.google.com/technologies/partner-sites?hl=ja" target="_blank" rel="noopener">Googleのページ</a>で確認できます。</p>
</div></main>'''
(out/'about.html').write_text(page('about.html','このサイトについて｜ひるメモ','ひるメモの運営方針、広告（アフィリエイト）の利用、掲載情報の扱いについて。',about,'about'),encoding='utf-8')
today=TODAY
urls=['']+[b['slug']+'.html' for b in B]+['about.html']
(out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod></url>\n' for u in urls)+'</urlset>\n',encoding='utf-8')
items_xml=''.join(f'<item><title>{e(b["title"])}</title><link>{BASE}{b["slug"]}.html</link><guid>{BASE}{b["slug"]}.html</guid><pubDate>{datetime.datetime.combine(b["date"],datetime.time(13,0)).strftime("%a, %d %b %Y %H:%M:%S +0900")}</pubDate><description>{e(cutdesc(b["intro"]))}</description></item>' for b in B)
(out/'feed.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0"><channel><title>ひるメモ</title><link>{BASE}</link><description>ヒルナンデスで紹介された商品・宿まとめ（非公式）</description><language>ja</language>{items_xml}</channel></rss>\n',encoding='utf-8')
(out/'b092c025ea1e7d07f8441da1c4355da6.txt').write_text('b092c025ea1e7d07f8441da1c4355da6',encoding='utf-8')
(out/'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n',encoding='utf-8')
for f in sorted(out.iterdir()): print(f.name, f.stat().st_size)
