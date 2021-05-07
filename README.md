A cross-platform python based utility to download audiobooks from scribd for personal offline use.
___

### Requirements
* **_A premium Scribd account_**
* Python 3.6
* Python module argparse
* Python module selenium

### Installation:
* clone with ```git clone https://github.com/mrtztg/scribd_dl.git``` or download the release file and extract it.
* install requirements with ```pip install -r requirements.txt```

### Usage:
* Make a text file (e.g:my_links_file.txt) in script folder (alongside scribd_dl.py) and put books url in it (one url per line). example:
  ```
  https://www.scribd.com/audiobook/265831522/Elon-Musk-Tesla-Spacex-and-the-Quest-for-a-Fantastic-Future
  https://www.scribd.com/audiobook/366626161/Influence-The-Psychology-of-Persuasion
  https://www.scribd.com/audiobook/237848637/The-Alchemist
  ```
* Download book with script. Sample:
    ```shell
    python scribd_dl.py -u "my_email" -p "my_password" -i my_links_file.txt
    ```
  
### Advanced usage:
```
usage: scribd_dl.py [-h] [-u USERNAME] [-p PASSWORD] [-i INPUT] [--display] [-v]

Download audiobooks from scribd.

optional arguments:
  -h, --help            show this help message and exit
  -u USERNAME, --username USERNAME
                        Account email/username
  -p PASSWORD, --password PASSWORD
                        Account password
  -i INPUT, --input INPUT
                        Specify the file that contains book/audiobooks url list
  --display             Display the browser to user
  -v, --verbose         Increase output verbosity

```

#### Disclaimer
Downloading books from Scribd for free maybe prohibited. This tool is meant for educational purposes only. Please support the authors by buying their titles.