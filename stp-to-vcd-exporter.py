#!/usr/bin/env python3
import argparse
import xml.etree.ElementTree as ET

def export(input_filename: str, output_filename: str, ns_per_div: int, window_start: int, window_length: int):
    # Read data from stp file.
    tree = ET.parse(input_filename)
    session = tree.getroot()

    signals = []

    data_view = session.find('./instance/signal_set/presentation/data_view')
    for net_or_bus in data_view:
        if net_or_bus.tag == 'net':
            name = net_or_bus.attrib['name']
            indices = [int(net_or_bus.attrib['storage_index'])]
            signals.append((name, indices))
        elif net_or_bus.tag == 'bus':
            name = net_or_bus.attrib['name']
            indices = []
            for net in net_or_bus:
                indices.append(int(net.attrib['storage_index']))
            signals.append((name, indices))

    data = session.find('./instance/signal_set/trigger/log/data')
    samples_array = data.text

    samples_count = int(data.attrib['sample_depth'])
    signals_count = len(samples_array) // samples_count

    samples = []

    for t in range(samples_count):
        samples.append(samples_array[t*signals_count:(t+1)*signals_count])

    if window_length == 0:
        window_length = samples_count

    samples = samples[window_start:window_start + window_length]

    # Generate vcd file.
    output = []
    output.append('$version stp-to-vcd-exporter.py 1.0 $end')
    output.append('$timescale 1 ns $end')

    for i, (name, indices) in enumerate(signals):
        c = chr(i + ord('!'))
        output.append(f'$var reg {len(indices)} {c} {name} $end')

    output.append('$enddefinitions $end')

    def get_value(t, i):
        _, indices = signals[i]
        if len(indices) == 1:
            index = indices[0]
            return samples[t][index]
        else:
            vs = 'b'
            for index in indices:
                vs += samples[t][index]
            vs += ' '
            return vs

    prev_values = ['' for _ in range(len(signals))]

    for t in range(len(samples)):
        values = [get_value(t, i) for i in range(len(signals))]

        if values != prev_values:
            output.append(f'#{t * ns_per_div}')

            for i in range(len(signals)):
                v = values[i]
                pv = prev_values[i]
                if v != pv:
                    c = chr(i + ord('!'))
                    output.append(f'{v}{c}')

        prev_values = values

    output.append('')

    with open(output_filename, 'wt') as f:
        f.write('\n'.join(output))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='Input filename (.stp file)')
    parser.add_argument('output', type=str, help='Output filename (.vcd file)')
    parser.add_argument('ns', type=int, help='Nanoseconds per div')
    parser.add_argument('--wstart', type=int, help='Window start (number of samples)', default=0)
    parser.add_argument('--wlen', type=int, help='Window length (number of samples)', default=0)
    args = parser.parse_args()
    export(args.input, args.output, args.ns, args.wstart, args.wlen)
