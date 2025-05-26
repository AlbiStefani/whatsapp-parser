from wa_parser.parser import WhatsappParser,WhatsappMessage
import csv
import argparse


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

def wa_messages_to_csv(messages,outpat_path):
    keys = ("date","time","sender","message","is_system_message")
    
    try:
        with open(outpat_path,"w",newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            for msg in messages:
                dict_writer.writerow(msg.to_dict())
    except IsADirectoryError:
        with open(outpat_path+"/a.csv","w",newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            for msg in messages:
                dict_writer.writerow(msg.to_dict())

def main():
    cli_parser = argparse.ArgumentParser(prog="Whatsapp Chat Parser", description="Simple implementation of a WA group chat parser")
    cli_parser.add_argument("filename", type=str)
    cli_parser.add_argument("-s","--sourcesystem",type=str,choices=["android"],default="android")
    cli_parser.add_argument("-c", "--count", action="store_true",default=False)
    cli_parser.add_argument("-o", "--output",type=str, default=None)
    cli_parser.add_argument("-f", "--format", type=str, choices=["csv"],default=None)

    args = cli_parser.parse_args()

    input_file = args.filename
    count = args.count
    output = args.output
    format = args.format
    source_system = args.sourcesystem


    parser = WhatsappParser(format=source_system)
    messages = parser.parse_wa_chat(input_file)

    if count:
        for k,v in count_user_messages(messages).items():
            print(f"{k}: {v}")
    if format == "csv" and output is not None:
        print(f"\nSaving messages to {output}\n")
        wa_messages_to_csv(messages=messages,outpat_path=output)
        print("\nDone.\n")

if __name__ == "__main__":
    main()
