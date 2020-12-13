import subprocess
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--test', default="MyAgentR")
parser.add_argument('--agent2', default="cpy0126.RandomAgent")
parser.add_argument('--rounds', default=300, type=int)
parser.add_argument('--f',default=6,type=int)
parser.add_argument('--t',default=10,type=int)
parser.add_argument('--s',default=1,type=int)
args = parser.parse_args()
agent1 = 'cpy0126.'+args.test
args = parser.parse_args()
for i in range(args.f,args.t+1,args.s):
	results=str(subprocess.check_output(['python3','my_arena.py','--agent1',agent1,'--agent2',args.agent2,'--rounds',str(args.rounds),'--headless','--control',str(i)]))
	output = results.split(' ')[-1]
	output = output.split('\\')[0]
	print(i,float(output))
