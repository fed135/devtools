import os, sys

pre = '{"images":['
post = ']}'

def scan_dir(dir):
    create_manifest(dir, "")
    for root, dirs, files in os.walk(dir):  
        for folder in dirs:
            create_manifest(folder, root)


def create_manifest(dir, r):
    print "    Creating manifest for " + dir
    final = pre
    count = 0
    for item in os.listdir(os.path.join(r, dir)):
        if os.path.isfile(os.path.join(r, dir, item)):
            final += '{"name":"'+item+'", "size":'+str(os.path.getsize(os.path.join(r, dir, item)))+'},'
            count += 1
    print ("    %d files added to manifest " + dir) % count
    final = final[:-1]
    final += post

    print "    Writing..."
    f = open(os.path.join(r, dir , "manifest.json"),'w+')
    f.write(final)
    f.close()
    print "    Manifest completed!"
    print " "

if __name__ == "__main__":
    
    print "==================================="
    print "Scanning directory..."
    scan_dir(sys.argv[1])
    print "Scan completed!"
    