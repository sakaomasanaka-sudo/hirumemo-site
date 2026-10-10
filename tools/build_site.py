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
