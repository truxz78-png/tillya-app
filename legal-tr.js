// Automatic translation for the legal pages (same method as index.html: no Google banner).
// Uses the language chosen in the app, or the phone's language. English stays as is.
(function(){
  var saved=null; try{saved=localStorage.getItem('tillya-lang')}catch(e){}
  var base=(navigator.languages&&navigator.languages[0])||navigator.language||'en';
  var lang=saved||(base.toLowerCase().indexOf('zh')===0?'zh-CN':base.split('-')[0]);
  if(!lang||lang==='en')return;
  document.documentElement.lang=lang;
  if(lang==='ar')document.documentElement.dir='rtl';
  var cache={}; try{cache=JSON.parse(localStorage.getItem('tillya-tr-'+lang)||'{}')}catch(e){}
  function nodes(){var out=[],w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,{acceptNode:function(n){var p=n.parentElement;if(!p||/^(SCRIPT|STYLE|NOSCRIPT)$/.test(p.tagName)||p.closest('[translate=no],.notranslate')||!n.nodeValue.trim())return NodeFilter.FILTER_REJECT;return NodeFilter.FILTER_ACCEPT;}});while(w.nextNode())out.push(w.currentNode);return out;}
  async function tr(t){var k=t.trim();if(cache[k])return cache[k];var r=await fetch('https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl='+lang+'&dt=t&q='+encodeURIComponent(k));var j=await r.json();var s=j[0].map(function(x){return x[0]}).join('');if(/^[A-Z]/.test(k)&&s)s=s.charAt(0).toUpperCase()+s.slice(1);cache[k]=s;return s;}
  addEventListener('load',async function(){
    var note=document.getElementById('trnote');if(note)note.hidden=false;
    for(var n of nodes()){var o=n.nodeValue,lead=o.match(/^\s*/)[0],trail=o.match(/\s*$/)[0];try{n.nodeValue=lead+await tr(o)+trail;}catch(e){}}
    try{localStorage.setItem('tillya-tr-'+lang,JSON.stringify(cache))}catch(e){}
  });
})();
