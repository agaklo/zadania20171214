import argparse
import random, os
from os.path import basename
from glob import glob

def generate_files(directory):
    for i in range(random.randint(20,50)):
        file_name = os.path.join(directory,  ("file_%03d.csv" % i) )
        print ("Will print data to %s" % file_name)
        with open( file_name , "w") as f: 
            f.write("X;Y;Z;\n")
            for _ in range(random.randint(30,500)):
                f.write("%d;%d;%d;\n" % ( random.randint(-50000,50000),
                                        random.randint(-50000,50000),
                                        random.randint(-50000,50000)))    


def validate_header(line, file_name):
    normalized = []
    parts=line.split(';');
    for elem in parts: 
        normalized.append(elem.strip())

    if normalized[0] is not 'X':
        raise Exception("Header in file %s has no X on position 0" % file_name)
        
    if normalized[1] is not 'Y':
        raise Exception("Header in file %s has no Y on position 1" % file_name)

    if normalized[2] is not 'Z':
        raise Exception("Header in file %s has no Z on position 2" % file_name)


def validate_line(line, file_name):
    normalized = []
    parts=line.split(';');
    for elem in parts: 
        normalized.append(elem.strip())
    
    for i in range(3): 
        try:
           normalized[i] = int(normalized[i])
        except ValueError:
           raise Exception(
                "In file: %s at position %d found something " \
                "thait is not a number: %s" % (file_name, i, normalized[i]))
    return normalized


def verify_files(directory):
    for file_name in glob(os.path.join(directory, '*.csv')):
        temp_file_name = ("temp_file_%s.%04d") % ( basename(file_name) , random.randint(1,500) ) 
        with open(file_name, "r") as f: 
            with open(temp_file_name, "w") as output_f:
                print ("Verifiying file: %s" % file_name)
                header = f.readline()
                validate_header(header, file_name)
                output_f.write(header);

                for line in f:
                    normalized = validate_line(line, file_name)
                    numbers = []
                    for i in range(3):
                        #numbers.append(("%.3f" % ( int(normalized[i])/50000.0 )  ) );
                        numbers.append(str( int(normalized[i])/50000.0 ));
                    output_line = ';'.join(numbers)+"\n"
                    output_f.write(output_line)
        #jak juz oba sie zamkna
        os.rename( temp_file_name, file_name)
            

if __name__== '__main__':
    parser = argparse.ArgumentParser("test")
    parser.add_argument("command", 
	help="Issue a command to generate or normalize files", 
	choices=['generate','normalize']); 

    parser.add_argument("dir", 
	help="Choose directory with files"); 
    args = parser.parse_args()

    if args.command == "generate":
        print ("Script will generate sample files in directory: " + args.dir)
        generate_files(args.dir)
    elif args.command == "normalize":
        print ("Script will normalize files form directory: " + args.dir)
        verify_files(args.dir)
    else:
        print ("Unknown command: " +args.command)


