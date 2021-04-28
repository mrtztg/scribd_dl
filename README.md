A cross-platform python based utility to download audiobooks from scribd for personal offline use.
___

### Requirements
* Python 3.6
* Python module argparse
* Python module selenium

### Installation:
* clone with ```git clone https://github.com/mrtztg/scribd_dl.git```
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
    python3 scribd_dl.py -u my_email -p my_password -i my_links_file.txt
    ```

#### Disclaimer
Downloading books from Scribd for free maybe prohibited. This tool is meant for educational purposes only. Please support the authors by buying their titles.