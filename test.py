import subprocess
i=5
results=str(subprocess.check_output(['python3','arena.py','--agent1=cpy0126.RandomAgent','--agent2=cpy0126.RandomAgent','--round=2','--control=',i]))
ouput = results.split(' ')[-1]
output = output.split('\\')[0]
print(float(output))
