from flask import Flask, render_template, request, jsonify
import sqlite3, os, subprocess, tempfile, sys, time, json
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(ROOT, 'codearena.db')
app = Flask(__name__)
CHALLENGES = [
 {'id':'two-sum','title':'Two Sum','difficulty':'Easy','topic':'Arrays, Hash Maps','description':'Given a list of integers and a target, return the indices of two numbers that add to the target. Return indices in ascending order.','starter':'def solve(nums, target):\n    seen = {}\n    for i, value in enumerate(nums):\n        if target - value in seen:\n            return [seen[target - value], i]\n        seen[value] = i\n    return []\n','cases':[({'nums':[2,7,11,15],'target':9},[0,1]),({'nums':[3,2,4],'target':6},[1,2]),({'nums':[3,3],'target':6},[0,1])]},
 {'id':'valid-palindrome','title':'Valid Palindrome','difficulty':'Easy','topic':'Strings','description':'Return True if the string is a palindrome when case and non-alphanumeric characters are ignored.','starter':'def solve(text):\n    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())\n    return cleaned == cleaned[::-1]\n','cases':[({'text':'A man, a plan, a canal: Panama'},True),({'text':'race a car'},False),({'text':''},True)]},
 {'id':'first-unique','title':'First Unique Character','difficulty':'Medium','topic':'Strings, Hash Maps','description':'Return the index of the first non-repeating character, or -1 if every character repeats.','starter':'def solve(text):\n    counts = {}\n    for ch in text:\n        counts[ch] = counts.get(ch, 0) + 1\n    for i, ch in enumerate(text):\n        if counts[ch] == 1:\n            return i\n    return -1\n','cases':[({'text':'leetcode'},0),({'text':'loveleetcode'},2),({'text':'aabb'},-1)]}
]
def connect():
 c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init_db():
 with connect() as c:
  c.execute('CREATE TABLE IF NOT EXISTS submissions(id INTEGER PRIMARY KEY AUTOINCREMENT,candidate TEXT NOT NULL,challenge_id TEXT NOT NULL,passed INTEGER NOT NULL,total INTEGER NOT NULL,runtime_ms INTEGER NOT NULL,submitted_at TEXT NOT NULL)')
def evaluate(code, inputs, expected):
 # Local portfolio demo only; submitted code is not sandboxed. Do not expose publicly.
 payload=json.dumps(inputs)
 harness='import json\n'+code+'\nif __name__ == "__main__":\n    payload = json.loads('+repr(payload)+')\n    print(json.dumps(solve(**payload)))\n'
 path=None
 try:
  with tempfile.NamedTemporaryFile('w',suffix='.py',delete=False,encoding='utf-8') as f: f.write(harness); path=f.name
  start=time.perf_counter(); p=subprocess.run([sys.executable,path],capture_output=True,text=True,timeout=2,cwd=ROOT)
  ms=int((time.perf_counter()-start)*1000)
  if p.returncode: return False,ms,(p.stderr or 'Execution failed')[-400:]
  actual=json.loads(p.stdout.strip().splitlines()[-1]); return actual==expected,ms,None
 except subprocess.TimeoutExpired: return False,2000,'Time limit exceeded (2 seconds).'
 except Exception as e: return False,0,str(e)[:300]
 finally:
  if path and os.path.exists(path): os.remove(path)
@app.route('/')
def home(): return render_template('index.html', challenges=CHALLENGES)
@app.route('/health')
def health(): return jsonify(status='ok',service='CodeArena',timestamp=datetime.now(timezone.utc).isoformat())
@app.route('/api/challenges')
def challenges(): return jsonify([{k:v for k,v in x.items() if k not in ('cases','starter')} for x in CHALLENGES])
@app.route('/api/leaderboard')
def leaderboard():
 with connect() as c: rows=c.execute('SELECT candidate,SUM(passed) passed_tests,SUM(total) total_tests,COUNT(*) submissions FROM submissions GROUP BY candidate ORDER BY passed_tests DESC, submissions ASC LIMIT 10').fetchall()
 return jsonify([dict(r) for r in rows])
@app.route('/api/submissions')
def recent():
 with connect() as c: rows=c.execute('SELECT candidate,challenge_id,passed,total,runtime_ms,submitted_at FROM submissions ORDER BY id DESC LIMIT 12').fetchall()
 return jsonify([dict(r) for r in rows])
@app.route('/api/submit',methods=['POST'])
def submit():
 d=request.get_json(silent=True) or {}; name=str(d.get('candidate','Developer')).strip()[:40] or 'Developer'; cid=d.get('challenge_id'); code=str(d.get('code',''))[:12000]
 ch=next((x for x in CHALLENGES if x['id']==cid),None)
 if not ch: return jsonify(error='Choose a valid challenge.'),400
 if 'def solve(' not in code: return jsonify(error='Your code must define solve(...).'),400
 results=[]; passed=0; total_ms=0
 for inp,expected in ch['cases']:
  ok,ms,err=evaluate(code,inp,expected); passed+=int(ok); total_ms+=ms; results.append({'passed':ok,'runtime_ms':ms,'error':err})
 stamp=datetime.now(timezone.utc).isoformat(timespec='seconds')
 with connect() as c: c.execute('INSERT INTO submissions(candidate,challenge_id,passed,total,runtime_ms,submitted_at) VALUES(?,?,?,?,?,?)',(name,cid,passed,len(ch['cases']),total_ms,stamp))
 return jsonify(passed=passed,total=len(ch['cases']),runtime_ms=total_ms,results=results,message='All tests passed!' if passed==len(ch['cases']) else 'Some tests failed. Review the results and try again.')
if __name__=='__main__':
 init_db(); app.run(host='127.0.0.1',port=5000,debug=False)
