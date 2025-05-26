from wa_parser.parser import WhatsappParser,WhatsappMessage
import csv
import argparse
import os
import sys


def count_user_messages(messages):
    count = {}
    for msg in messages:
        if not msg.is_system_message:
            sender = msg.sender
            if sender not in count.keys():
                count[sender] = 1
            else:
                count[sender] += 1
    return count

def wa_messages_to_csv(messages,output_path):
    keys = ("date","time","sender","message","is_system_message")
    if os.path.isdir(output_path):
        output_file_path = os.path.join(output_path, "parsed_chat.csv")
    else:
        output_file_path = output_path
    with open(output_file_path,"w",newline="", encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        for msg in messages:
            dict_writer.writerow(msg.to_dict())


def main():
    cli_parser = argparse.ArgumentParser(prog="Whatsapp Chat Parser", description="Simple implementation of a WA group chat parser")
    cli_parser.add_argument("filename", type=str, help="Raw txt file, as extracted from Whatsapp")
    cli_parser.add_argument("-s","--sourcesystem",type=str,choices=["android"],default="android",help="System from where the raw txt file comes from (Android,ios)")
    cli_parser.add_argument("-c", "--count", action="store_true",default=False,help="Print to console the number of sent messages for each user")
    cli_parser.add_argument("-o", "--output",type=str, default="./",help="Path to save the parsed output, if not provided file will be saved on the current directory")
    cli_parser.add_argument("-f", "--format", type=str, choices=["csv"],default=None,help="Format to save the parsed output, if not provided parsed output will not be saved")

    args = cli_parser.parse_args()

    input_file = args.filename
    count = args.count
    output = args.output
    format = args.format
    source_system = args.sourcesystem


 
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    try:
        parser = WhatsappParser(format=source_system)
        messages = parser.parse_wa_chat(input_file)

        if count:
            for k,v in count_user_messages(messages).items():
                print(f"{k}: {v}")
        if format == "csv" and output is not None:
            print(f"\nSaving messages to {output}\n")
            wa_messages_to_csv(messages=messages,output_path=output)
            print("\nDone.\n")
    except Exception as e:
        print(f"An error occurred during parsing: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
