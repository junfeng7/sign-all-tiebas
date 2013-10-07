cmd=''
f=open('server.sql','r')    
for line in f:
    if not line:
        break
    line=line.strip()
    if not line:
        continue
    cmd+=line
    if line[len(line)-1]==';':
        print cmd
        cmd=''
f.close()

