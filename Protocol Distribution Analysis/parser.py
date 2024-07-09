import sys
import dpkt
from decimal import Decimal

def write_data(pcap_reader, human_readable):
        """
        Writes data from pcap reader to system output specified in main. CSV data in the
        format "(time since first packet), (payload size)" with 1 packet per line. Data
        is in seconds and bytes respectively, with seconds rounded to 6 decimal places. 
        Uses decimal module for accurate time computations.

        Args:
            pcap_reader (dpkt.pcap.Reader): Reader instance reading packets from file.
            human_readable (boolean): Ideally True if printing to command line, and False
                                      if saving to CSV. Just adds text before data, ex.
                                      "Packet size:" etc.

        Returns:
            None
        """

        # Var to save last packets time
        prev_t = None
        
        # Iterate over each packet in the pcap file
        for timestamp, buf in pcap_reader:

            # Parse the frame from the packet buffer
            eth = dpkt.ethernet.Ethernet(buf)

            # Filter anything unsupported--this should be none of them
            if not isinstance(eth.data, dpkt.ip.IP):
                print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__, file=sys.stderr)
                break

            # Access data within the frame
            ip = eth.data

            # Skip fragmented packets, since they don't have the data attribute
            if ip.mf or ip.offset > 0:
                continue
            
            # Access header for payload size
            header = ip.data
            payload_size = len(header.data)
            
            # Calculate inter arrival time
            if prev_t == None:
                prev_t = Decimal(timestamp)
                inter_t = Decimal('0.000000')
            else:
                inter_t = Decimal(timestamp) - prev_t
                inter_t = inter_t.quantize(Decimal('0.000000'))
                prev_t = Decimal(timestamp)

            # Print to stdout or save to CSV
            if human_readable:
                print(f"Time since last packet {inter_t}s | Payload size = {payload_size}B")
            else:
                print(f"{inter_t}, {payload_size}")
                

def main(pcap_path, output_path):
    """
    Process input data from a pcap file and write output to stdout or another file.

    Args:
        pcap_path (str): Path to the input pcap file containing data to be processed.
        output_path (str, optional): Path to the output file to write processed data.
                                     If not provided, processed data will be printed to console.

    Returns:
        None
    """
    # Open .pcap file for reading
    with open(pcap_path, 'rb') as f:
        # Create a dpkt.pcap.Reader instance
        pcap_reader = dpkt.pcap.Reader(f)

        # Saving to file
        if output_path:
            # Ensure output file name is accurate
            while True:
                user_input = input(f"Save packet data to {output_path}? (y/n): ").strip().lower()
                if user_input == 'y':
                    print(f"Parsing {pcap_path} data into {output_path}")
                    break
                else:
                    print("Operation cancelled.")
                    sys.exit(1)

            # Save original stdout
            original_stdout = sys.stdout

            # Open the file for writing
            with open(output_path, "w") as file:
                sys.stdout = file               # Change stdout
                write_data(pcap_reader, False)  # Write to file, CSV format
                sys.stdout = original_stdout    # Restore stdout
        
        # Write to stdout, human-readable
        else:
            write_data(pcap_reader, True)

# Script entry point
if __name__ == "__main__":

    # Setup command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python parser.py input_pcap output_csv (output data to file)")
        print("OR   : python parser.py input_pcap            (to print data)")
        sys.exit(1)
    else:
        pcap_path = sys.argv[1]

    output_path = sys.argv[2] if len(sys.argv) == 3 else None
    
    # Call main
    main(pcap_path, output_path)