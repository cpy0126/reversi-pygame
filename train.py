import subprocess
result = subprocess.check_output(['python3','arena.py','--agent1','cpy0126.MyAgent','--agent2','cpy0126.MyAgentR','--headless','--rounds','30'])
print(result)
result = subprocess.check_output(['python3','arena.py','--agent2','cpy0126.MyAgent','--agent1','cpy0126.MyAgentR','--headless','--rounds','30'])
print(result)