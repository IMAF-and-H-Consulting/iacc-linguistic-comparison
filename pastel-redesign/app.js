(function(){
"use strict";
const err=(m)=>{const e=document.getElementById('err');e.style.display='block';e.textContent='Error: '+m;};
window.onerror=(m)=>err(m);
const $=(s)=>document.querySelector(s);
const el=(t,c,txt)=>{const d=document.createElement(t);if(c)d.className=c;if(txt!==undefined)d.textContent=txt;return d;};
const fmt=(v,d=1)=>v===null||v===undefined||Number.isNaN(v)?'—':Number(v).toFixed(d);
const pct=(v)=>v===null||v===undefined||Number.isNaN(v)?'—':(100*v).toFixed(1)+'%';

/* ---------- z bars ---------- */
/* Plain-English explanations for each style measure, shown on hover/focus. */
const TIP={
words_per_sentence:'Average sentence length, in words. Longer sentences make readers hold more in memory before the period arrives.',
sentence_len_sd:'How much sentence lengths vary. High means a lurching mix of short and very long sentences; low means a steady rhythm.',
sentence_len_p90:'The length of the longest tenth of sentences — how tough it gets at the extreme end.',
letters_per_word:'Average word length in letters. It creeps up when plain words are swapped for technical ones.',
syllables_per_word:'Average syllables per word — the raw ingredient inside every readability formula.',
long_words_pct:'Share of words with seven or more letters. "Medication" counts; "drug" does not.',
polysyllable_pct:'Share of words with three or more syllables — "implementation" counts, "plan" does not.',
flesch_reading_ease:'Flesch Reading Ease, a 0–100 scale where higher means easier. 60 is plain English; below 30 is academic-journal territory. The draft scores 0.6.',
flesch_kincaid_grade:'U.S. school grade needed to follow the text, from sentence length and syllables. 12 means high-school senior; the draft is at ~18, past a bachelor\u2019s degree.',
gunning_fog:'Gunning Fog grade level, from sentence length and 3+-syllable words. 17+ is graduate-school prose.',
smog:'SMOG grade level, based on polysyllables per sentence. Health materials for patients are usually written at 9 or below.',
coleman_liau:'Coleman–Liau grade level, computed from letters and sentences instead of syllables — a machine-friendly cousin of the others.',
ari:'Automated Readability Index: grade level from characters per word and words per sentence. Same idea, different yardstick.',
mattr:'Vocabulary variety in a sliding 500-word window (moving-average type–token ratio). Higher means the text keeps introducing new words instead of repeating itself.',
types_per_10k:'How many distinct words appear in a typical 10,000-word stretch. Higher means a wider working vocabulary.',
passive_per_100_sent:'Passive-voice sentences per 100 sentences ("was funded", "is required"). Passive constructions hide who is supposed to act.',
questions_per_100_sent:'Direct questions per 100 sentences. Earlier plans regularly posed questions to the reader; the draft almost never does.',
first_plural_per_1k:'"We / our / us" per 1,000 words — the sound of the authors speaking as themselves.',
committee_per_1k:'"The Committee" per 1,000 words — how often the text talks about the body that wrote it.',
modals_per_1k:'Modal verbs per 1,000 words (must, shall, should, will, would, may, might, can, could) — the dial between describing the world and directing it.',
deontic_index:'Share of modal verbs that impose obligation (must, shall, should, "required to") rather than predict or permit. The draft\u2019s 0.66 means two-thirds of its modals are marching orders.',
must_per_1k:'"Must" per 1,000 words — hard obligation.',
should_per_1k:'"Should" per 1,000 words — soft obligation. The draft uses it ten times as often as any earlier plan.',
will_per_1k:'"Will" per 1,000 words — plain prediction or promise. Earlier plans leaned on it; the draft avoids it.',
may_might_per_1k:'"May / might" per 1,000 words — permission and possibility, the language of open options.',
hedges_per_1k:'Hedging language per 1,000 words ("may", "suggests", "appears", "not yet known", "limited evidence") — how carefully the text qualifies its claims.',
boosters_per_1k:'Booster words per 1,000 ("clearly", "proven", "critical", "established") — how emphatically the text asserts its claims.',
nominalisation_pct:'Share of words that are verbs turned into abstract nouns ("implementation", "assessment", "coordination"). The "analyse the analysis" pattern: nouns multiply while actors disappear.',
acronyms_per_1k:'Initialisms per 1,000 words (IACC, CMS, NIH), excluding ordinary words the document also writes in lowercase.',
numerals_per_1k:'Digits and percentages per 1,000 words — how quantified the prose is.',
ref_markers_per_1k:'Citation markers per 1,000 words ([12], "et al.", "(Smith 2019)", PMIDs) — how visibly the text leans on sources.',
total_p10k:'Every explicit reference to autism or to autistic people, counted in one non-overlapping pass — person-first and identity-first phrasings, "on the spectrum", self-advocate/autistic-community, then bare "autism" and "ASD". Independent of which naming convention was in fashion. Held 199–314 per 10k for seventeen years (mean 268, sd 33); the draft is at 108.',
person_p10k:'The person-referring subset: phrases that point at autistic people rather than at autism as a topic. Peaked at 113 per 10k in SP-2023; the draft is at 28.',
abstract_p10k:'Autism or ASD named as a topic, without reference to a person. Also falls by half in the draft, which is why this is not a naming-convention effect.',
agency_p10k:'Federal agency acronyms (HHS, NIH, CDC, FDA, CMS, HRSA…) per 10,000 words — how much of the text is about the machinery rather than the subject.',
agency_autism_ratio:'Agency names per autism reference. Every plan from 2009 to 2023 sat between 0.03 and 0.12 — naming autism 8 to 36 times more often than any agency. The draft is at 1.54.',
community_p10k:'Less-profit-motivated organisations and the people around autistic individuals — nonprofits, advocacy groups, community partners and members, families, caregivers, parents, stakeholders — per 10,000 words. Term list harvested from the plans; full inventory in community_partner_terms.csv.',
community_combined_p10k:'The combined non-agency side: autistic-person references plus nonprofits, partners, community members, families, and advocacy groups, per 10,000 words. In SP-2023 this combined side is at 335; the draft is at 120, below agency visibility (167).',
agency_share_vs_community:'Of all actor-role mentions (agencies + autistic people + community/partner/family orgs), the share assigned to federal agencies. SP-2023: 32.2%. Draft: 75.1%.',
community_share_of_agents:'Of all actor-role mentions, the share assigned to autistic people and the community/partner/family/nonprofit layer together. SP-2023: 67.8%. Draft: 24.9%.'};
let zmode='sp23';
/* log2 ratio draft:SP-2023, so a doubling and a halving are the same bar length
   in opposite directions. Undefined (0 in the comparator) is clipped to the end. */
const lr=(r)=>{
  if(r.sp23===null||r.sp23===undefined||r.draft===null)return null;
  if(r.sp23===0&&r.draft===0)return 0;
  if(r.sp23===0)return 6; if(r.draft===0)return -6;
  return Math.log2(r.draft/r.sp23);
};
const zof=(r)=>zmode==='sp'?r.zSP:zmode==='all'?r.zAll:lr(r);
function drawZ(){
  try{
    const host=$('#zbars');host.innerHTML='';
    const baseline=zmode==='sp23'?'SP-2023':zmode==='sp'?'8-plan mean':'45-doc mean';
    const heading=el('div','style-row style-heading');
    ['Measure','Change',baseline,'2026 draft',zmode==='sp23'?'Ratio':'z-score'].forEach(t=>heading.appendChild(el('span','',t)));
    host.appendChild(heading);
    const rows=[...DATA.zscores].filter(r=>zof(r)!==null).sort((a,b)=>Math.abs(zof(b))-Math.abs(zof(a)));
    rows.forEach(r=>{
      const z=zof(r), ratioMode=zmode==='sp23';
      const row=el('div','style-row');row.dataset.feature=r.feature;
      row.appendChild(el('div','name',r.feature.replaceAll('_',' ')));
      const bar=el('div','zbar');bar.appendChild(el('div','axis'));
      [-4,-2,2,4].forEach(t=>{const tick=el('div','tick');tick.style.left=(50+t/6*50)+'%';bar.appendChild(tick);});
      const fill=el('div','fill '+(z>=0?'pos':'neg'));fill.style.width=Math.min(Math.abs(z),6)/6*50+'%';
      fill.style.background=Math.abs(z)>(ratioMode?1:2)?'var(--red)':Math.abs(z)>(ratioMode?0.5:1)?'var(--orange)':'#9a958a';
      bar.appendChild(fill);row.appendChild(bar);
      const before=zmode==='sp23'?fmt(r.sp23,2):zmode==='sp'?fmt(r.spMean,2):'mean';
      row.appendChild(el('div','baseline-value',before));
      row.appendChild(el('b','draft-value',fmt(r.draft,2)));
      const ratio=Math.pow(2,z);
      const change=ratioMode?(r.draft===0?'0 uses':r.sp23===0?'new':ratio>=1?'×'+fmt(ratio,1):'÷'+fmt(1/ratio,1)):(z>=0?'+':'')+fmt(z,1);
      row.appendChild(el('div','change-value',change));
      row.tabIndex=0;
      const desc=TIP[r.feature]||'';
      row.setAttribute('aria-label',r.feature.replaceAll('_',' ')+': '+baseline+' '+before+', 2026 draft '+fmt(r.draft,2)+', '+(ratioMode?'ratio ':'z-score ')+change+'. '+desc);
      const tip=el('div','tipbox');
      tip.innerHTML='<div class="tt">'+r.feature.replaceAll('_',' ')+'</div>'+desc+'<div class="tn">'+baseline+': '+before+' → 2026 draft: '+fmt(r.draft,2)+'</div>';
      row.appendChild(tip);host.appendChild(row);
    });
  }catch(e){err('zbars: '+e.message)}
}
drawZ();
$('#ztoggle').addEventListener('click',(ev)=>{
  const b=ev.target.closest('button');if(!b)return;
  zmode=b.dataset.m;
  document.querySelectorAll('#ztoggle button').forEach(x=>x.classList.toggle('on',x===b));
  drawZ();
});

/* ---------- trend chart ---------- */
/* Plain-English notes for the term selector. TERM_TIP keys must match lexicon_per10k.csv exactly. */
const GROUP_TIP={
'Naming autism':'The identity-language battleground: what the documents call the condition and the people who have it.',
'What is to be done':'The action vocabulary — what the government says it will do about autism.',
'Causes and biology':'Where autism comes from, in the documents\u2019 telling: genes, environment, and the contested frontier.',
'People, participation, equity':'Who is being talked about, and who gets a seat at the table.',
'Life course':'Autism across the lifespan, from first diagnosis to old age.',
'Governance and money':'The machinery: budgets, mandates, metrics, and who answers to whom.',
'Voice and modality':'How the text speaks — obligation, possibility, hope.'};
const TERM_TIP={
"person-first ('people with autism')":"Person-first phrasing — the convention long promoted by journals and agencies, putting the person before the diagnosis.",
"identity-first ('autistic people')":"Identity-first phrasing — the form most autistic self-advocates prefer, treating autism as part of who someone is.",
"'on the (autism) spectrum'":"The casual umbrella phrase — how the documents refer to the community in less clinical terms.",
"'autistic' (any use)":"Any use of the word 'autistic' — whether autistic people show up as people, not just as cases.",
"ASD (cs)":"The clinical acronym, counted case-sensitively. The draft nearly stopped using it.",
"'autism spectrum disorder(s)'":"The full formal DSM label.",
"'disorder(s)'":"The deficit framing embedded in the diagnostic label itself.",
"'condition(s)'":"'Condition' — a softer, less deficit-framed alternative to 'disorder'.",
"'profound autism'":"The contested Lancet Commission label (2021) for autistic people with the highest support needs. Absent from the entire record until the draft.",
"nonspeaking / minimally verbal":"Terms for nonspeaking autistic people — the population at the centre of the facilitated-communication and spelling-method wars.",
"neurodivers*":"Any 'neurodiversity / neurodivergent' word — the frame that treats autism as difference rather than defect.",
"treatment(s)":"Medical-model language: autism as something to treat. The draft's favoured word.",
"intervention(s)":"The behavioural and educational field's standard word, dominant in the record since 2009.",
"cure(s)":"The word the self-advocacy movement most objects to — watch whether an administration dares to use it.",
"prevent*":"'Prevent / prevention' — autism framed as something to avert. Controversial with self-advocates; central to the current administration's rhetoric.",
"precision":"As in precision medicine — biomarker-guided, individualised care.",
"evidence-based":"The field's own quality claim. Worth watching who gets to define it.",
"implementation":"Moving research into practice — 'implementation science' is the draft's organising buzzword.",
"vaccin*":"Any vaccine mention. Long near-taboo in IACC documents after the debunked link; it returns under the new administration.",
"immun*":"Immune-system language — 'immune', 'autoimmune', 'inflammation'. The draft elevates it to a 'Priority Therapeutic Domain'.",
"mitochondri*":"Mitochondrial dysfunction — a fringe-adjacent biomedical hypothesis the draft embraces.",
"gut / microbiome / GI":"Gut and microbiome language — a favourite topic of the biomedical parent-advocacy wing.",
"folate / leucovorin":"The B-vitamin pathway (leucovorin = folinic acid) that the administration promoted as an autism treatment in 2025.",
"regression":"Loss of acquired skills in early childhood — central to the 'regressive autism' narrative.",
"prenatal / maternal":"Exposures and events before or during birth — the search for environmental causes starts here.",
"exposure(s)":"Environmental exposures — chemicals, pollutants, medications. The administration's suspected culprits.",
"heterogene*":"'Heterogeneity' — acknowledging that autism is many different things, not one.",
"lived experience":"The community's own term for expertise gained by being autistic or caring for someone autistic.",
"self-advoca*":"Mentions of self-advocates — autistic people speaking for themselves. 'Nothing about us without us.'",
"disparit*":"'Disparities' — unequal access to diagnosis and services by race, income, geography.",
"equity / equitable":"Fairness framing in access and outcomes.",
"underserved":"Communities the system fails to reach.",
"women / girls / female(s)":"Autism in women and girls — historically under-diagnosed and under-studied.",
"quality of life / well-being":"Outcomes that matter to families, beyond symptom counts.",
"early identification/intervention":"Catching autism early — the services gateway of the past two decades.",
"adult(s) / adulthood":"Adulthood — where services famously fall off a cliff.",
"aging / older / elderly":"Autistic people growing old — almost entirely unstudied.",
"transition*":"The move from school to adult life — a persistent weak point.",
"employment / workforce / vocational":"Work — the outcome families rank among the highest and the system delivers least.",
"housing":"Where autistic adults live — a chronic unmet need.",
"mental health / psychiatric":"Co-occurring mental-health conditions — anxiety, depression, suicidality.",
"co-occurring / comorbid*":"Conditions that travel with autism (epilepsy, GI, sleep, anxiety). The draft reorganised the whole plan around them.",
"safety / wandering / elopement":"Wandering and elopement — a leading parental fear, and the target of Kevin and Avonte's Law.",
"dashboard(s)":"Management-by-metrics: the draft promises public performance dashboards.",
"statut* / mandate(s)":"Statutes and mandates — what the law requires the committee and agencies to do.",
"duplicat*":"Duplication-hunting — the efficiency frame: autism spending as overlap to eliminate.",
"portfolio":"The research portfolio — how the autism dollars are spread across topics.",
"metric(s) / milestone(s) / benchmark(s)":"Measurable targets — the draft's accountability machinery.",
"coordinat*":"The committee's statutory purpose: coordination across agencies.",
"partnership* / public-private":"Public–private partnerships — bringing foundations and industry into the federal effort.",
"the Secretary (cs)":"'The Secretary' of HHS, case-sensitive — how often the text addresses political leadership upward.",
"Congress (cs)":"'Congress' mentions — legislative accountability.",
"federal":"The word 'federal' itself — the draft's single most distinctive word (keyness z = 23.9).",
"IACC (cs)":"The committee talking about itself.",
"'must' (cs)":"Hard obligation, per 10,000 words.",
"'shall' (cs)":"Statutory obligation — the lawyer's 'must'.",
"'should' (cs)":"Soft obligation. The draft leans on it ten times harder than any earlier plan.",
"'will' (cs)":"Prediction or promise. Earlier plans leaned on it; the draft avoids it.",
"'may' / 'might' (cs)":"Permission and possibility — the language of open options.",
"recommend*":"'Recommend' — the committee's statutory verb: it advises rather than directs.",
"'we' / 'our' / 'us' (cs)":"First-person plural — the authors speaking as themselves.",
"'the Committee' (cs)":"How often the text talks about the body that wrote it.",
"urgen* / crisis / epidemic / emergency":"Crisis vocabulary — escalation rhetoric.",
"hope* / promis* / opportunit*":"Hope vocabulary — the optimism framing earlier plans preferred."};
function describeSeries(s){
  if(s.kind==='sty'||s.kind==='ref')return TIP[s.feature]||'';
  return TERM_TIP[s.term]||GROUP_TIP[s.group]||'';
}
const docs=DATA.trends.docs;
const allSeries=[...DATA.trends.lexicon.map(x=>({...x,kind:'lex'})),...DATA.trends.style.map(x=>({...x,kind:x.kind||'sty'}))];
const sel=$('#termsel');
/* Style first, then the subject-reference measures, then the domain lexicon:
   how the document is written is the part that does not depend on which naming
   convention was in fashion in a given year. The 91 lexicon terms are
   sub-grouped by their seven categories rather than listed flat, so the
   selector stays navigable. */
const groups={},order=[];
const grp=(key,label)=>{if(!groups[key]){const g=document.createElement('optgroup');g.label=label;groups[key]=g;order.push(key);}return groups[key];};
grp('sty','how the prose is written');
grp('ref','how often it names its own subject');
allSeries.forEach((s,i)=>{
  const o=document.createElement('option');o.value=i;
  const g=s.kind==='lex'?grp('lex:'+s.group,'lexicon · '+s.group):grp(s.kind,'');
  o.textContent=s.kind==='lex'?s.term:s.label;
  g.appendChild(o);
});
order.forEach(k=>sel.appendChild(groups[k]));
/* Open on "should" — the study's most extreme and most baseline-robust measure. */
const DEF=allSeries.findIndex(x=>x.feature==='should_per_1k');
sel.value=DEF>=0?DEF:0;

function star(cx,cy,r,fill){
  let p='';
  for(let i=0;i<10;i++){
    const a=-Math.PI/2+i*Math.PI/5, rr=i%2===0?r:r*0.42;
    p+=(i===0?'M':'L')+(cx+rr*Math.cos(a)).toFixed(1)+','+(cy+rr*Math.sin(a)).toFixed(1);
  }
  return '<path d="'+p+'Z" fill="'+fill+'" stroke="#1c1a16" stroke-width="1"/>';
}
function drawTrend(){
  try{
    const s=allSeries[+sel.value];
    const svg=$('#trendsvg');
    const W=780,H=380,pl=58,pr=18,pt=18,pb=40;
    const xs=docs.map(d=>d.year);
    const xmin=2008.4,xmax=2026.6;
    const vals=s.vals.map(v=>v===null?null:+v);
    const ymax=Math.max(...vals.filter(v=>v!==null),0.01)*1.08;
    const X=y=>pl+(y-xmin)/(xmax-xmin)*(W-pl-pr);
    const Y=v=>pt+(1-v/ymax)*(H-pt-pb);
    let h='<rect x="0" y="0" width="'+W+'" height="'+H+'" fill="#fbfaf6"/>';
    for(let g=0;g<=4;g++){
      const v=ymax*g/4,y=Y(v);
      h+='<line x1="'+pl+'" y1="'+y+'" x2="'+(W-pr)+'" y2="'+y+'" stroke="#e7e2d6"/>'+
         '<text x="'+(pl-8)+'" y="'+(y+4)+'" text-anchor="end" font-size="10" font-family="ui-monospace,monospace" fill="#8f897c">'+fmt(v,v<10?1:0)+'</text>';
    }
    docs.forEach(d=>{
      h+='<text x="'+X(d.year)+'" y="'+(H-pb+18)+'" text-anchor="middle" font-size="10" font-family="ui-monospace,monospace" fill="'+(d.draft?'#a42a28':'#8f897c')+'"'+(d.draft?' font-weight="bold"':'')+'>'+d.year+'</text>';
    });
    h+='<line x1="'+pl+'" y1="'+(H-pb)+'" x2="'+(W-pr)+'" y2="'+(H-pb)+'" stroke="#d9d3c5"/>';
    const prior=docs.map((d,i)=>({d,v:vals[i],i})).filter(p=>!p.d.draft&&p.v!==null);
    h+='<polyline fill="none" stroke="#31567e" stroke-width="1.8" points="'+prior.map(p=>X(p.d.year).toFixed(1)+','+Y(p.v).toFixed(1)).join(' ')+'"/>';
    prior.forEach(p=>{h+='<circle cx="'+X(p.d.year)+'" cy="'+Y(p.v)+'" r="4" fill="#31567e"><title>'+p.d.id+': '+fmt(p.v,2)+'</title></circle>';});
    const di=docs.findIndex(d=>d.draft);
    if(di>=0&&vals[di]!==null){
      const last=prior[prior.length-1];
      if(last)h+='<line x1="'+X(last.d.year)+'" y1="'+Y(last.v)+'" x2="'+X(docs[di].year)+'" y2="'+Y(vals[di])+'" stroke="#a42a28" stroke-width="1.6" stroke-dasharray="5,4"/>';
      h+=star(X(docs[di].year),Y(vals[di]),10,'#c8931a');
      h+='<text x="'+(X(docs[di].year)-2)+'" y="'+(Y(vals[di])-14)+'" text-anchor="end" font-size="11" font-family="ui-monospace,monospace" fill="#a42a28">draft '+fmt(vals[di],2)+'</text>';
    }
    svg.innerHTML=h;
    $('#trendnote').textContent=s.label+(s.kind==='lex'?' — per 10,000 words':'')+' · earlier plans 2009–2023, gold star = 2026 draft';
    const d=describeSeries(s);
    const tn=$('#termnote');
    if(d){tn.style.display='block';tn.innerHTML='<b>'+s.label+'</b> — '+d+(s.kind==='lex'?' <span style="font-family:var(--mono);font-size:10.5px">(cs) = case-sensitive · * = any ending · counts per 10,000 words</span>':'');}
    else tn.style.display='none';
  }catch(e){err('trend: '+e.message)}
}
/* ---------- grouped trend carousel ---------- */
const GROUPS=[
  {title:"Autism references collapse as agency references surge",
   note:"The page’s signature finding: the draft names autism less than half as often as any prior plan, while federal agency acronyms fill the space.",
   series:[
     {idx:allSeries.findIndex(x=>x.feature==='total_p10k'), color:'var(--blue)', label:'autism references /10k'},
     {idx:allSeries.findIndex(x=>x.feature==='agency_p10k'), color:'var(--orange)', label:'agency acronyms /10k'}
   ]},
  {title:"“Should” surges as “will” disappears",
   note:"The grammatical genre shift: earlier plans predict and describe (“will”); the draft commands (“should”).",
   series:[
     {idx:allSeries.findIndex(x=>x.feature==='should_per_1k'), color:'var(--red)', label:'“should” /1k'},
     {idx:allSeries.findIndex(x=>x.feature==='will_per_1k'), color:'var(--blue)', label:'“will” /1k'}
   ]},
  {title:"Treatments rise as interventions and services fall",
   note:"The clinical vocabulary swap: the unit of analysis shifts from persons receiving services to subtypes receiving compounds.",
   series:[
     {idx:allSeries.findIndex(x=>x.kind==='lex'&&x.term==='treatment(s)'), color:'var(--red)', label:'treatment(s) /10k'},
     {idx:allSeries.findIndex(x=>x.kind==='lex'&&x.term==='intervention(s)'), color:'var(--blue)', label:'intervention(s) /10k'}
   ]},
  {title:"Immune vocabulary surges as vaccine vocabulary is erased",
   note:"The causal-framing shift: immune and metabolic language rises tenfold; “vaccine,” previously used to address and refute causation claims, drops to zero.",
   series:[
     {idx:allSeries.findIndex(x=>x.kind==='lex'&&x.term==='immun*'), color:'var(--red)', label:'immun* /10k'},
     {idx:allSeries.findIndex(x=>x.kind==='lex'&&x.term==='vaccin*'), color:'var(--blue)', label:'vaccin* /10k'}
   ]},
  {title:"Person references thin as word length climbs",
   note:"The draft uses the longest words in the record while referring to autistic people less than half as often as any earlier plan.",
   series:[
     {idx:allSeries.findIndex(x=>x.feature==='person_p10k'), color:'var(--blue)', label:'person refs /10k'},
     {idx:allSeries.findIndex(x=>x.feature==='long_words_pct'), color:'var(--red)', label:'long words (7+ letters) %'}
   ]}
,
  {title:"Agencies claim 80% of actor roles as person visibility collapses",
   note:"In SP-2023, autistic people held 57.8% of agent-role mentions; the draft reverses this to 19.8%. Dependency-parse proxy for Hoefer & Martin (SCiL 2026) proto-role properties.",
   series:[
     {idx:allSeries.findIndex(x=>x.feature==='agency_p10k'), color:'var(--orange)', label:'agency visibility /10k'},
     {idx:allSeries.findIndex(x=>x.feature==='person_p10k'), color:'var(--blue)', label:'person visibility /10k'}
   ]},
  {title:"Agencies versus autistic people and less-profit-motivated organisations together",
   note:"One combined non-agency side: autistic people plus nonprofits, partners, community members, families, and advocacy groups. Combined visibility falls from 335/10k (SP-2023) and a 309/10k earlier-plan mean to 120 in the draft — below agency visibility (167). Combined actor-role share falls from 67.8% to 24.9%; agencies hold 75.1%. Term list in community_partner_terms.csv.",
   series:[
     {idx:allSeries.findIndex(x=>x.feature==='agency_p10k'), color:'var(--orange)', label:'federal agencies /10k'},
     {idx:allSeries.findIndex(x=>x.feature==='community_combined_p10k'), color:'var(--blue)', label:'autistic people + orgs /10k'}
   ]}];
let gSlide=0;
function drawGrouped(){
  const g=GROUPS[gSlide];
  $('#tgtitle').textContent=(gSlide+1)+' / '+GROUPS.length+' \u2014 '+g.title;
  const dotsEl=$('#tdots');
  dotsEl.innerHTML='';
  GROUPS.forEach((_,i)=>{const d=el('span','');if(i===gSlide)d.className='on';d.onclick=()=>{gSlide=i;drawGrouped();};dotsEl.appendChild(d);});
  g.series.forEach((sr,si)=>{
    const s=allSeries[sr.idx];
    if(!s)return;
    const svg=$('#tgsvg'+si);
    const lbl=$('#tgl'+si);
    lbl.textContent=sr.label;
    const W=380,H=320,pl=52,pr=12,pt=14,pb=36;
    const vals=s.vals.map(v=>v===null?null:+v);
    const ymax=Math.max(...vals.filter(v=>v!==null),0.01)*1.12;
    const xmin=2008.4,xmax=2026.6;
    const X=y=>pl+(y-xmin)/(xmax-xmin)*(W-pl-pr);
    const Y=v=>pt+(1-v/ymax)*(H-pt-pb);
    let h='<rect x="0" y="0" width="'+W+'" height="'+H+'" fill="#fbfaf6"/>';
    for(let gg=0;gg<=4;gg++){
      const v=ymax*gg/4,y=Y(v);
      h+='<line x1="'+pl+'" y1="'+y+'" x2="'+(W-pr)+'" y2="'+y+'" stroke="#e7e2d6"/>';
      h+='<text x="'+(pl-6)+'" y="'+(y+3)+'" text-anchor="end" font-size="9" font-family="ui-monospace,monospace" fill="#8f897c">'+fmt(v,v<10?1:0)+'</text>';
    }
    docs.forEach(d=>{
      h+='<text x="'+X(d.year)+'" y="'+(H-pb+16)+'" text-anchor="middle" font-size="9" font-family="ui-monospace,monospace" fill="'+(d.draft?'#a42a28':'#8f897c')+'"'+(d.draft?' font-weight="bold"':'')+'>'+(d.year%2===1||d.draft?d.year:'')+'</text>';
    });
    h+='<line x1="'+pl+'" y1="'+(H-pb)+'" x2="'+(W-pr)+'" y2="'+(H-pb)+'" stroke="#d9d3c5"/>';
    const prior=docs.map((d,i)=>({d,v:vals[i],i})).filter(p=>!p.d.draft&&p.v!==null);
    h+='<polyline fill="none" stroke="'+sr.color+'" stroke-width="2" points="'+prior.map(p=>X(p.d.year).toFixed(1)+','+Y(p.v).toFixed(1)).join(' ')+'"/>';
    prior.forEach(p=>{h+='<circle cx="'+X(p.d.year)+'" cy="'+Y(p.v)+'" r="3.5" fill="'+sr.color+'"><title>'+p.d.id+': '+fmt(p.v,2)+'</title></circle>';});
    const di=docs.findIndex(d=>d.draft);
    if(di>=0&&vals[di]!==null){
      const last=prior[prior.length-1];
      if(last)h+='<line x1="'+X(last.d.year)+'" y1="'+Y(last.v)+'" x2="'+X(docs[di].year)+'" y2="'+Y(vals[di])+'" stroke="#a42a28" stroke-width="1.4" stroke-dasharray="4,3"/>';
      h+=star(X(docs[di].year),Y(vals[di]),8,'#c8931a');
      h+='<text x="'+(X(docs[di].year))+'" y="'+(Y(vals[di])-11)+'" text-anchor="middle" font-size="10" font-family="ui-monospace,monospace" fill="#a42a28" font-weight="bold">'+fmt(vals[di],vals[di]<10?1:0)+'</text>';
    }
    svg.innerHTML=h;
  });
  $('#tgrpnote').textContent=g.note;
}
$('#tprev').onclick=()=>{gSlide=(gSlide-1+GROUPS.length)%GROUPS.length;drawGrouped();};
$('#tnext').onclick=()=>{gSlide=(gSlide+1)%GROUPS.length;drawGrouped();};
drawGrouped();

/* ---------- view toggle (grouped / single) ---------- */
$('#tviewtoggle').querySelectorAll('button').forEach(b=>{
  b.addEventListener('click',()=>{
    $('#tviewtoggle').querySelectorAll('button').forEach(x=>x.classList.remove('on'));
    b.classList.add('on');
    const v=b.dataset.v;
    $('#tgrouped').style.display=v==='grouped'?'':'none';
    $('#tsingle').style.display=v==='single'?'':'none';
    if(v==='single')drawTrend();
  });
});

drawTrend();
sel.addEventListener('change',drawTrend);

/* ---------- keyness ---------- */
let ktab='words',ksort=1,kdir=-1,kq='',kexp=false;
function ktable(){
  try{
    const host=$('#ktable');
    let rows=DATA.keyness[ktab].filter(r=>!kq||r[0].includes(kq));
    rows=[...rows].sort((a,b)=>{
      const va=a[ksort==='term'?0:ksort],vb=b[ksort==='term'?0:ksort];
      if(typeof va==='string')return kdir*va.localeCompare(vb);
      return kdir*(va-vb);
    });
    /* Keyness is about the ends of the distribution, not the middle. Default to
       the 25 most over-used and 25 most under-used terms; kexp shows all (capped
       at 400 rows so the page stays usable). Searching or re-sorting keeps the
       same window, applied to whatever the user asked for. */
    let lim,note;
    if(!kexp&&!kq&&ksort===1){
      const top=rows.slice(0,25),bot=rows.slice(-25);
      lim=top.concat(bot); note=' · showing the 25 most over- and 25 most under-used';
    }else{
      lim=rows.slice(0,400); note=rows.length>400?' (first 400 — refine the filter)':'';
    }
    let h='<div style="font-family:var(--mono);font-size:11px;color:var(--muted);margin-bottom:6px">'+rows.length+' terms'+note+' · positive z = more in the draft'+
      (!kq&&ksort===1?' · <a href="#keyness" id="kexpand" style="color:var(--red)">'+(kexp?'show the ends only':'show all')+'</a>':'')+'</div>';
    h+='<table><thead><tr><th data-c="term">term</th><th data-c="3" class="num">'+(ktab==='vs2023'?'SP-2023':'Earlier')+' /10k</th><th data-c="5" class="num">'+(ktab==='vs2023'?'SP-2023':'Earlier')+' uses</th><th data-c="2" class="num">2026 /10k</th><th data-c="4" class="num">2026 uses</th><th data-c="1" class="num">z</th></tr></thead><tbody>';
    lim.forEach((r,i)=>{
      if(!kexp&&!kq&&ksort===1&&i===25)h+='<tr><td colspan="6" style="padding:6px 0;color:var(--muted);font-family:var(--mono);font-size:11px;border-bottom:none">\u22ee  '+(rows.length-50).toLocaleString()+' terms between the two ends</td></tr>';
      h+='<tr><td class="t">'+r[0]+'</td><td class="num">'+fmt(r[3],1)+'</td><td class="num">'+r[5]+'</td><td class="num"><b>'+fmt(r[2],1)+'</b></td><td class="num">'+r[4]+'</td><td class="num" style="color:'+(r[1]>0?'var(--red)':'var(--blue)')+'">'+fmt(r[1],1)+'</td></tr>';
    });
    host.innerHTML=h+'</tbody></table>';
    host.querySelectorAll('th[data-c]').forEach(th=>th.onclick=()=>{const c=th.dataset.c;if(ksort===c)kdir*=-1;else{ksort=c==='term'?'term':+c;kdir=c==='term'?1:-1;}ktable();});
    const x=host.querySelector('#kexpand');
    if(x)x.onclick=(ev)=>{ev.preventDefault();kexp=!kexp;ktable();};
  }catch(e){err('keyness: '+e.message)}
}
ktable();
$('#ktoggle').addEventListener('click',(ev)=>{const b=ev.target.closest('button');if(!b)return;ktab=b.dataset.k;document.querySelectorAll('#ktoggle button').forEach(x=>x.classList.toggle('on',x===b));ktable();});
$('#ksearch').addEventListener('input',(ev)=>{kq=ev.target.value.toLowerCase().trim();ktable();});

/* ---------- vocabulary chips ---------- */
function chips(list,host,mode){
  try{
    const h=$(host);h.innerHTML='';
    list.forEach(r=>{
      const c=el('span','chip'+(r.kind==='name'?' name':''));
      c.innerHTML=(mode==='new'?'<b>'+r.term+'</b>':'<b style="color:var(--blue)">'+r.term+'</b>')+'<span class="c">'+(mode==='new'?r.count+'×':'in '+r.plans+' plans')+'</span>';
      h.appendChild(c);
    });
  }catch(e){err('chips: '+e.message)}
}
function vfilter(){
  const q=$('#vsearch').value.toLowerCase().trim();
  const nw=DATA.vocab.new.filter(r=>!q||r.term.includes(q));
  const dr=DATA.vocab.dropped.filter(r=>!q||r.term.includes(q));
  chips(nw,'#newchips','new');chips(dr,'#dropchips','drop');
  $('#newn').textContent=nw.length+' terms';$('#dropn').textContent=dr.length+' terms';
}
vfilter();
$('#vsearch').addEventListener('input',vfilter);

/* ---------- trend reversals ---------- */
try{
  const host=$('#ctlbars');
  const mx=100;  /* bars are percentages: each document has its own trend-set size */
  DATA.control.forEach(r=>{
    const row=el('div','zrow');
    row.style.gridTemplateColumns='130px 1fr 130px';
    row.appendChild(el('div','name',r.id));
    const bar=el('div');bar.style.cssText='position:relative;height:14px';
    const b=el('div');b.style.cssText='position:absolute;left:0;top:2px;bottom:2px;width:'+(r.pct/mx*100)+'%;background:'+(r.draft?'var(--red)':'#8a96a6');
    bar.appendChild(b);row.appendChild(bar);
    row.appendChild(el('div','zval',fmt(r.pct,0)+'% · '+r.n+' of '+r.tot));
    row.title=r.id+' scored against its own past: '+r.n+' of '+r.tot+' strong trends reversed ('+fmt(r.pct,1)+'%)';
    host.appendChild(row);
  });
}catch(e){err('control: '+e.message)}

let tmode='strong',tsort='late',tdir=-1;
function ttable(){
  try{
    const host=$('#ttable');
    let rows=DATA.termTrends.filter(r=>tmode==='all'?true:tmode==='strong'?r.strong:r.verdict===tmode);
    rows=[...rows].sort((a,b)=>tdir*(a[tsort]>b[tsort]?1:a[tsort]<b[tsort]?-1:0));
    let h='<div style="font-family:var(--mono);font-size:11px;color:var(--muted);margin-bottom:6px">'+rows.length+' terms</div>';
    h+='<table><thead><tr><th data-c="term">term</th><th data-c="rho" class="num">ρ 2007–23</th><th data-c="early" class="num">/10k before 2013</th><th data-c="late" class="num">/10k 2018+</th><th data-c="draft" class="num">draft /10k</th><th>verdict</th></tr></thead><tbody>';
    rows.forEach(r=>{
      h+='<tr><td class="t">'+r.term+'</td><td class="num">'+fmt(r.rho,2)+'</td><td class="num">'+fmt(r.early,1)+'</td><td class="num">'+fmt(r.late,1)+'</td><td class="num"><b>'+fmt(r.draft,1)+'</b></td><td><span class="pill '+(r.verdict==='reverses trend'?'rev':'con')+'">'+r.verdict+'</span></td></tr>';
    });
    host.innerHTML=h+'</tbody></table>';
    host.querySelectorAll('th[data-c]').forEach(th=>th.onclick=()=>{const c=th.dataset.c;if(tsort===c)tdir*=-1;else{tsort=c;tdir=c==='term'?1:-1;}ttable();});
  }catch(e){err('trend table: '+e.message)}
}
ttable();
$('#ttoggle').addEventListener('click',(ev)=>{const b=ev.target.closest('button');if(!b)return;tmode=b.dataset.t;document.querySelectorAll('#ttoggle button').forEach(x=>x.classList.toggle('on',x===b));ttable();});

/* ---------- subject reference (autism vs agencies) ---------- */
try{
  const host=$('#refbars');
  const mx=Math.max(...DATA.reference.map(r=>Math.max(r.total,r.agency)));
  DATA.reference.forEach(r=>{
    const row=el('div','zrow');
    row.style.gridTemplateColumns='130px 1fr 150px';
    row.appendChild(el('div','name',r.id==='SP-2026-DRAFT'?'2026 draft':r.id));
    const bar=el('div');bar.style.cssText='position:relative;height:16px';
    const b1=el('div');b1.style.cssText='position:absolute;left:0;top:1px;bottom:8px;width:'+(100*r.total/mx)+'%;background:var(--blue)';
    const b2=el('div');b2.style.cssText='position:absolute;left:0;top:9px;bottom:1px;width:'+(100*r.agency/mx)+'%;background:var(--orange)';
    bar.appendChild(b1);bar.appendChild(b2);
    row.appendChild(bar);
    const v=el('div','zval');
    v.innerHTML='<b>'+fmt(r.total,0)+'</b> vs '+fmt(r.agency,0)+' · '+fmt(r.ratio,2)+':1';
    row.appendChild(v);
    row.title=r.id+': '+fmt(r.total,1)+' autism references and '+fmt(r.agency,1)+' agency acronyms per 10k words ('+fmt(r.person,1)+' of the autism references are to autistic people)';
    host.appendChild(row);
  });
}catch(e){err('refbars: '+e.message)}

/* ---------- carryover ---------- */
try{
  const host=$('#carrybars');
  DATA.carryover.forEach(r=>{
    const row=el('div','zrow');
    row.style.gridTemplateColumns='130px 1fr 155px';
    row.appendChild(el('div','name',r.id));
    const bar=el('div');bar.style.cssText='position:relative;height:16px';
    const b1=el('div');b1.style.cssText='position:absolute;left:0;top:1px;bottom:8px;width:'+(r.prev*100*1.6)+'%;background:var(--blue)';
    const b2=el('div');b2.style.cssText='position:absolute;left:0;top:9px;bottom:1px;width:'+(r.any*100*1.6)+'%;background:var(--orange)';
    bar.appendChild(b1);bar.appendChild(b2);
    row.appendChild(bar);
    row.appendChild(el('div','zval',fmt(r.prev*100,2)+'% / '+fmt(r.any*100,2)+'%'));
    row.title=r.id+': '+fmt(r.prev*100,2)+'% from previous plan, '+fmt(r.any*100,2)+'% from any earlier publication';
    host.appendChild(row);
  });
}catch(e){err('carryover: '+e.message)}

/* ---------- sections table ---------- */
let ssort=null,sdir=-1;
function stable(){
  try{
    const host=$('#sectable');
    let rows=[...DATA.sections];
    if(ssort)rows.sort((a,b)=>{const va=a[ssort],vb=b[ssort];if(typeof va==='string')return sdir*va.localeCompare(vb);return sdir*((va??-1e9)-(vb??-1e9));});
    let h='<table><thead><tr><th data-c="section">section</th><th data-c="pages">pages</th><th data-c="words" class="num">words</th><th data-c="fk" class="num">FK grade</th><th data-c="should" class="num">should /1k</th><th data-c="idf" class="num">identity-first</th><th data-c="novel" class="num">new text</th><th data-c="nearest">nearest earlier doc</th></tr></thead><tbody>';
    rows.forEach(r=>{
      h+='<tr><td class="t">'+r.section+'</td><td>'+r.pages+'</td><td class="num">'+r.words.toLocaleString()+'</td><td class="num"'+(r.fk>=18?' style="color:var(--red)"':'')+'>'+fmt(r.fk,1)+'</td><td class="num"'+(r.should>=10?' style="color:var(--red)"':'')+'>'+fmt(r.should,1)+'</td><td class="num">'+pct(r.idf)+'</td><td class="num">'+pct(r.novel)+'</td><td>'+r.nearest+'</td></tr>';
    });
    host.innerHTML=h+'</tbody></table>';
    host.querySelectorAll('th[data-c]').forEach(th=>th.onclick=()=>{const c=th.dataset.c;if(ssort===c)sdir*=-1;else{ssort=c;sdir=-1;}stable();});
  }catch(e){err('sections: '+e.message)}
}
stable();
})();

// Keep chapter navigation and table controls usable on keyboard and touch.
const chapterAnchors=[...document.querySelectorAll('.chapter-rail a')];
const chapterObserver=new IntersectionObserver(entries=>{
  const visible=entries.filter(e=>e.isIntersecting)[0];
  if(!visible)return;
  chapterAnchors.forEach(a=>{const active=a.hash==='#'+visible.target.id;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
},{rootMargin:'-10% 0px -75% 0px'});
chapterAnchors.forEach(a=>{const section=document.querySelector(a.hash);if(section)chapterObserver.observe(section);});
document.querySelectorAll('.toggle,.view-toggle').forEach(group=>{
  const sync=()=>group.querySelectorAll('button').forEach(b=>b.setAttribute('aria-pressed',b.classList.contains('on')));
  sync();group.addEventListener('click',sync);
});
function prepareHeaders(){document.querySelectorAll('th[data-c]').forEach(th=>{
  if(th.tabIndex===0)return;th.tabIndex=0;th.title='Sort by '+th.textContent;
  th.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();th.click();}});
});}
prepareHeaders();
new MutationObserver(prepareHeaders).observe(document.querySelector('.report'),{childList:true,subtree:true});
