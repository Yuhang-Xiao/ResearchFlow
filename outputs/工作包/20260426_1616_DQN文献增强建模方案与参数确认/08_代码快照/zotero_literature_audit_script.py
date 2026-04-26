from pathlib import Path
import pandas as pd, re, shutil
zbase=Path(r'D:\桌面\codex\zotero')
out=Path(r'D:\桌面\codex\workflow1\outputs\工作包\20260426_1616_DQN文献增强建模方案与参数确认')
keywords=['DQN','deep reinforcement','reinforcement','safe reinforcement','constrained','constraint','POMDP','MDP','belief','food safety','risk','monitoring','AFB','aflatoxin','peanut','黄曲霉','花生','食品','风险','强化学习','监管','抽检']
rows=[]
issue=[]
for p in zbase.rglob('*'):
    if not p.is_file():
        continue
    name=str(p.name)
    full=str(p)
    rel=str(p.relative_to(zbase))
    hay=(name+' '+full).lower()
    path_hit=any(k.lower() in hay for k in keywords)
    if p.suffix.lower() in ['.md','.txt','.csv','.pdf'] and (path_hit or p.parent.name in ['deepreads','screened','candidates','pdfs']):
        rec={'relative_path':rel,'suffix':p.suffix.lower(),'bytes':p.stat().st_size,'path_keyword_hit':path_hit,'has_pdf':p.suffix.lower()=='.pdf','note_garbled':False,'question_marks_count':0,'replacement_char_count':0,'relevant_keywords':''}
        if p.suffix.lower() in ['.md','.txt','.csv']:
            try:
                txt=p.read_text(encoding='utf-8', errors='replace')
            except Exception as e:
                txt=''
                issue.append({'relative_path':rel,'issue':'read_failed','detail':str(e)})
            qm=txt.count('?????')
            rep=txt.count('�')
            rec['question_marks_count']=qm
            rec['replacement_char_count']=rep
            rec['note_garbled']= bool(qm or rep)
            if rec['note_garbled']:
                issue.append({'relative_path':rel,'issue':'garbled_note','detail':f'?????={qm}; replacement={rep}'})
            hits=[k for k in keywords if k.lower() in txt.lower() or k.lower() in hay]
            rec['relevant_keywords']=' | '.join(hits[:20])
        else:
            rec['relevant_keywords']=' | '.join([k for k in keywords if k.lower() in hay][:20])
        rows.append(rec)
inv=pd.DataFrame(rows).sort_values(['suffix','relative_path'])
inv.to_csv(out/'02_表格输出/zotero_literature_inventory.csv', index=False, encoding='utf-8-sig')
pd.DataFrame(issue).to_csv(out/'07_日志与错误/zotero_encoding_pdf_issue_log.csv', index=False, encoding='utf-8-sig')
md=['# Zotero 文献审计报告','',f'- 扫描根目录：`{zbase}`',f'- 候选文献/笔记/PDF 数：{len(inv)}',f'- 乱码或读取问题数：{len(issue)}','']
if issue:
    md.append('## 乱码/读取问题')
    for r in issue[:30]:
        md.append(f"- `{r['relative_path']}`: {r['issue']} ({r['detail']})")
    md.append('')
md.append('## 可用性原则')
md.append('含 `?????` 或 replacement character 的 Zotero note 不作为正式 DQN 建模依据；若该文献重要，应追溯 PDF 全文、出版页面或重新生成无乱码中文笔记。')
md.append('')
md.append('完整清单见 `02_表格输出/zotero_literature_inventory.csv`；问题日志见 `07_日志与错误/zotero_encoding_pdf_issue_log.csv`。')
(out/'04_报告输出/zotero_literature_audit_report.md').write_text('\n'.join(md), encoding='utf-8')
print(len(inv), len(issue))
