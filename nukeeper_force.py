import argparse
import os
import re


def main():

    parser = argparse.ArgumentParser(description='Nuget package updater')
    parser.add_argument("--p", default=None, required=False, dest="package", help="Package name")
    parser.add_argument("--v", default=None, required=False, dest="version", help="Package version")
    parser.add_argument("--n", default=None, required=False, dest="nukeeper", help="Nukeeper output file")

    args = parser.parse_args()

    if  args.nukeeper != None:
        packages = []
        f = open(args.nukeeper, 'r')
        lines = f.read().splitlines()        
        for line in lines:
            search = re.match(r'([\w\.]*) to ([\d\.]+)', line)
            if search != None:
                pair = search.groups(0)
                print(f'Found update {pair[0]} to {pair[1]}')
                packages.append(pair)
        f.close()
        print(f'=> Found {len(packages)} possible updates')

        for package in packages:
            update_package(package[0], package[1])

        exit()        

    if  args.package == None and args.version == None:
        print('You need to specify package and version to update')

    update_package(args.package, args.version)

def update_package(packageName, packageVersion):
    print(f'Updating {packageName} to {packageVersion}')

    pattern = f'Include[\s]*=[\s]*()"{packageName}"[\s]*Version[\s]*=[\s]*"[\d\.]+"'
    pattern.encode('unicode_escape')
    replaceString = f'Include="{packageName}" Version="{packageVersion}"'
    replaceString.encode('unicode_escape')        

    rootDir = os.curdir
    csprojFiles = [os.path.join(root, name)
                for root, dirs, files in os.walk(rootDir)
                for name in files
                if name.endswith((".csproj"))]


    for project in csprojFiles:    
        data = []
        replaceCount = 0        
        f = open(project, 'r')
        lines = f.read().splitlines()
        for line in lines:
            line.encode('unicode_escape')
            result = re.subn(pattern, replaceString, line)
            data.append(str(result[0]))
            replaceCount += result[1]
        f.close()
        
        if replaceCount > 0:
            f = open(project, 'w')
            print(f'\tUpdating {project}')
            f.write('\n'.join(data))
            f.write('\n')
            f.close()

if __name__== "__main__":
  main()
