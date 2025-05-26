# WhatsApp group chat parser

Simple implementation of a whatsapp group chat parser. <br>
<b>wa_parser/</b> contains the implementation of the actual parser <br>

### How to
1. Clone repo
2. Install requirements
```
pip install -r requirements.txt
```
3. Install wa_parser in development mode
```
pip install -e .
```
### Example usage
To save the messages in a csv file in the current location:
```
python scripts/script.py path/to/file.txt -c -f csv
```

**Compatibility:** This parser should be compatible across different Android versions. 

## To Do
- [ ] Implement support for IOS chat
