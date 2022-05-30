with open(f"I:\data\Simulation\Simulation_2022_04_21__13_45_51\events.dat", 'rt') as input_file:
    with open(f"I:\data\Simulation\Simulation_2022_04_21__13_45_51\events_fixed.dat", 'wt') as output_file:
        for line in input_file:
            #read replace the string and write to output file
            #print(line)
            output_file.write(line.replace('\Å§', '\t'))