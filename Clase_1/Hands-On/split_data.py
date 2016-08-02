import argparse

parser = argparse.ArgumentParser(description='Split LAMMPS OUT')
parser.add_argument('-f', '--file', dest='file_path',
                    help='Archivo a splitear.')
parser.add_argument('-s', '--start', dest='start_word', default='Step',
                    help="Palabra comenzar el spliteo")
parser.add_argument('-e', '--end', dest='end_word', default='Loop',
                    help="Palabra terminar el spliteo")
parser.add_argument('-c', '--columns', dest='columns', action='append',
                    type=int,
                    help='Columnas a splitear. Si no se especifica, se guardan todas')
args = parser.parse_args()


def split_data(file_path, start_word='Step', end_word='Loop'):

    f_in = open(file_path, 'r')
    f_out = open(file_path + '.data', 'w')

    while True:
        line = f_in.readline()

        if start_word in line:
            # salto la linea q comienza con 'Step'
            line = f_in.readline()

            while True:
                # fin de los datos
                if end_word in line:
                    break
                # Si el archivo no llega a tener la palabra 'Loop'
                # este escript no va a terminar nunca!!
                if line == '':
                    break

                f_out.write(line)
                line = f_in.readline()

        # End of file
        if line == '':
            break

    f_in.close()
    f_out.close()


def extract_columns(file_path, columns=[0, 4]):
    f_in = open(file_path + '.data', 'r')
    f_out = open(file_path + '.split', 'w')

    for line in f_in.readlines():
        if line == '' or line == '\n':
            break

        split = line.split()
        for i, col in enumerate(columns):
            if i == 0:
                new_line = split[col]
            else:
                new_line += '\t' + split[col]
        new_line += '\n'
        f_out.write(new_line)

    f_in.close()
    f_out.close()

split_data(args.file_path, args.start_word, args.end_word)

if args.columns:
    extract_columns(args.file_path, args.columns)
